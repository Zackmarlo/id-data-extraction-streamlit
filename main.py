# app.py
import streamlit as st
import cv2
import numpy as np
import pandas as pd
from OCR import extract_text
from ultralytics import YOLO
import os

import torch

torch.classes.__path__ = []
model = YOLO("best.pt")
st.set_page_config(page_title="🪪 ID OCR", layout="centered")
st.title("🪪 ID Data Extraction")

uploaded_file = st.file_uploader("📤 Upload your ID image", type=["png", "jpg", "jpeg"])
os.makedirs("croped", exist_ok=True)  # Create directory if it doesn't exist
if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    st.image(image_rgb, caption="Uploaded ID", use_container_width=True)

    with st.spinner("🔍 Detecting ID..."):
        results = model(image_rgb, conf=0.5)
        annotated_image = results[0].plot()
        print(len(results[0].boxes))
        st.image(annotated_image, caption="Detected ID", use_container_width=True)
    for i, box in enumerate(results[0].boxes.xyxy):  # xyxy = [x1, y1, x2, y2]
      class_id = int(results[0].boxes.cls[i])
      label = model.names[class_id]
      x1, y1, x2, y2 = map(int, box)

      # Crop and save
      cropped = image_rgb[y1:y2, x1:x2]
      crop_path = f"{label}.jpg"
      cv2.imwrite(os.path.join("croped",crop_path), cropped)
    with st.spinner("🔍 Processing the image..."):
        try:
            data = extract_text("croped")
            st.success("✅ Extraction complete!")
            df = pd.DataFrame([data])
            st.table(df)
        except Exception as e:
            st.error(f"❌ Failed to process image: {e}")
            raise e
