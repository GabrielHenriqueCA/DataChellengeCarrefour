from pymongo import MongoClient

# Conectando com o MongoDb

client = MongoClient("mongodb://dio:dio@localhost:27017/")
db = client.dio
collection_trends = db.trends