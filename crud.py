from ast import Constant
from unicodedata import name
from flask.wrappers import Response
import json
from flask import request
from bson.objectid import ObjectId
from prometheus_client import Counter, Gauge, Histogram, Summary
import requests


creating = Counter('create', 'flaskApp create user')
verifying = Counter('verify', 'flaskApp verify user')
updating = Counter('update', 'flaskApp update user')
deleting = Counter('delete', 'flaskApp delete user')
genre_search = Counter('genre_search', 'Searching movies by Genre', ['genre'])


STREAM_REQUEST_PROCESS_TIME = Summary('stream_request_process_time', 'Time spent processing request')

class Crud():
    def __init__(self, mydb):
        self.mydb = mydb
        

    def verify_user(self):
        verifying.inc()
        mydb = self.mydb
        try:
            data = {"Name": request.form["Name"],
                    "lastName": request.form["lastName"]}
            my_collection = mydb.myNewCollection2
            db_response = my_collection.find_one(data)
            # for attr in dir(db_response):
            #     print(attr)
                
            # print(db_response.__getattribute__)
            # print(type(db_response))
            print("---------------------------------------------")
            if (db_response):
                return Response(
                    response=json.dumps({
                        "message": "User found",
                        "id": f"{db_response['_id']}",
                    }),
                    status=200,
                    mimetype="application/json",
                )
            else:
                return Response(
                    response=json.dumps({
                        "message": "user not found",
                    }),
                    status=404,
                    mimetype="application/json"
                )
        except Exception as ex:
            print(ex)
        return Response(
            response=json.dumps({
                "message": "can not verify user",
            })
        )

    def insert_user(self):
        mydb = self.mydb
        try:
            data = {"Name": request.form["Name"],
                    "lastName": request.form["lastName"]}
            my_collection = mydb.myNewCollection2
            db_response = my_collection.insert_one(data)
            # for attr in dir(db_response):
            #     print(db_response.attr)
            # print(db_response.inserted_id)
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
            return Response(
                response=json.dumps({
                    "message": "Error on creating user",
                }),
                status=404,
            )

    def delete_user(self, id):
        mydb = self.mydb
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
                
            else: 
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
                "message": "Wrong objectid format",
            })
        )
    def get_user_id(self):
        mydb = self.mydb
        try:
            my_collection = mydb.myNewCollection2
            data = list(my_collection.find())
            for user in data:
                user["_id"] = str(user["_id"])
            print(data)
            return Response(
                response=json.dumps(data),
                status=500,
                mimetype="application/json",
            )
        except Exception:
            print("ERROR: get_users failed")
        return Response(
            response=json.dumps({
                "message": "error on getting user",
            })
        )
    def get_users(self):
        mydb = self.mydb
        try:
            my_collection = mydb.myNewCollection2
            data = list(my_collection.find())
            for user in data:
                user["_id"] = str(user["_id"])
            print(data)
            return Response(
                response=json.dumps(data),
                status=500,
                mimetype="application/json",
            )
        except Exception:
            print("ERROR: get_users failed")
        return Response(
            response=json.dumps({
                "message": "error on getting user",
            })
        )

    def update_user(self, id):
        mydb = self.mydb
        try:
            my_collection = mydb.myNewCollection2
            db_response = my_collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"Name": request.form["Name"],
                          "lastName": request.form["lastName"]}}
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

    def get_user_by_id(self, id):
        mydb = self.mydb
        try:
            my_collection = mydb.myNewCollection2
            db_response = my_collection.find_one({"_id": ObjectId(id)})
            print(db_response)
            print(type(db_response))
            # ***************************
            db_response["_id"] = str(db_response["_id"])
            # ***************************
            for attr in dir(db_response):
                print(attr)
            if db_response:
                return Response(
                        response=json.dumps(db_response),
                        status=200,
                        mimetype="application/json"
                )
            else:
                return Response(
                        response=json.dumps(db_response),
                        status=404,
                        mimetype="application/json"
                )
        except Exception as ex:
            print(ex)
            return Response(
                response=json.dumps({
                    "message": "user id not exist",  
                }),
                status=404,
            )
