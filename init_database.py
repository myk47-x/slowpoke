from src.models import slowpoke_database,User,Ticket,Enrolled,Solution,Followup
import peewee
from src.glpi_client import NewClient
from src.load_users import escavate_users
from src.load_tickets import escavate_tickets
from src.load_followups import escavate_followups


slowpoke_database.connect()
slowpoke_database.create_tables([User, Ticket, Enrolled, Solution, Followup])


with NewClient() as client:

    client.authenticate()

    escavate_users(client,{"limit":1000,"sort":"id:asc"})
    escavate_tickets(client, {"limit":2000,"filter":"status.id!=6;is_deleted==false"},True)
#    load_enrollments(client)
    escavate_followups(client, {"limit" : 5000})









def load_enrollments(base_client: NewClient):
    params = {
        "limit" : INIT_ENROLLED,
        "filter" : "status.id!=6;is_deleted==false"
    }

    req = base_client.get(f"{GLPI_URL}Assistance/Ticket", params)
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




