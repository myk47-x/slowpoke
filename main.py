from src.glpi_client import *
from dotenv import load_dotenv
from src.search_new_tickets import escavate_tickets
from src.users_update import escavate_users

from src.config import GLPI_URL
import peewee

if __name__ == "__main__":

    with GlpiClient() as client:
        
        client.authenticate()
        escavate_tickets(base_client,{"limit" : 300, "sort" : "id:asc"})
        escavate_users(base_client)



#print(escavate_tickets(glpi))


"""

with httpx.Client() as glpi:
    load_newest_tickets(glpi, 20, asc) > 
        seria tipo isso no main
"""
