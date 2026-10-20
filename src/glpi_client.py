"""Minimal httpx client to interact with GLPI

client.authenticate() generates Bearer token utilizing GLPI OAuth2 with
password. Scoped to user, email and api

client.get() does a request to the specified endpoint and returns dict of json

__enter__ and __exited__ implemented to context manager use
"""

import httpx
import json
import os
from .config import GLPI_CLIENT_ID, GLPI_CLIENT_SECRET, GLPI_EMAIL, GLPI_PASSWORD, GLPI_URL
from dotenv import set_key, load_dotenv
from typing import Any

class NewClient:

    def __init__(self):
        self.client = httpx.Client(timeout=10)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()

    def authenticate(self): 
        """Do post request to GLPI token endpoint to receive Bearer header

        configuration values should be defined in .env file

        the generated bearer token is stored is also stored in .env
        """
        data = {
            "grant_type" : "password",
            "client_id" : GLPI_CLIENT_ID,
            "client_secret" : GLPI_CLIENT_SECRET,
            "username" : GLPI_EMAIL,
            "password" : GLPI_PASSWORD,
            "scope" : "api email user"
        }
        response = self.client.post(f"{GLPI_URL}token", data=data)
        set_key(".env","BEARER",response.json()["access_token"])
        load_dotenv(override=True) # rewrites Bearer value on .env

    def get(self, url: str, **kw: Any):
        """Do a basic authenticated http get request with the client,
        needs url arg and accepts multiple params via function args
        """
        headers ={
            "Authorization" : f"Bearer {os.environ["BEARER"]}",
        }
        params = kw
        response = self.client.get(url, headers=headers, params=params)
        return response.json() # turns the response into dict or list of dicts

