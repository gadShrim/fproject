import time
import pymongo
from ServerToDataBase import *
import datetime
from flask import *
import json
import re
from validate_email import validate_email
import requests

# ------------------------ data for user ------------------------
app = Flask(__name__)


def check_email(email):
    # regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # if (re.fullmatch(regex, email)):
    #     return True
    # else:
    #     return False
    email_address = email
    response = requests.get(
        "https://isitarealemail.com/api/email/validate",
        params={'email': email_address})
    status = response.json()['status']
    if status == "valid":
        return True
    return False


def check_data(data):
    send = "The rep is incorrect, please change it"
    if not check_user_name(data["username"]):
        return send.replace('rep', 'username')
    if not data['name'].isalpha():
        return send.replace('rep', 'name')
    elif not data['lastname'].isalpha():
        return send.replace('rep', 'lastname')
    elif not check_email(data['useremail']):
        return send.replace('rep', 'useremail')
    elif not data['age'].isnumeric():
        return send.replace('rep', 'age')
    elif not len(data['userpassword']) > 6:
        return send.replace('rep', 'userpassword')
    elif not data['usercity'].isalpha():
        return send.replace('rep', 'usercity')
    else:
        return True


def get_user(useremail):
    return get_user_from_server(useremail)


def check_user_name(username):
    response = username_availble(username)
    return response


def change_detail(username, field, new_detail):
    if field == "name" or "lastname" or "useremail" or "age" or "usercity":
        # print(field)
        # print(new_detail)
        change_some(username, field, new_detail)
    else:
        print("the field is uncorrected")


def change_username(old_username, new_username):
    if username_availble(new_username):
        change_some(old_username, "username", new_username)
    else:
        print("the new user name is unavailable")


def change_user_password(username, oldpassword, newpassword):
    change_password(username, oldpassword, newpassword)


# ------------------------ data for team ------------------------
def new_team(team_name, userid):
    if type(userid) == str:
        userid = ObjectId(userid)
    teamid = create_team(team_name, userid)
    print(f"type of teamid in new team{type(teamid)}")
    return teamid


def get_team(teamid):
    print(get_team_from_server(teamid))


def new_user_for_team(username, teamid):
    add_user_to_team(username, teamid)


# ------------------------ data for tasks ------------------------
def get_all_tasks(teamid):
    print("hello get all tasks")
    if type(teamid) == str:
        teamid = ObjectId(teamid)
    tasks = get_tasks(teamid)
    print(f"in get_all_tasks the tasks is:{tasks} and the type of tasks is{type(tasks)}")
    return tasks


def add_new_task(data):
    teamid = data["teamid"]
    userid = data["userid"]
    title = data["title"]
    task = data["task"]
    date = data["fdate"]
    taskid = set_task(teamid, userid, title, task, date)
    return taskid


def task_completed(data):
    teamid = data["teamid"]
    taskid = data["taskid"]
    userid = data["userid"]
    return finish_task(teamid, taskid, userid)


def task_delete(data):
    teamid = data["teamid"]
    taskid = data["taskid"]
    userid = data["userid"]
    return delete_task(teamid, taskid, userid)


# ------------------------ data for shoppinglist ------------------------
def get_all_lists(teamid):
    print("hello get all lists")
    if type(teamid) == str:
        teamid = ObjectId(teamid)
    list = get_lists(teamid)
    print(f"in lists the lists is:{list} and the type of lists is{type(list)}")
    return list


def new_shopping_list(data):
    print(data)
    teamid = data["teamid"]
    userid = data["userid"]
    title = data["title"]
    list = data["list"]
    return create_shopping_list(teamid, userid, title, list)


def save_shopping_list(data):
    print("savelist", data)
    teamid = data["teamid"]
    userid = data["userid"]
    listid = data["listid"]
    list = data["list"]

    return save_shopping_list_data(teamid, userid, listid, list)


def shopping_list_completed(data):
    teamid = data["teamid"]
    listid = data["listid"]
    userid = data["userid"]
    return finish_shopping_list(teamid, listid, userid)


@app.route("/setshlist", methods=['POST'])
def createShopping():
    data = request.get_json()
    print(f"data in create-shopping list {data}")
    listid = new_shopping_list(data)
    if listid:
        return jsonify(str(listid))
    else:
        return jsonify("Failure") \
 \
            @ app.route("/saveshlist", methods=['POST'])


def saveShoppingList():
    data = request.get_json()
    print(f"data in save-shopping list {data}")
    listid = save_shopping_list(data)
    if listid:
        return jsonify(str(listid))
    else:
        return jsonify("Failure")


