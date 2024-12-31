from dotenv import load_dotenv
import os

load_dotenv()

ASYNC_SQLALCHEMY_DATABASE_URL = os.getenv("ASYNC_SQLALCHEMY_DATABASE_URL")
SYNC_SQLALCHEMY_DATABASE_URL = os.getenv("SYNC_SQLALCHEMY_DATABASE_URL")




