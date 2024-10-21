import uuid
import json
import gymplan.utility.filePaths as fp
#fpUserJson()
class User():
    def __init__(id,name,goal,daysPerWeek):
        self.id = str(uuid.uuid4())
        self.name = name
        self.goal = goal
        self.daysPerWeek = daysPerWeek

    def to_dict(self):
        return {
            "name": self.name,
            "goal": self.goal,
            "daysPerWeek": self.daysPerWeek
        }

    def uploadUser(self):
        file_path = fp.fpUserJson()
        try:
            with open(file_path, "r") as f:
                users = json.load(f)
        except FileNotFoundError:
            users = {}

        users[self.id] = self.to_dict()

        with open(file_path, "w") as f:
            json.dump(users, f, indent=4)


        