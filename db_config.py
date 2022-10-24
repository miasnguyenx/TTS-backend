from pymongo import MongoClient


def get_database():

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    # LWvsalkRYIrldscM
    CONNECTION_STRING = "mongodb+srv://nghianguyen:LWvsalkRYIrldscM@\
       cluster0.x9w591u.mongodb.net/?retryWrites=true&w=majority"
    # Create a connection using MongoClient. You can import MongoClient or use
    # pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database
    # throughout the tutorial)
    try:
        print(client.server_info())
    except Exception:
        print("Unable to connect to the server.")
    return client['sample_airbnb']


db = get_database()
