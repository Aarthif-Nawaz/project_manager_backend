from pymongo import MongoClient
from bson.objectid import ObjectId

host = "mongodb+srv://admin:1234@cluster0.0kgm7.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
db_name = 'impact'
db = MongoClient(host)[db_name]

def stringify_object_id(obj):
    if type(obj) is list:
        [stringify_object_id(o) for o in obj]
    elif type(obj) is dict:
        for k in obj:
            if type(obj[k]) is ObjectId:
                obj[k] = str(obj[k])
            else:
                stringify_object_id(obj[k])

def signup(user):
    get_new_user = get_user(user['email'])
    if get_new_user is None:
        return str(db.users.insert_one({
            'name': user['name'],
            'email': user['email'],
            'password': user['password']
        }).inserted_id)
    else:
        return "Email Exists"


def get_user(email):
    user = db.users.find_one({'email': email})
    if user:
        return dict(user)
    else:
        return None


def login(user):
    get_new_user = get_user(user['email'])
    if get_new_user is not None:
        if get_new_user['password'] == user['password']:
            return "Success"
        else:
            return "Wrong Password"
    else:
        return "No such email exists"



def addProject(project):
    return str(db.projects.insert_one({
        'email': project['email'],
        'name': project['name'],
        'description': project['description'],
        'worktypes': project['worktypes'],
        'contractors': project['contractors'],
        'users': project['users'],
    }).inserted_id)

def get_projects(email):
    projects = list(db.projects.find({'email': email}))
    stringify_object_id(projects)
    if projects:
        return projects
    else:
        return None