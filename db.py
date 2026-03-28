from pymongo import MongoClient

# Connect to MongoDB (local)
client = MongoClient("mongodb://localhost:27017/")

# Create/use database
db = client["Online_Food_Delivery"]

# Collections
users = db["users"]
menu = db["menu"]
orders = db["orders"]

