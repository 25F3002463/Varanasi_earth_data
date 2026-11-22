import streamlit as st
from PIL import Image
import pandas as pd
import os

st.set_page_config(
    page_title="Varanasi Satellite Intelligence",
    page_icon="🛰️",
    layout="wide"
)

st.title("🛰️ Varanasi Satellite Intelligence")
st.write("Earth Observation & Vegetation Analysis")

st.divider()

# Load images
if os.path.exists("varanasi_satellite.png"):

    rgb = Image.open("varanasi_satellite.png")

    ndvi = Image.open("varanasi_ndvi.png")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Satellite Imagery")
        st.image(rgb, use_container_width=True)

    with col2:
        st.subheader("NDVI Vegetation Map")
        st.image(ndvi, use_container_width=True)

else:
    st.error("Satellite images not found!")

st.divider()

st.subheader("Location Information")

st.write("Location: Varanasi, Uttar Pradesh")
st.write("Satellite: Sentinel-2")
st.write("Analysis: Vegetation Index (NDVI)")

st.success("Satellite dashboard loaded!")