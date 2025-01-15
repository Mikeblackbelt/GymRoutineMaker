import uuid
import json
import bcrypt
import sys
import os

sys.path.append(os.path.abspath(r'C:\Users\mike.mat\Desktop\GymRoutineMaker'))
import gymplan.utility.filePaths as fp
import gymplan.utility.mergeJson as mj

#chatgpt refactored

def _load_users() -> dict:
    try:
        with open(fp.fpUserJson(), "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

defaultSettings = {
    '2auth': False,
    'dark_mode': False,
    'privacy_settings': {
        'logEmail': False,
    } 
} #subj to change
class User:
    def __init__(self, name: str, username: str, password: str, *, email: str = None, uid: str = None, routines: dict = None, settings: dict = defaultSettings) -> None:
        users = _load_users()
        if any(user['username'] == username for user in users.values()):
            raise ValueError("Username already exists, please choose a different one")
        self.id = str(uuid.uuid4()) if uid is None else uid
        self.name = name
        self.username = username
        self.password = self._hash_password(password)
        self.email = email
        self.routines = routines or []
        self.settings = settings or defaultSettings
        mj.logToFile('userLogs.txt', f'\n{self.id} created')

    @staticmethod
    def _hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "routines": self.routines,
            "settings": self.settings
        }

    def upload(self) -> None:
        users = _load_users()
        users[self.id] = self.to_dict()
        mj.logToFile('userLogs.txt', f'\n{self.id} uploaded with userdata:\n\n{users[self.id]}')
        with open(fp.fpUserJson(), "w") as f:
            json.dump(users, f, indent=4)


def getUserData(*, id: str = None, name: str = None, username: str = None) -> dict:
    users = _load_users()
    if id:
        user = users.get(id)
        if user:
            return user
        raise ValueError("User not found with the given ID")
    if username:
        user = next((user for user in users.values() if user['username'] == username), None)
        if user:
            return user
        raise ValueError("User not found with the given username")
    if name:
        matches = [user for user in users.values() if user['name'] == name]
        if len(matches) > 1:
            raise ValueError("Multiple users with the same name")
        if matches:
            return matches[0]
        raise ValueError("User not found with the given name")
    raise ValueError("At least one identifier (id, name, username) is required")

def update_settings(new_settings: dict, *, id: str = None, name: str = None, username: str = None ) -> None:
    if not any([id,name,username]):
        raise ValueError("At least one identifier (id, name, username) is required")
    if id:
        userdata = getUserData(id=id)
    elif username:
        userdata = getUserData(username=username)
    else:
        userdata = getUserData(name=name)
    
    
    fullUD = _load_users()
    userid = next((key for key, value in fullUD.items() if value == userdata),None) if not id else id
    userdata['settings'] = new_settings
  
    fullUD[userid] = userdata
    
    with open(fp.fpUserJson(), "w") as f:
         json.dump(fullUD, f, indent=2)
    
def update_UD(new_data: dict, *, id: str = None, name: str = None, username: str = None ) -> None:
    if not any([id,name,username]):
        raise ValueError("At least one identifier (id, name, username) is required")
    if id:
        userdata = getUserData(id=id)
    elif username:
        userdata = getUserData(username=username)
    else:
        userdata = getUserData(name=name)
    
    fullUD = _load_users()
    userid = next((key for key, value in fullUD.items() if value == userdata),None) if not id else id
    userdata = new_data
  
    fullUD[userid] = userdata
    
    with open(fp.fpUserJson(), "w") as f:
         json.dump(fullUD, f, indent=2)

def hauth2(username: str, password: str) -> bool:
    users = _load_users()
    for user in users.values():
        if user['username'] == username:
            return bcrypt.checkpw(password.encode(), user['password'].encode())
    raise ValueError("Username not found")

if __name__ == "__main__":
    update_settings({
            "2auth": False,
            "dark_mode": True,
            "privacy_settings": {
                "logEmail": True
            }
        },
        username = 'AdminAdmin')