import cmd
import datetime
import pymongo
from bson import ObjectId

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
client = pymongo.MongoClient(
    "mongodb+srv://gad:Aa12345678@atlascluster.oncqmoe.mongodb.net/?retryWrites=true&w=majority")
mydb = client.fproject


# mydb = myclient["fproject"]


# ------------------------ data for user ------------------------
def set_user_to_server(userdata):
    mycol = mydb["user"]
    mycol.insert_one(userdata)


def get_user_from_server(username):
    mycol = mydb["user"]
    for x in mycol.find({},
                        {"_id": 1, "username": 1, "name": 1, "lastname": 1, "useremail": 1, "age": 1, "usercity": 1}):
        if x.get("useremail") == username:
            return x


def get_all_user_from_server():
    mycol = mydb["user"]
    all = []
    for x in mycol.find({},
                        {"_id": 1, "username": 1, "name": 1, "lastname": 1, "useremail": 1, "age": 1, "usercity": 1}):
        all.append(x.get("username"))

    return all


def get_userid_from_server(username):
    mycol = mydb["user"]
    for x in mycol.find({},
                        {"_id": 1, "username": 1, "name": 1, "lastname": 1, "useremail": 1, "age": 1, "usercity": 1}):
        if x.get("username") == username:
            print(f"get id {x.get('_id')}")
            return x.get("_id")


def username_availble(username):
    mycol = mydb["user"]
    for x in mycol.find({}, {"_id": 0, "username": 1}):
        if x.get("username") == username:
            return False
    return True


def change_some(username, some, somedetails):
    mycol = mydb["user"]
    for x in mycol.find({},
                        {"username": 1, "name": 1, "lastname": 1, "useremail": 1, "age": 1,
                         "usercity": 1}):
        if x.get("username") == username:
            myquery = {some: x.get(some)}
            newvalues = {"$set": {some: somedetails}}
            mycol.update_one(myquery, newvalues)
            print("the ", some, "change to ", somedetails)
    # for x in mycol.find():
    #     print(x)


def change_password(username, oldpassword, newpassword):
    mycol = mydb["user"]
    pas = "userpassword"
    for x in mycol.find({},
                        {"username": 1, "userpassword": 1}):
        if x.get("username") == username:
            if x.get("userpassword") == oldpassword:
                myquery = {pas: x.get(pas)}
                newvalues = {"$set": {pas: newpassword}}
                mycol.update_one(myquery, newvalues)
                print("the ", pas, "change to ", newpassword)


def user_authentication(useremail):
    mycol = mydb["user"]
    for x in mycol.find({},
                        {"_id": 1, "username": 1, "useremail": 1, "userpassword": 1}):
        if x.get("useremail") == useremail:
            return x


# ------------------------ data for team ------------------------

def create_team(team_name, _id):
    mycol = mydb["team"]
    team = {
        "teamname": team_name,
        "users": [],
        "manager": _id,
        "tasks": []
    }
    team["users"].append(_id)
    x = mycol.insert_one(team)
    mycol = mydb["user"]
    mycol.update_one({'_id': _id}, {'$push': {'teams': x.inserted_id}})
    teamid = x.inserted_id
    return teamid


def get_teams_from_userid(userid):
    mycol = mydb["user"]
    for x in mycol.find({}, {"_id": 1, "teams": 1}):
        if x.get("_id") == userid:
            return x.get("teams")


def team_name_from_teamid(teamid):
    mycol = mydb["team"]
    teamname = []
    for x in mycol.find({}, {"_id": 1, "teamname": 1}):
        for y in teamid:
            # print(f"y is: {y} type of y {type(y)}")
            # print(f"x is: {x} type of x {type(x)}")
            if x.get("_id") == y:
                teamname.append(x)
    for x in teamname:
        x["_id"] = str(x["_id"])
    return teamname


def get_team_from_server(teamid):
    mycol = mydb["team"]
    for x in mycol.find({}, {"_id": 1}):
        if x.get("teamid") == teamid:
            return x


def add_user_to_team(username, teamid):
    mycol = mydb["team"]
    _id = get_userid_from_server(username)
    print(f"add user to team: team id = {teamid} type of team is {type(teamid)}")
    print(f"add user to team: user id = {_id} type of user is {type(_id)}")

    mycol.update_one({'_id': teamid}, {'$push': {'users': _id}})


# ------------------------ data for tasks ------------------------

