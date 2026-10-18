from src.glpi_session import *
from dotenv import load_dotenv
from src.search_new_tickets import escavate_tickets

glpi  = NewClient()

req = glpi.authenticate("https://ti.adubosreal.com.br/api.php/v2.3/token")
load_dotenv(override=True)
print(escavate_tickets(glpi))

"""

with httpx.Client() as glpi:
    load_newest_tickets(glpi, 20, asc) > 
        seria tipo isso no main
"""
