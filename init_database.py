from src.models import *
import httpx
import peewee
from src.config import *
from src.glpi_client import *
from src.parse_html import *
from src.dict_functions import *
from src.users_update import *
from src.search_new_tickets import *

slowpoke_database.connect()
slowpoke_database.create_tables([User, Ticket, Enrolled, Solution, Followup])


with NewClient() as client:

    client.authenticate()

    escavate_users(client,{"limit":1000,"sort":"id:asc"})
    escavate_tickets(client, {"limit":2000,"filter":"status.id!=6;is_deleted==false"},True)
   # load_enrollments(base_client)
    #load_followups(base_client)



















def load_enrollments(base_client: NewClient):
    params = {
        "limit" : INIT_ENROLLED,
        "filter" : "status.id!=6;is_deleted==false"
    }

    req = base_client.get(f"{GLPI_URL}Assistance/Ticket", **params)
    created_enrollments: int = 0
    for i in req:
        try:
            enrolled, created = Enrolled.get_or_create(
                ticket = int(i["id"]),
                enrolled_requester = int(i["user_recipient"]["id"]),
                enrolled_technician = get_technician(i),
                enrolled_team = get_team(i)
            )
            if created:
                created_enrollments += 1
        except IntegrityError as e:
            print("Invalid enrollment data", e)

        except Exception as e:
            print("Unknown enrollment error", e)
    print(f"{created_enrollments} enrollments created")


def load_followups(base_client: NewClient):

    created_followups: int = 0
    query = Ticket.select()
    for ticket in query:
        req = base_client.get(f"{GLPI_URL}Assistance/Ticket/{ticket.ticket}"
        "/Timeline/Followup")

        for i in req:
            followups = {
                "ticket" : int(i["item"]["items_id"]),
                "followup" : i["item"]["id"] ,
                "followup_user" : i["item"]["user"]["id"],
                "followup_content" : html_to_text(i["item"]["content"]) 
            }
            try:
                followup, created = Followup.get_or_create(**followups)
                if created:
                    created_followups += 1
            except IntegrityError as e:
                print("Invalid followup data", e)
            except Exception as e:
                print("Unknown followup error", e)
    print(f"{created_followups} created followups")
