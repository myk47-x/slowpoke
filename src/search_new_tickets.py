from .config import GLPI_URL
import os

def escavate_tickets(cli):
    headers = {
            "Authorization" : f"Bearer {os.environ["BEARER"]}"
    }
    params = {
        "sort" : "id:desc"
    }
    return cli.client.get(f"{GLPI_URL}Project", headers=headers,params=params).json()
