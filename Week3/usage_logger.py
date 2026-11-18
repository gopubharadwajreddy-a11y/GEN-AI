import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError


def fix_mongo_uri(uri: str) -> str:
    """Automatically escape special characters in password if unquoted."""
    if not uri:
        return uri
    # Match standard mongodb or mongodb+srv URI with user:pass@host
    match = re.match(r"^(mongodb(?:\+srv)?://)([^:]+):(.*)@([^/@]+)(/?.*)$", uri)
    if match:
        prefix, user, pwd, host, suffix = match.groups()
        # If password contains unencoded '@'
        if "@" in pwd and "%40" not in pwd:
            pwd = quote_plus(pwd)
            return f"{prefix}{user}:{pwd}@{host}{suffix}"
    return uri


class UsageLogger:
    def __init__(self):
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=True)
        else:
            load_dotenv(override=True)

        raw_uri = os.getenv("MONGODB_URI")
        if not raw_uri:
            raise ValueError("MONGODB_URI not found in .env")

        mongo_uri = fix_mongo_uri(raw_uri)

        # Connect to configured MongoDB URI with timeout
        connected = False
        try:
            self.client = MongoClient(
                mongo_uri,
                serverSelectionTimeoutMS=3000,
                connectTimeoutMS=3000,
                socketTimeoutMS=5000,
                retryWrites=True
            )
            self.client.admin.command("ping")
            connected = True
        except Exception:
            pass

        if not connected:
            # Fallback to local MongoDB instance
            try:
                local_client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
                local_client.admin.command("ping")
                self.client = local_client
                print("[Info] Atlas connection failed; connected to local MongoDB.")
                connected = True
            except Exception as local_err:
                raise RuntimeError(
                    "Could not connect to MongoDB Atlas or local MongoDB. "
                    "Ensure MongoDB is running or add your IP to Atlas Network Access."
                ) from local_err

        db = self.client["llm_monitoring"]
        self.collection = db["api_usage"]

    def log_call(self, record):
        # Work on a copy so the caller's dictionary is not changed
        document = dict(record)
        document["timestamp"] = datetime.now(timezone.utc)

        for attempt in range(3):
            try:
                self.collection.insert_one(document)
                print("Usage details saved to MongoDB.")
                return True
            except PyMongoError as error:
                print(f"MongoDB write attempt {attempt + 1} failed: {error}")
                if attempt < 2:
                    time.sleep(2 ** attempt)

        print("Warning: usage record could not be saved.")
        return False

    def close(self):
        self.client.close()
