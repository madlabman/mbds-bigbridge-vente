from pymongo import MongoClient

client = MongoClient('document', 27017)
db = client.test
order = {'OrderId':1, 'TotalPrice': 100500}
orders = db.orders
order_id = orders.insert_one(order).inserted_id
print(order_id)
