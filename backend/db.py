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
        db.users.insert_one({
            'name': user['name'],
            'email': user['email'],
            'password': user['password']
        })
        db.Notifications.insert_one({
            'email': user['email']
        })
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


def addImage(Image):
    return str(db.Images.insert_one({
        'project_id': ObjectId(Image['id']),
        'image': Image['image']
    }).inserted_id)


def addProject(project):
    return str(db.projects.insert_one({
        'email': project['email'],
        'name': project['name'],
        'description': project['description'],
        'worktypes': project['worktypes'],
        'contractors': project['contractors'],
        'users': project['users'],
    }).inserted_id)


def get_projects(email=None, id=None, user=None):
    projects = []
    if email:
        projects = list(db.projects.find({'email': email}))
    if user:
        projects = list(db.projects.find({'users': {"$in": [user]}}))
    if id:
        projects = dict(db.projects.find_one({'_id': ObjectId(id)}))
    stringify_object_id(projects)
    if projects:
        return projects
    else:
        return None


def get_images(id=None, project_id=None):
    Images = []
    if project_id:
        Images = list(db.Images.find({'project_id': ObjectId(project_id)}))
    if id:
        Images = dict(db.Images.find_one({'_id': ObjectId(id)}))
    stringify_object_id(Images)
    if Images:
        return Images
    else:
        return None


def update_project(project):
    query = {}
    if 'name' in project:
        query['name'] = project['name']
    if 'description' in project:
        query['description'] = project['description']
    if 'worktypes' in project:
        query['worktypes'] = project['worktypes']
    if 'contractors' in project:
        query['contractors'] = project['contractors']
    if 'users' in project:
        query['users'] = project['users']

    return db.projects.update(
        {
            '_id': ObjectId(project['_id'])
        },
        {
            '$set': query

        }
    )


def update_image(project):
    return db.Images.update(
        {
            '_id': ObjectId(project['_id'])
        },
        {
            '$push': {
                'worktype': project['worktype'],
                'contractor': project['contractor'],
                'description': project['description'],
                'elements': project['elements']
            }
        }
    )


def delete_project(project):
    return db.projects.delete_one({
        '_id': ObjectId(project['_id'])
    })


def updateNotification(project):
    return db.Notifications.update(
        {
            'email': project['email']
        },
        {
            '$push': {
                'notifications': project['notification']
            }
        }
    )


def getNotification(project):
    notifications = dict(db.Notifications.find_one({'email': project['email']}))
    stringify_object_id(notifications)
    if notifications:
        return notifications
    return None
