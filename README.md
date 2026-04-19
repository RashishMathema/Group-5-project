# JobPrep Companion

JobPrep Companion is a lightweight LLM chatbot prototype aligned with the group proposal for **MSAI-631-B01**. It implements the MVP described in the proposal: interview preparation, resume bullet rewriting, and checklist generation, using explicit text commands and a simple Gradio interface.

This starter version is designed to be:
- free-resource friendly
- easy to run locally
- easy to deploy to Hugging Face Spaces
- structured enough for a class demo and group extension

## Implemented MVP Features

### 1) Interview Preparation Mode
- Generate role-relevant interview questions
- Include behavioral prompts
- Encourage STAR-style practice
- Support basic mock interview flow foundations

### 2) Resume Bullet Rewriter Mode
- Rewrite bullets to align with a job description
- Improve clarity and action language
- Avoid invented metrics or fabricated experience
- Suggest placeholders for missing details

### 3) Checklist Generator Mode
- Create structured job application checklists
- Create interview-preparation checklists
- Include short prep plans when requested

### Usability Essentials
- `help` command
- `reset` command
- explicit mode switching
- fallback guidance when inputs are unclear

## Project Structure

```text
jobprep_companion/
├── app.py
├── requirements.txt
├── README.md
└── jobprep_companion/
    ├── __init__.py
    ├── bot.py
    ├── inference.py
    ├── prompts.py
    └── state.py
```

## Commands

- `help`
- `reset`
- `mode: interview`
- `mode: resume`
- `mode: checklist`

## Local Run

```bash
python -m venv .venv
source .venv/bin/activate     # macOS/Linux
# .venv\Scripts\activate      # Windows
pip install -r requirements.txt
python app.py
```

## Hugging Face Spaces Notes

Use **Gradio** as the Space SDK. Keep `app.py` at the repository root and include `requirements.txt` so the Space installs dependencies automatically.

You can optionally set environment variables:

- `MODEL_NAME` (default: `google/flan-t5-base`)
- `MAX_NEW_TOKENS` (default: `384`)

## Suggested Next Improvements

1. Add a curated retrieval file for more grounded interview advice.
2. Add stronger output templates per mode.
3. Add an evaluation script for the 10-prompt test suite from the proposal.
4. Add a one-question-at-a-time mock interview state machine.
5. Add unit tests for command parsing and mode behavior.

## Notes for Your Group Report

This code directly follows the proposal scope by:
- using Python, Gradio, and Transformers
- supporting the three MVP modes
- avoiding paid APIs
- preserving a lightweight architecture suitable for local or hosted execution

