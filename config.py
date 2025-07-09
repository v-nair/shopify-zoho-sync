import os
from dotenv import load_dotenv

# Load env vars from .env (override existing)
load_dotenv(override=True)

# Required environment variables
REQUIRED_VARS = [
    "SHOPIFY_API_URL",
    "ZOHO_API_URL",
    "SHOPIFY_ACCESS_TOKEN",
    "ZOHO_ACCESS_TOKEN",
    "ZOHO_ORG_ID",
]

for var in REQUIRED_VARS:
    if not os.getenv(var):
        raise RuntimeError(f"Missing required environment variable: {var}")

# Exported configuration values
SHOPIFY_API_URL       = os.environ["SHOPIFY_API_URL"]
ZOHO_API_URL          = os.environ["ZOHO_API_URL"]
SHOPIFY_ACCESS_TOKEN  = os.environ["SHOPIFY_ACCESS_TOKEN"]
ZOHO_ACCESS_TOKEN     = os.environ["ZOHO_ACCESS_TOKEN"]
ZOHO_ORG_ID           = os.environ["ZOHO_ORG_ID"]