import os
import yaml

# Try to load config from config.yaml if it exists
CONFIG_FILE = "config.yaml"
config_data = {}
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config_data = yaml.safe_load(f) or {}

# Model-agnostic LLM provider selection (config.yaml > env > default)
LLM_PROVIDER = (
    config_data.get("LLM_PROVIDER") or
    os.getenv("LLM_PROVIDER") or
    "openai"
)
LLM_MODEL = (
    config_data.get("LLM_MODEL") or
    os.getenv("LLM_MODEL") or
    "gpt-3.5-turbo"
)

# Example config.yaml format:
# LLM_PROVIDER: openai
# LLM_MODEL: gpt-3.5-turbo 