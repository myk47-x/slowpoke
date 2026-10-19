import httpx
import json

from .config import *
from dotenv import set_key

class NewClient:

    def __init__(self):
        self.client = httpx.Client(timeout=10)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()

    def authenticate(self,url): #, client_id, client_secret, email, password):
        data = {
            "grant_type" : "password",
            "client_id" : GLPI_CLIENT_ID,
            "client_secret" : GLPI_CLIENT_SECRET,
            "username" : GLPI_EMAIL,
            "password" : GLPI_PASSWORD,
            "scope" : "api email user"
        }
        response = self.client.post(url, data=data)
        set_key(".env","BEARER",response.json()["access_token"])


    def get(self,url, **kw):
        headers ={
            "Authorization" : f"Bearer {os.environ["BEARER"]}",
        }
        params = kw
        response = self.client.get(url, headers=headers, params=params).json()
        return response