@app.route("/getlist", methods=['POST'])
def allLists():
    teamid = request.get_json()
    lists = get_all_lists(teamid)
    for x in lists:
        x["_ID"] = str(x["_ID"])
        if "ftask" in x:
            x["ftask"] = str(x["ftask"])

    # print(f"the task in get al tasks{tasks}")
    if lists:
        return jsonify(lists)
    else:
        return jsonify("Failure")


@app.route("/shlistcomplete", methods=['post'])
def finish():
    print("hello finish list")
    data = request.get_json()
    list = shopping_list_completed(data)
    if list:
        return jsonify(list)
    else:
        return jsonify("Failure")


@app.route("/createTeam", methods=['POST'])
def createTeam():
    data = request.get_json()
    print(data)
    teamid = new_team(data["teamName"], data["userID"])
    new_user_for_team(data["anotherUser"], teamid)
    if teamid:
        return jsonify(str(teamid))
    else:
        return jsonify("Failure")


@app.route("/getTasks", methods=['POST'])
def allTasks():
    teamid = request.get_json()
    tasks = get_all_tasks(teamid)
    for x in tasks:
        x["_ID"] = str(x["_ID"])
        if "ftask" in x:
            x["ftask"] = str(x["ftask"])

    # print(f"the task in get al tasks{tasks}")
    if tasks:
        return jsonify(tasks)
    else:
        return jsonify("Failure")


@app.route("/setTask", methods=['POST'])
def setTasks():
    print("hello set task")
    data = request.get_json()
    print(data)
    # return jsonify("hi")
    taskid = add_new_task(data)
    if taskid:
        return jsonify(str(taskid))
    else:
        return jsonify("Failure")


@app.route("/taskComplete", methods=['post'])
def finishtask():
    print("hello finish task")
    data = request.get_json()
    task = task_completed(data)
    if task:
        return jsonify(task)
    else:
        return jsonify("Failure")


@app.route("/deleteTask", methods=['post'])
def delete():
    data = request.get_json()
    print("hello delete task", data)

    task = task_delete(data)
    if task:
        return jsonify(task)
    else:
        return jsonify("Failure")


@app.route("/getTeams", methods=['POST'])
def teams_name():
    userid = request.get_json()
    userid = ObjectId(userid)
    print(f"the user ud is: {userid} type of useris is:{type(userid)}")

    teamsid = get_teams_from_userid(userid)
    print(f"the teams id is: {teamsid}type of teams id is:{type(teamsid)}")
    teamsname = team_name_from_teamid(teamsid)
    print(f"the teams name is: {teamsname}type of teams name is:{type(teamsname)}")
    if teamsname:
        return jsonify(teamsname)
    else:
        return jsonify("Failure")


@app.route("/createUser", methods=['POST'])
def create_new_user():
    print("get json{}".format(request.get_json()))
    print(request.from_values())
    data = request.get_json()
    print(data)
    res = check_data(data)
    print("res is{}".format(res))
    if type(res) == bool:
        set_user_to_server(data)
        return jsonify('OK')
    else:
        return jsonify(res)


@app.route("/login", methods=['POST'])
def checkLogin():
    print("log in")
    data = request.get_json()
    useremail = data["email"]
    truemail = user_authentication(useremail)
    time.sleep(1)
    if data["password"] == truemail["userpassword"]:
        print("Success")
        return jsonify(str(truemail["_id"]))
    print("Failure")
    return "Failure"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
    # check_email("amit255888888888888@gmail.com")
    dat = {
        "username": "avivush",
        "name": "aviv",
        "lastname": "lev",
        "useremail": "avivlev@gmail.com",
        "age": "34",
        "userpassword": "123123123",
        "usercity": "jerusalem",
        "teams": []
    }
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
    #
    teamid = "63fbb19223262f5715440fdf"
    # username = "aviviti"
    task = "by ticket for the trip"
    title = "trip"
    # taskid = "63b41db0cf3bbd24a5a8b271"
    date = datetime.date(2023, 3, 12)
    #
    # create_new_user(dat)
    # new_team("newteam", "aviviti")
    # add_user_to_team("gadsh", teamid)
    # add_new_task(teamid, "gadsh", title, task, date)
    # task_completed(teamid, taskid, "gadsh")
    # change_detail("aviviti", "name", "avihay")
    # change_username("aviviti","avihayush")
    # change_password("avihayush", "123123132", "111111111")
