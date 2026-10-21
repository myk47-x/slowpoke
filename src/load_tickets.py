from src.config.settings import GLPI_URL
import os
from src.utils.parse_html import html_to_text
from src.config.models import Ticket


def escavate_tickets(client, params=None, notify=False):

    req = client.get(f"{GLPI_URL}Assistance/Ticket", params)
    created_tickets: int = 0
    for i in req:
        try:
            ticket, created = Ticket.get_or_create(
                ticket = int(i["id"]), 
                defaults ={"ticket_title" : str.title(i["name"]),
                           "ticket_description" : html_to_text(i["content"])
                           }
            )
            if created:
                created_tickets += 1
                #if notify==True:
                    # notify()

        except Exception as e:
            print("insert error on tickets", e)

    print(f"{created_tickets} created new tickets")
