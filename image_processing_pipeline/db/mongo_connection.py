from pymongo import MongoClient

# MongoDB connection info
MONGO_URI = 'mongodb://root:example@mongo:27017/'
MONGO_DB = 'prova_db'
MONGO_IMAGE_COLLECTION = 'images'
MONGO_RESULT_COLLECTION = 'results'

def get_mongo_db():
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    return db

def get_mongo_image_collection():
    db = get_mongo_db()
    collection = db[MONGO_IMAGE_COLLECTION]
    return collection

def get_mongo_result_collection():
    db = get_mongo_db()
    collection = db[MONGO_RESULT_COLLECTION]
    return collection

def get_mongo_connection():
    return MongoClient(MONGO_URI)

def get_mongo_db(db_name):
    client = get_mongo_connection()
    db = client[db_name]
    return db

def get_mongo_collection(db_name, collection_name):
    db = get_mongo_db(db_name)
    collection = db[collection_name]
    return collection

