import os

# Model-agnostic LLM provider selection (set in .env or environment)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # e.g., openai, anthropic, gemini
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")  # e.g., gpt-3.5-turbo, claude-4, etc. 