import streamlit as st
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components
import os
from pymongo import MongoClient
from datetime import datetime
from PIL import Image
from io import BytesIO
import base64

# ENVIRONMENT VARIABLES
PROCESSED_FOLDER = os.getenv("PROCESSED_FOLDER")
PROCESSED_FOLDER = os.path.realpath(PROCESSED_FOLDER)
MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_METADATA_COLLECTION")
REFRESH_INTERVAL = 10

# MONGO CONNECTION
class MongoDBConnection:

    def __init__(self):
        
        self.client = MongoClient(MONGO_URL)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]
        self.hidden_collection = self.db.get_collection("hidden_metadata")

    def get_images_metadata(self):
        return list(self.collection.find({}).sort("timestamp", -1))

    def get_hidden_collection(self):
        return self.hidden_collection

    def get_metadata_collection(self):
        return self.collection


# Utility functions

st.markdown("""
<style>
.meta-block {
    font-size: 0.88rem;
    line-height: 1.6;
}
.button-align {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    height: 100%;
}
</style>
""", unsafe_allow_html=True)

def pil_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

mongo_conn = MongoDBConnection()
docs = mongo_conn.get_images_metadata()
    
def on_click_func(doc):
    mongo_conn.get_hidden_collection().insert_one(doc)
    mongo_conn.get_metadata_collection().delete_one({"_id": doc['_id']})
    st.session_state.hidden_ids.add(doc_id)
    st.rerun()

# Streamlit web app configuration

st_autorefresh(interval=REFRESH_INTERVAL * 1000, key="auto-refresh")

st.title("Images Classification Results")
st.text("Here the results of the image classification process are shown. To confirm that the image was processed, click on the 'Processed' button.")

if "hidden_ids" not in st.session_state:
    st.session_state.hidden_ids = set()

if not docs:
    st.info("No data available.")
else:
    for doc in docs:
        doc_id = str(doc['_id'])

        if doc_id in st.session_state.hidden_ids:
            continue

        image_path = doc.get("file_path")
        file_name = doc.get("file_name", "N/A")
        label = doc.get("label", "N/A")
        score = doc.get("prediction_score", "N/A")
        size = doc.get("image_size_bytes", "N/A")
        timestamp = doc.get("timestamp")
        if isinstance(timestamp, int):
            timestamp = datetime.fromtimestamp(timestamp / 1000)
        timestamp_str = timestamp.strftime("%d/%m/%Y %H:%M:%S") if timestamp else "N/A"

        with st.container():
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1.2, 3, 1])

            with col1:
                if os.path.exists(image_path):

                    image = Image.open(image_path)
                    img_base64 = pil_to_base64(image)
                    st.text("")

                    components.html(f"""
                    <style>
                    .custom-img {{
                        width: 90%;
                        cursor: zoom-in;
                        border-radius: 0.5rem;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                        transition: all 0.3s ease;
                    }}
                    .custom-img:fullscreen {{
                        width: 100vw;
                        height: 100vh;
                        object-fit: contain;
                        cursor: zoom-out;
                        background-color: black;
                    }}
                    </style>

                    <div style="text-align: center; margin-bottom: 10px;">
                    <img id="img-{doc_id}" class="custom-img"
                        src="data:image/png;base64,{img_base64}"
                        onclick="toggleFullscreen('{doc_id}')" />
                    </div>

                    <script>
                    function toggleFullscreen(id) {{
                        const img = document.getElementById("img-" + id);
                        if (!document.fullscreenElement) {{
                            img.requestFullscreen();
                        }} else {{
                            document.exitFullscreen();
                        }}
                    }}
                    </script>
                    """)

                else:
                    st.warning("Image not found.")

            with col2:
                st.markdown(f"### {file_name}")
                if os.path.exists(image_path):
                    width, height = image.size
                    dimensions = f"{width}x{height}"
                else:
                    dimensions = "N/A"
                st.markdown(f"""
                    <div class="meta-block">
                    <strong>Dimensions:</strong> {dimensions}<br>
                    <strong>Size:</strong> {size} bytes<br>
                    <strong>Label:</strong> {label}<br>
                    <strong>Prediction Score:</strong> {score}<br>
                    <strong>Timestamp:</strong> {timestamp_str}
                    </div>
                """, unsafe_allow_html=True)

            with col3:
                st.text("")
                st.text("")
                st.text("")
                st.text("")
                st.markdown('<div class="button-align">', unsafe_allow_html=True)
                if st.button("Processed", key=doc_id, use_container_width=True):
                    on_click_func(doc)
                st.markdown('</div>', unsafe_allow_html=True)
                
            st.markdown('<hr style="border: 2px solid #000000; margin: 30px 0;">', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)