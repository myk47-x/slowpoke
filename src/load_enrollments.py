from src.models import Enrolled
from .config import GLPI_URL
from .parse_dict import get_technician, get_team


def escavate_enrollments(client, params=None, notify=False):

    req = client.get(f"{GLPI_URL}Assistance/Ticket", params)
    updated_enrollments: int = 0
    created_enrollments = 0
    for i in req:
        try:
            enrollment = {
                "ticket" : int(i["id"]),
                "enrolled_requester" : int(i["user_recipient"]["id"]),
                "enrolled_technician" : get_technician(i),
                "enrolled_team" : get_team(i)
            }
        except Exception:
            print("kinda not ok")

        try:
            enrollment_exists = Enrolled.get_or_none(Enrolled.ticket == enrollment["ticket"])
            if enrollment_exists:
                is_same = Enrolled.get_or_none(**enrollment)
                if is_same:
                    continue
                else:
                    Enrolled.update(**enrollment).where(Enrolled.ticket == 
                                                        enrollment["ticket"]).execute()
                    updated_enrollments += 1
            else:
                Enrolled.create(**enrollment)
                created_enrollments += 1
        except Exception:
            print("not ok")
    print(f"{updated_enrollments} updated enrollments")
    print(f"{created_enrollments} created enrollments")
