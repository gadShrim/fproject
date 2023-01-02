import pymongo
import ServerToDataBase


def check_user_name(username):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["fproject"]
    mycol = mydb["user"]
    for x in mycol.find({}, {"_id": 0, "username": 1}):
        if x.get("username") == username:
            return False
    return True


# test: if username is available
# x= check_user_name("gadshu")
# print(x)

def create_new_user(userdata):
    if check_user_name(userdata["username"]):
        ServerToDataBase.set_user_to_server(userdata)
    else:
        print("this username is not available")


dat = {
    "username": "aviviti",
    "name": "avivit",
    "lastname": "noa",
    "useremail": "avivitnol@gmail.com",
    "age": "22",
    "userpassword": "123456789",
    "usercity": "ashdod"
}
print(dat)
create_new_user(dat)
