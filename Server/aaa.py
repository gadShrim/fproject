import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb+srv://erez116:v32VxFnUU3reEhZF@atlascluster.oncqmoe.mongodb.net/?retryWrites=true&w=majority")
# db = client.test
db = client["fproject"]

userdata = {
    "username": "gadsh",
    "name": "gad",
    "lastname": "shrim",
    "useremail": "gadsh@gmail.com",
    "age": "30",
    "userpassword": "11223344",
    "usercity": "Ashdod",
    "teams": []
}

mycol = db["team"]

