from flask import Flask, request, redirect, render_template
import json
from flask.wrappers import Response
import pymongo
from redis_db import redis_conn
from bson.objectid import ObjectId


app = Flask(__name__)

try:
    myclient = pymongo.MongoClient(
        "mongodb+srv://nghianguyen:DdIkT3fWitktzD0m@clus\
        ter0.x9w591u.mongodb.net/?retryWrites=true&w=majority")
    mydb = myclient["sample_airbnb"]
    print(myclient.server_info())
except ConnectionError:
    print("MONGO CONNECTION ERROR")

try:
    myredis = redis_conn()
    myredis.set("a", "b")
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
    try:
        data = {"name": request.form["name"],
                "lastName": request.form["lastName"]}
        my_collection = mydb.myNewCollection2
        db_response = my_collection.insert_one(data)
        print(db_response.inserted_id)
        return Response(
            response=json.dumps({
                "message": "user_created",
                "id": f"{db_response.inserted_id}"
            }),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)


@app.route("/getusers", methods=['GET'])
def get_users():
    try:
        my_collection = mydb.myNewCollection2
        data = list(my_collection.find())
        for user in data:
            user["_id"] = str(user["_id"])
        print(data)
        return Response(
            response=json.dumps(data),
            status=500,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
    return Response(
        response=json.dumps({
            "message": "cannot read users",
        })
    )


@app.route("/delete/<id>", methods=['DELETE'])
def delete(id):
    try:
        my_collection = mydb.myNewCollection2
        db_response = my_collection.delete_one({"_id": ObjectId(id)})
        if db_response.deleted_count == 1:

            return Response(
                response=json.dumps({
                    "message": "user deleted",
                }),
                status=200,
                mimetype="application/json"
            )
        return Response(
            response=json.dumps({
                "message": "user not found",
            }),
            status=200,
            mimetype="application/json"
        )

    except Exception as ex:
        print(ex)
    return Response(
        response=json.dumps({
            "message": "delete failed",
        })
    )


@app.route("/update/<id>", methods=['PATCH'])
def update(id):
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
