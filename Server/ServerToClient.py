import pymongo
from ServerToDataBase import *
import datetime
from flask import Flask, request, jsonify
import json
import re
from validate_email import validate_email
import requests


# import MySQLdb


# ------------------------ data for user ------------------------

def create_new_user(userdata):
    res = check_data(userdata)
    if type(res) == bool:
        set_user_to_server(userdata)
        return "New user created successfully"
    else:
        return res


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
    send = "Please change the rep, it is incorrect"
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


def get_user(username):
    print(get_user_from_server(username))


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


def change_password(username, newpassword):
    change_some(username, "userpassword", newpassword)


# ------------------------ data for team ------------------------
def new_team(team_name, username):
    create_team(team_name, username)


def get_team(teamid):
    print(get_team_from_server(teamid))


def new_user_for_team(username, teamid):
    add_user_to_team(username, teamid)


# ------------------------ data for tasks ------------------------

def add_new_task(teamid, username, task, date=None):
    set_task(teamid, username, task, date)


def task_completed(teamid, taskid, username):
    finish_task(teamid, taskid, username)


# ------------------------ data for shoppinglist ------------------------


# Setup flask server
app = Flask(__name__)


# def sql():
#     db = MySQLdb.connect("localhost","root","","sql8591008")
#     insertrec=db.cursor()
#     sqlquery="insert into users()"


# Setup url route which will calculate
# total sum of array.
@app.route('/project/register', methods=['POST'])
def sum_of_array():
    data = request.get_json()
    res = create_new_user(data)
    print(res)
    print(data)

    # Data variable contains the
    # data from the node server
    # ls = data['array']

    # calculate the sum

    # Return data in json format
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(port=5000)

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
    # userdata = {
    #     "username": "gadsh",
    #     "name": "gad",
    #     "lastname": "shrim",
    #     "useremail": "gadsh@gmail.com",
    #     "age": "30",
    #     "userpassword": "11223344",
    #     "usercity": "Ashdod",
    #     "teams": []
    # }
    #
    # teamid = "63b41d1edd3902090a55ef80"
    # username = "aviviti"
    # task = "buy a new computer"
    # taskid = "63b41db0cf3bbd24a5a8b271"
    # date = datetime.date(2023, 1, 12)
    #
    # create_new_user(dat)
    # new_team("newteam", "aviviti")
    # add_user_to_team("gadsh", teamid)
    # add_new_task(teamid, username, task, date)
    # task_completed(teamid, taskid, "gadsh")
    # change_detail("aviviti", "lastname", "shoshi")
