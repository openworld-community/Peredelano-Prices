import datetime
import pytz

from dao.CRUD import get_database, update_price_by_name

db = get_database()
test_coll = db['testcoll']

# test_item = {
#     "_id": 1,
#     "product": {
#         "name": "B&J strawberry cheesecake 465ml",
#         "price": [
#             "7,00",
#             "€"
#         ]
#     },
#     "market": "Aroma"
# }
# test_coll.insert_one(test_item)

update_price_by_name(test_coll, "B&J strawberry cheesecake 465ml", "9.00")


