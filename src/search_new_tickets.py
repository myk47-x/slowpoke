from .config import GLPI_URL
import os

def escavate_tickets(cli):
    headers = {
            "Authorization" : f"Bearer {os.environ["BEARER"]}"
    }
    params = {
        "sort" : "id:desc",
        "filter" :"status:id!=6"
    }
    return cli.client.get(f"{GLPI_URL}Assistance/Ticket", headers=headers,params=params).json()[0]
