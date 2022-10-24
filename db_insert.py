from dateutil import parser
from db_config import get_database

dbname = get_database()
collection_name = dbname["user_1_items"]

expiry_date = '2021-07-13T00:00:00.000Z'
expiry = parser.parse(expiry_date)
item_3 = {
  "item_name": "Bread",
  "quantity": 2,
  "ingredients": "all-purpose flour",
  "expiry_date": expiry
}
collection_name.insert_one(item_3)
