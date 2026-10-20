"""Load client and database configurations

INIT variables defines how much data will be queried by init database script
"""

import os
from dotenv import load_dotenv

load_dotenv()

GLPI_URL = os.getenv("GLPI_URL")
GLPI_CLIENT_ID = os.getenv("GLPI_CLIENT_ID")
GLPI_CLIENT_SECRET = os.getenv("GLPI_CLIENT_SECRET")
GLPI_EMAIL = os.getenv("GLPI_EMAIL")
GLPI_PASSWORD = os.getenv("GLPI_PASSWORD")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

INIT_USERS=1500
INIT_TICKETS=1000
INIT_ENROLLED=1000
