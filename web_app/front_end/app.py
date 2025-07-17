import streamlit as st
import os
from pymongo import MongoClient
import pandas as pd
from PIL import Image
from streamlit_autorefresh import st_autorefresh


# DATA FOLDER
PROCESSED_FOLDER = os.getenv("PROCESSED_FOLDER")
PROCESSED_FOLDER = os.path.realpath(PROCESSED_FOLDER)
# MONGODB variables
MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_METADATA_COLLECTION")

REFRESH_INTERVAL = 30

class MongoDBConnection:
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]
        
    def get_images_metadata(self):
        return list(self.collection.find({}))

def load_image_with_metadata(doc):
    filename = doc.get("file_name")
    file_path = doc.get("file_path", "")
    
    st.markdown("---")
    if os.path.exists(file_path):
        try:
            image = Image.open(file_path)
            st.image(image, caption=filename, use_column_width=True)
        except Exception as e:
            st.error(f"Error loading image {file_path}: {e}")
    else:
        st.warning(f"Image not found: {file_path}")

    # Show metadata nicely
    st.json({k: v for k, v in doc.items() if k != 'image_data'})

st_autorefresh(interval=REFRESH_INTERVAL * 1000, key="auto-refresh")

st.title("📸 Data Processing Results")
st.caption(f"Auto-refresh every {REFRESH_INTERVAL} seconds")

# Mongo connection
mongo_conn = MongoDBConnection()
images_metadata = mongo_conn.get_images_metadata()

if not images_metadata:
    st.warning("No image metadata found.")
else:
    # Show each image with metadata
    for doc in images_metadata:
        # Optional cleanup
        doc['_id'] = str(doc['_id'])
        if 'timestamp' in doc:
            doc['timestamp'] = pd.to_datetime(doc['timestamp'], unit='ms')
        load_image_with_metadata(doc)