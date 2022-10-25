from redis.commands.json.path import Path
from flask import Flask, request, redirect, render_template
import json
import rediscached
import mongodb
import crud


app = Flask(__name__)

try:
    mydb = mongodb.connect()
    worker = crud.Crud(mydb)
except ConnectionError:
    print("MONGO CONNECTION ERROR")

try:
    myredis = rediscached.connect()
except ConnectionError:
    print("REDIS CONNECTION ERROR")


@app.route("/")
def app_setup():
    return "HELLO"


@app.route("/create", methods=['POST'])
def create():
    result = worker.insert_user()
    return result


@app.route("/getusers", methods=['GET'])
def get_users():
    result = worker.get_users()
    return result


@app.route("/delete/<id>", methods=['DELETE'])
def delete(id):
    result = worker.delete_user(id)
    return result


@app.route("/update/<id>", methods=['PUT'])
def update(id):
    result = worker.update_user(id)
    return result


@app.route("/getuser/<id>", methods=['GET'])
def get_user(id):
    result = worker.get_user(id)
    user = result.data.decode("utf-8")
    user = json.loads(user)
    # print(user)
    # print(user["_id"])
    user_cached = {
        "user": {
            "name": user["Name"],
            "lastName": user["lastName"]
        }
    }
    myredis.json().set("user:"+user["_id"], "$", user_cached)
    return result
