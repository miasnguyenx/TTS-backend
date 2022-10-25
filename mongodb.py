import pymongo


def connect():
    myclient = pymongo.MongoClient(
            "mongodb+srv://nghianguyen:DdIkT3fWitktzD0m@clus\
            ter0.x9w591u.mongodb.net/?retryWrites=true&w=majority")
    mydb = myclient["sample_airbnb"]
#     print(myclient.server_info())
    return mydb
