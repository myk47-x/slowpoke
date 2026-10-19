def get_technician(dictionary):
    for i in dictionary["team"]:
        if i["role"] == "assigned" and i["type"] == "User":
            return i["id"]

def get_team(dictionary):
    for i in dictionary["team"]:
        if i ["role"] == "assigned" and i["type"] == "Group":
            return i["name"]
