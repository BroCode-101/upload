import streamlit as st
import pandas as pd
import cloudinary.uploader
import cloudinary
from dotenv import load_dotenv
import os
import io

st.write("📤 This is the upload page. You can upload files here.")
file = st.file_uploader("Upload your CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    st.write("✅ Dataset loaded successfully")
    st.dataframe(df.head())

def upload_to_cloud(file):
    load_dotenv()
    cloudinary.config(
        cloud_name=os.getenv("CLOUD_NAME"),
        api_key=os.getenv("API_KEY"),
        api_secret=os.getenv("API_SECRET")
    )
    st.write("🔗 Connected to Cloudinary:", cloudinary.config().cloud_name)
    file.seek(0)
    file_bytes = file.read()
    file_stream = io.BytesIO(file_bytes)

    link = cloudinary.uploader.upload(
        file_stream,
        resource_type="raw",
        folder="test_uploader",
        public_id=file.name.split('.')[0]
    )
    st.success("✅ Dataset uploaded successfully!")
    st.write("🔗 File URL:", link['secure_url'])
    # st.json(link)  # Uncomment to see full response

if st.button("Upload to Cloudinary"):
    try:
        upload_to_cloud(file)
    except Exception as err:
        st.error(f"❌ Error uploading file to Cloudinary: {err}")