def get_tasks(teamid):
    mycol = mydb["team"]
    for x in mycol.find({}, {"_id": 1, "tasks": 1}):
        if x.get("_id") == teamid:
            print(f"the tasks in team id: {teamid} is : {x.get('tasks')}")
            return x.get("tasks")


def set_task(teamid, userid, title, description, fdate=None):
    mycol = mydb["team"]
    oid2 = ObjectId(teamid)
    sdate = str(fdate)
    print(title)
    _ID = ObjectId()
    # task = {
    #     "_ID": _ID,
    #     "userid": userid,
    #     "title": title,
    #     "task": description,
    #     "done": False,
    #     "date": sdate
    #
    # }
    # mycol.update_one({'_id': oid2}, {'$push': {'tasks': task}})
    mycol.update_one({'_id': oid2},
                     {'$push': {
                         'tasks': {"_ID": _ID, "userid": userid, "title": title, "task": description,
                                   "done": False, "date": sdate}}})
    return _ID


def finish_task(teamid, taskid, userid):
    oid1 = ObjectId(teamid)
    oid2 = ObjectId(taskid)
    _id = ObjectId(userid)
    mycol = mydb["team"]
    cdate = datetime.date.today()
    current_date = str(cdate)
    mycol.update_one({"_id": oid1, "tasks._ID": oid2}, {"$set": {"tasks.$.done": True}})
    mycol.update_one({"_id": oid1, "tasks._ID": oid2}, {"$set": {"tasks.$.fdate": current_date}})
    mycol.update_one({"_id": oid1, "tasks._ID": oid2}, {"$set": {"tasks.$.ftask": _id}})
    return "Success"


def delete_task(teamid, taskid, userid):
    oid1 = ObjectId(teamid)
    oid2 = ObjectId(taskid)
    # _id = userid
    mycol = mydb["team"]
    i = 0
    for team in mycol.find({},
                           {"_id": 1, "tasks": 1}):
        if team.get("_id") == oid1:
            tasks = team.get("tasks")
            print(tasks)
            for task in tasks:
                print(type(task))
                if task["_ID"] == oid2:
                    tasks.pop(i)
                    print(tasks)
                    break
                i = i + 1
            mycol.update_one({'_id': oid1}, {'$set': {'tasks': tasks}})
    return "Success"


# ------------------------ data for shoppinglist ------------------------
def get_lists(teamid):
    mycol = mydb["team"]
    for x in mycol.find({}, {"_id": 1, "shlists": 1}):
        if x.get("_id") == teamid:
            # print(f"the tasks in team id: {teamid} is : {x.get('tasks')}")
            return x.get("shlists")


def create_shopping_list(teamid, userid, title, list):
    mycol = mydb["team"]
    oid2 = ObjectId(teamid)
    _ID = ObjectId()
    mycol.update_one({'_id': oid2},
                     {'$push': {
                         'shlists': {"_ID": _ID, "userid": userid, "title": title, "list": list
                                     }}})
    return _ID


def save_shopping_list_data(teamid, userid, listid, list):
    mycol = mydb["team"]
    oid1 = ObjectId(teamid)
    listId = ObjectId(listid)
    newList=list
    print("save list to mongo",newList)
    mycol.update_one({"_id": oid1, "shlists._ID": listId}, {"$set": {"shlists.$.list": newList}})
    return "successes"


def finish_shopping_list(teamid, listid, userid):
    oid1 = ObjectId(teamid)
    oid2 = ObjectId(listid)
    mycol = mydb["team"]
    cdate = datetime.date.today()
    current_date = str(cdate)
    mycol.update_one({"_id": oid1, "shlists._ID": oid2}, {"$set": {"shlists.$.done": True, "shlists.$.fdate": current_date, "shlists.$.fshlist": userid }})
    return "Success"


def delete_shopping_list(teamid, listid):
    oid1 = ObjectId(teamid)
    oid2 = ObjectId(listid)
    # _id = userid
    mycol = mydb["team"]
    i = 0
    for team in mycol.find({},
                           {"_id": 1, "shlists": 1}):
        if team.get("_id") == oid1:
            shlist = team.get("shlists")
            print(shlist)
            for list in shlist:
                print(type(list))
                if list["_ID"] == oid2:
                    shlist.pop(i)
                    shlist.append()
                    print(shlist)
                    break
                i = i + 1
            mycol.update_one({'_id': oid1}, {'$set': {'shlists': shlist}})
    return "Success"


if __name__ == '__main__':
    delete_task("644140e5e181758853e571f2", "64580b7b818547fe8544b7e5")
