import pymongo
from bson import ObjectId

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["fproject"]


# ------------ data for user ------------
def set_user_to_server(userdata):
    mycol = mydb["user"]
    x = mycol.insert_one(userdata)
    print(x)


def get_user_to_server(username):
    mycol = mydb["user"]
    for x in mycol.find({}, {"_id": 1, "username": 1, "useremail": 1}):
        if x.get("username") == username:
            return x.get("_id")


def change_some(username, some, somedetails):
    mycol = mydb["user"]
    for x in mycol.find({}, {"_id": 0, "username": 1, "name": 1, "lastname": 1, "useremail": 1, "age": 1,
                             "userpassword": 1, "usercity": 1}):
        if x.get("username") == username:
            myquery = {some: x.get(some)}
            newvalues = {"$set": {some: somedetails}}
            mycol.update_one(myquery, newvalues)
            print("the ", some, "change to ", somedetails)
    # for x in mycol.find():
    #     print(x)


# ------------ data for team ------------

def get_team_to_server(team):
    mycol = mydb["team"]
    for x in mycol.find({}, {"_id": 1}):
        if x.get("teamid") == team:
            return x.get("_id")


def create_team(team_name, username):
    mycol = mydb["team"]

    team = {
        "teamname": team_name,
        "users": [],
        "manager": username
    }
    team["users"].append(username)
    x = mycol.insert_one(team)
    print(x.inserted_id)
    mycol = mydb["user"]
    _id = get_user_to_server(username)
    print(type(x.inserted_id))
    print(type(_id))
    mycol.update_one({'_id': _id}, {'$push': {'teams': x.inserted_id}})


def add_user_to_team(username, team):
    mycol = mydb["team"]
    oid2 = ObjectId(team)
    print(oid2)
    x = mycol.update_one({'_id': oid2}, {'$push': {'users': username}})


def set_task(team, username, task):
    mycol = mydb["team"]
    # print(mycol["tasks"])
    oid2 = ObjectId(team)
    mycol.update_one({'_id': oid2},
                     {'$push': {'tasks': {"_ID": ObjectId(), "username": username, "task": task, "done": False}}})


def finish_task(teamid, taskid):
    oid1 = ObjectId(teamid)
    oid2 = ObjectId(taskid)
    mycol = mydb["team"]
    mycol.update_one({"_id": oid1, "tasks._ID": oid2}, {"$set": {"tasks.$.done": True}})


if __name__ == '__main__':
    # test: set new task
    task = "go shopping "
    # set_task("63b2cdcc8fc4e9d0bd870068", "gadsh", task)

    # test:change something in user data
    # change_some("avivi", "lastname", "levi")

    userdata = {
        "username": "gadsh",
        "name": "gad",
        "lastname": "shrim",
        "useremail": "gadsh@gmail.com",
        "age": "30",
        "userpassword": "11223344",
        "usercity": "Gilo",
        "teams": []
    }
    # username = "amitush"
    # set_user_to_server(userdata)

    # test: create new team
    # create_team("besty", "gadsh")

    # add user to your team
    # add_user_to_team("amitush", "63b2cdcc8fc4e9d0bd870068")

    finish_task("63b2cdcc8fc4e9d0bd870068", "63b2cf3da64ce445adc94d0e")
