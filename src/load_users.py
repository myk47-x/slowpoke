from src.config.settings import GLPI_URL
from src.config.models import User


def escavate_users(client, params=None, notify=False): #params are not mandatory
    req = client.get(f"{GLPI_URL}Administration/User", params)
    created_users: int = 0
    for i in req:
        try:
            user, created = User.get_or_create(
                user = int(i["id"]), defaults={
                    "user_name" : str.title(f"{i['firstname']} {i['realname']}"),
                    "user_email" : i["username"]
                }
            )
            if created:
                created_users += 1
                # if notify==True:
                    # notify()
        except Exception as e:
            print("error on new user flow", e)
    print(f"{created_users} created users")




