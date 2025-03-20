import json
import os
import mongo_connection

DATA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__))))), 'data')

def import_json_to_mongo():
    # Path to the JSON file
    file_path = os.path.join( DATA_FOLDER, '23S.json')
    
    # Read the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Get the MongoDB collection
    collection = mongo_connection.get_mongo_collection('prova_db', 'images')
    
    # Insert data into MongoDB
    collection.insert_many(data)
