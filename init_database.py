from src.models import *
import httpx
import peewee
from src.config import *
from src.glpi_session import *
from src.parse_html import *


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
                enrolled_technician = 744
                enrolled_team = "Teste"
            )
            if created:
                created_enrollments += 1
        except IntegrityError as e:
            print("Invalid enrollment data", e)

        except Exception as e:
            print("Unkow enrollment error", e)
    print(f"{created_enrollments} enrollments created")


with NewClient() as base_client:

    base_client.authenticate(f"{GLPI_URL}token")
    load_dotenv(override=True)
    
    load_users(base_client)
    load_open_tickets(base_client)
    load_enrollments(base_client)
