import datetime
import pymongo
from bson import ObjectId

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["fproject"]


# ------------------------ data for user ------------------------
def set_user_to_server(userdata):
    mycol = mydb["user"]
    mycol.insert_one(userdata)


def get_user_from_server(username):
    mycol = mydb["user"]
    for x in mycol.find({},
                        {"_id": 1, "username": 1, "name": 1, "lastname": 1, "useremail": 1, "age": 1, "usercity": 1}):
        if x.get("username") == username:
            return x


def get_userid_from_server(username):
    mycol = mydb["user"]
    for x in mycol.find({},
                        {"_id": 1, "username": 1, "name": 1, "lastname": 1, "useremail": 1, "age": 1, "usercity": 1}):
        if x.get("username") == username:
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
                         "userpassword": 0, "usercity": 1}):
        if x.get("username") == username:
            myquery = {some: x.get(some)}
            newvalues = {"$set": {some: somedetails}}
            mycol.update_one(myquery, newvalues)
            print("the ", some, "change to ", somedetails)
    # for x in mycol.find():
    #     print(x)


# ------------------------ data for team ------------------------

def create_team(team_name, username):
    mycol = mydb["team"]
    _id = get_userid_from_server(username)
    team = {
        "teamname": team_name,
        "users": [],
        "manager": _id
    }
    team["users"].append(_id)
    x = mycol.insert_one(team)
    mycol = mydb["user"]
    mycol.update_one({'_id': _id}, {'$push': {'teams': x.inserted_id}})


def get_team_from_server(teamid):
    mycol = mydb["team"]
    for x in mycol.find({}, {"_id": 1}):
        if x.get("teamid") == teamid:
            return x


def add_user_to_team(username, teamid):
    mycol = mydb["team"]
    oid2 = ObjectId(teamid)
    _id = get_userid_from_server(username)
    mycol.update_one({'_id': oid2}, {'$push': {'users': _id}})


# ------------------------ data for tasks ------------------------


def set_task(teamid, username, task, date=None):
    mycol = mydb["team"]
    oid2 = ObjectId(teamid)
    sdate = str(date)
    mycol.update_one({'_id': oid2},
                     {'$push': {'tasks': {"_ID": ObjectId(), "username": username, "task": task, "done": False,
                                          "date": sdate}}})


def finish_task(teamid, taskid, username):
    oid1 = ObjectId(teamid)
    oid2 = ObjectId(taskid)
    mycol = mydb["team"]
    cdate = datetime.date.today()
    current_date = str(cdate)
    _id = get_userid_from_server(username)
    mycol.update_one({"_id": oid1, "tasks._ID": oid2}, {"$set": {"tasks.$.done": True}})
    mycol.update_one({"_id": oid1, "tasks._ID": oid2}, {"$set": {"tasks.$.fdate": current_date}})
    mycol.update_one({"_id": oid1, "tasks._ID": oid2}, {"$set": {"tasks.$.ftask": _id}})


# ------------------------ data for shoppinglist ------------------------
def create_shopping_list(teamid, username, products, date=None):
    mycol = mydb["team"]
    oid2 = ObjectId(teamid)
    sdate = str(date)
    mycol.update_one({'_id': oid2},
                     {'$push': {'shlists': {"_ID": ObjectId(), "username": username, "products": products, "done": False,
                                           "date": sdate}}})


def finish_shopping_list(teamid, listid, username):
    oid1 = ObjectId(teamid)
    oid2 = ObjectId(listid)
    mycol = mydb["team"]
    cdate = datetime.date.today()
    current_date = str(cdate)
    _id = get_userid_from_server(username)
    mycol.update_one({"_id": oid1, "tasks._ID": oid2}, {"$set": {"shlists.$.done": True}})
    mycol.update_one({"_id": oid1, "tasks._ID": oid2}, {"$set": {"shlists.$.fdate": current_date}})
    mycol.update_one({"_id": oid1, "tasks._ID": oid2}, {"$set": {"shlists.$.fshlist": _id}})

def all_products():
    mycol = mydb["team"]
    myprod = mydb["all_products"]
    prod = myprod.find()
    for x in mycol.find({},
                        {"teamname": 1, "manager": 1, "shlist": 1}):
        p = x['shlist'][0]['products']
        for i in p:
            for j in prod:
                if j == i:
                    break


if __name__ == '__main__':
    # test: set new task
    # task = "shopping "
    # date = datetime.date(2018, 5, 12)
    # print(date)
    # print(type(date))
    # set_task("63b2cdcc8fc4e9d0bd870068", "gadsh", task)
    # test:change something in user data
    # change_some("aviviti", "lastname", "lev")

    products = {
        "חלב": "1",
        "לחם": "2",
        "גבינה": "6"
    }
    teamid = "63b41d1edd3902090a55ef80"
    # create_shopping_list(teamid, "gadsh", products)
    # all_products()
