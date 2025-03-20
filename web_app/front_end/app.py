import pymongo 
import streamlit as st
import pandas as pd

@st.cache_resource
def init_connection():
    return pymongo.MongoClient("mongodb://root:example@mongo:27017/")


client = init_connection()
db = client["prova_db"]
collection = db["images"]

# Fetch only the "Organism name" field from MongoDB
def fetch_organism_names():
    data = collection.find({}, {"Organism name": 1, "_id": 0})  # Exclude _id
    return [doc["Organism name"] for doc in data]

# Convert to DataFrame for better visualization
organism_names = fetch_organism_names()
df = pd.DataFrame(organism_names, columns=["Organism name"])

# Streamlit UI
st.title("Organism Names from MongoDB")
st.dataframe(df)  # Display as a table
