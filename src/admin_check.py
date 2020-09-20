import json


def check_admin(user):
    with open("config.json", 'r') as file:
        ADMINS = json.load(file)['administrators']

    if user in ADMINS:
        return True
    else:
        return False
