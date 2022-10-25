from curses.ascii import NUL
from queue import Empty
from unittest import result
from flask import Flask, request, redirect, render_template
import json
from flask.wrappers import Response
import pymongo
import rediscached
import mongodb
import crud
from bson.objectid import ObjectId


app = Flask(__name__)

try:
    mydb = mongodb.connect()
    print(mydb)
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


# @app.route("/")
# def read():
#     return render_template('index.html')


@app.route("/create", methods=['POST'])
def create():
    worker.insert_user()


@app.route("/getusers", methods=['GET'])
def get_users():
    result = worker.get_users()
    if (result):
        return Response(
            response=result,
            status=500,
            mimetype="application/json"
        )


@app.route("/delete/<id>", methods=['DELETE'])
def delete(id):
    result = worker.delete_user(id)
    return result


@app.route("/update/<id>", methods=['PATCH'])
def update(id):
    result =
    try:
        my_collection = mydb.myNewCollection2
        db_response = my_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"name": request.form["name"]}}
        )

        for attr in dir(db_response):
            print(attr)
        print(db_response.modified_count)

        if db_response.modified_count == 1:
            return Response(
                response=json.dumps({"message": "user updated"}),
                status=200,
                mimetype="application/json"
            )

        return Response(
            response=json.dumps({
                "message": "nothing to update",
            }),
        )

    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({
                "message": "cannot update users",
            })
        )
