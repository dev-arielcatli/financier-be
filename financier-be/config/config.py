from dotenv import load_dotenv

load_dotenv()

import os

# ENVIRONMENT FILES
APP_NAME = os.getenv("APP_NAME", "financier")
STAGE = os.getenv("STAGE", "test")

DIR_FUNCTIONS = "functions"

# LAMBDA NAMES
LAMBDA_FASTAPI = "fastapi_lambda"
