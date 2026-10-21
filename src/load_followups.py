from src.config.settings import GLPI_URL
from src.config.models import Ticket, Followup
from src.utils.parse_html import html_to_text

def escavate_followups(client, params=None, notify=False):

    created_followups: int = 0
    query = Ticket.select()
    for ticket in query:
        req = client.get(f"{GLPI_URL}Assistance/Ticket/{ticket.ticket}"
                         "/Timeline/Followup", params)

        for i in req:
            followups = {
                "ticket" : int(i["item"]["items_id"]),
                "followup" : i["item"]["id"],
                "followup_user" : i["item"]["user"]["id"],
                "followup_content" : html_to_text(i["item"]["content"])
            }
            try:
                followup, created = Followup.get_or_create(**followups)
                if created:
                    created_followups += 1
                    # if notify == True:
                    # notify()
            except Exception as e:
                print("Unknown error", e)
    print(f"{created_followups} created followups")
