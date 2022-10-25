from array import array
from cgi import print_directory
from unicodedata import name
from faker import Faker
import pymongo

try:
    myclient = pymongo.MongoClient(
        "mongodb+srv://nghianguyen:LWvsalkRYIrldscM@clus\
        ter0.x9w591u.mongodb.net/?retryWrites=true&w=majority")
    db = myclient["sample_airbnb"]
    # print(myclient.server_info())
except ConnectionError:
    print("MONGO CONNECTION ERROR")

fake = Faker()
a_name = fake.name()

# for i in range(100):
#     a_object = {
#         "Name": fake.first_name(),
#         "lastName": fake.last_name()
#     }
#     db.myNewCollection2.insert_one(a_object)


def add_data():
    for i in range(100):
        a_object = {
            "Name": fake.first_name(),
            "lastName": fake.last_name()
        }
        db.myNewCollection2.insert_one(a_object)


for i in db.myNewCollection2.find():
    print(i)
myclient.close()
