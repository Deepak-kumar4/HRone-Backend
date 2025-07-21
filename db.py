from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = None
db = None

def connect_to_mongo():
    global client, db
    mongo_url = os.getenv("MONGO_URL")
    client = MongoClient(mongo_url)
    db = client["hrone"]
    init_indexes()  # Ensure indexes are created once connected

def get_db():
    return db

def init_indexes():
    try:
        db.orders.create_index("user_id")  # Optimize GET /orders/user_id
        db.orders.create_index("items.product_id")  # Improve product lookups in orders
        db.products.create_index("name")  # Optional: Useful for product name search
        print("✅ Indexes initialized successfully.")
    except Exception as e:
        print("❌ Error initializing indexes:", e)
