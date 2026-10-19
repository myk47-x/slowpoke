from src.models import *
import httpx
import peewee
from src.config import *
from src.glpi_session import *
from src.parse_html import *
from src.dict_functions import *

slowpoke_database.connect()
slowpoke_database.create_tables([User, Ticket, Enrolled, Solution, Followup])


def load_users(base_client: NewClient):
    params = {"limit" : INIT_USERS}
    req = base_client.get(f"{GLPI_URL}Administration/User", **params)
    created_users: int = 0
    for i in req:
        try:
            user, created = User.get_or_create(
                user = int(i["id"]),
                user_name = str.title(f"{i['firstname']} {i['realname']}"),
                user_email = i["username"]
            )
            if created:
                created_users += 1

        except IntegrityError as e:
            print("Invalid user data ", e)

        except Exception as e:
            print("Unknow error getting user")

    print(f"{created_users} created users")


def load_open_tickets(base_client: NewClient):
    params = {"limit" : INIT_TICKETS,
              "filter" : "status.id!=6;is_deleted==false"}

    req = base_client.get(f"{GLPI_URL}Assistance/Ticket", **params)
    created_tickets: int = 0
    for i in req:
        try:
            ticket, created = Ticket.get_or_create(
                ticket = int(i["id"]),
                ticket_title = str.title(i["name"]),
                ticket_description = html_to_text(i["content"])
            )
            if created:
                created_tickets += 1

        except IntegrityError as e:
            print("Invalid ticket data ", e)

        except Exception as e:
            print("Unknow error getting ticket", e)
    print(f"{created_tickets} created tickets")


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
            print("Unkow enrollment error", e)
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
                print("Unknow followup error", e)
    print(f"{created_followups} created followups")




with NewClient() as base_client:

    base_client.authenticate(f"{GLPI_URL}token")
    load_dotenv(override=True)
    
    load_users(base_client)
    load_open_tickets(base_client)
    load_enrollments(base_client)
    load_followups(base_client)
