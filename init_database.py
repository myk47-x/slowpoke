from src.models import *
import httpx
import peewee
from src.config import *
from src.glpi_session import *


slowpoke_database.connect()
slowpoke_database.create_tables([User, Ticket, Enrolled, Solution, Followup])

#base_client = NewClient()

with NewClient() as base_client:
    def load_users():
        base_client.authenticate(f"{GLPI_URL}token")
        load_dotenv(override=True)
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
                print("Invalid data ", e)

            except Exception as e:
                print("Unknow error")

        print(f"{created_users} created users")


    load_users()


