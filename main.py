from src.glpi_session import *
from dotenv import load_dotenv
from src.search_new_tickets import escavate_tickets

import peewee


with NewClient() as base_client:

    base_client.authenticate(f"{GLPI_URL}token")
    load_dotenv(override=True)

    escavate_tickets(base_client)




#print(escavate_tickets(glpi))


"""

with httpx.Client() as glpi:
    load_newest_tickets(glpi, 20, asc) > 
        seria tipo isso no main
"""
