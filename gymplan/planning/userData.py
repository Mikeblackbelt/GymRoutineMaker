import uuid
import json
import sys
import os

sys.path.append(os.path.abspath(r'C:\Users\mike.mat\Desktop\GymRoutineMaker'))

import gymplan.utility.filePaths as fp
import gymplan.utility.mergeJson as mj

#fpUserJson()
class User():
    def __init__(self,name,goal,daysPerWeek,uid=None) -> None:
        self.id = str(uuid.uuid4()) if uid is None else uid
        self.name = name
        self.goal = goal
        self.daysPerWeek = daysPerWeek
        mj.logToFile('userLogs.txt', f'\n{self.id} created')

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "goal": self.goal,
            "daysPerWeek": self.daysPerWeek
        }

    def upload(self) -> None:
        try:
            with open(fp.fpUserJson(), "r") as f:
                users = json.load(f)
        except FileNotFoundError:
            users = {}

        users[self.id] = self.to_dict()
        mj.logToFile('userLogs.txt', f'\n{self.id} uploaded with userdata:\n\n{users[self.id]}')

        with open(fp.fpUserJson(), "w") as f:
            json.dump(users, f, indent=4)

def getUserData(id=None, name= None) -> dict:
    if id is None and name is None:
        raise Exception('Atleast one input is required')
    elif id is not None:
        with open(fp.fpUserJson(), "r") as f:
                users = json.load(f)
        if id in users: return users[id]
        else: raise Exception("User not found")
    else:
        values = users.values()
        data = list(filter(lambda values: values['name'] == 'dev',values))
        if len(data) > 1: raise Exception('Multiple users with same name')
        else: return data[0]


testUser = User('test','A',5)
print(getUserData(str(1)))