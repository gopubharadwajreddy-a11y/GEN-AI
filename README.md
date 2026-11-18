# GEN-AI Coursework & Labs

This repository contains weekly assignments, lab exercises, and experiments for the Generative AI curriculum.

## Repository Overview

- **`week1/`**: Introduction to generative models and initial Gemini API client setup.
- **`week-2/`**: LLM client implementation, response handling, and unit testing.
- **`Week3/`**: LLM client enhancements with token usage logging and MongoDB persistence.
- **`Week4/`**: Tokenizer analysis and comparison across different architectures.
- **`Week5/`**: Token budget estimation, cost calculation, and rate limiting simulations.
- **`week6/`**: LLM evaluation benchmark using a golden dataset and baseline metrics comparison.
- **`week7/`**: Interactive Lab: Next-Token Probabilities, Logits & Decoding using GPT-2.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/gopubharadwajreddy-a11y/GEN-AI.git
   cd GEN-AI
   ```

2. **Environment Configuration:**
   For weekly assignments requiring API keys or database connections (such as `week1`, `week-2`, `Week3`, and `Week5`):
   - Copy `.env.example` to `.env` in the respective folder:
     ```bash
     cp week1/.env.example week1/.env
     ```
   - Populate `.env` with your actual API keys and credentials.

3. **Install Dependencies:**
   Navigate to any module/week directory and install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
