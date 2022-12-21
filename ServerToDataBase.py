import pymongo


def set_user_to_server(userdata):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["fproject"]
    mycol = mydb["user"]
    x = mycol.insert_one(userdata)
    print(x)


def get_user_to_server(username):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["fproject"]
    mycol = mydb["user"]
    for x in mycol.find({}, {"_id": 0, "username": 1, "useremail": 1}):
        print(x)
    if x.get("username") == username:
        return x.get("useremail")


def change_some(username, some, somedetails):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["fproject"]
    mycol = mydb["user"]
    for x in mycol.find({}, {"_id": 0, "username": 1, "name": 1, "lastname": 1, "useremail": 1, "age": 1,
                             "userpassword": 1, "usercity": 1}):
        if x.get("username") == username:
            myquery = {some: x.get(some)}
            newvalues = {"$set": {some: somedetails}}
            mycol.update_one(myquery, newvalues)
    for x in mycol.find():
        print(x)

# test:change something in user data
# change_some("avivi", "lastname", "alush")

userdata = {
    "username": "gadsh",
    "name": "gad",
    "lastname": "shrim",
    "useremail": "gadsh@gmail.com",
    "age": "30",
    "userpassword": "11223344",
    "usercity": "Gilo"
}
username = "amitush"
set_user_to_server(userdata)
# a = "63a1aa200226d52f5a92364c"
# print(y)
