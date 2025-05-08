# main.py
import streamlit as st
import cv2
from YOLO import detect_and_crop
from OCR import extract_text
from database import insert_to_db
import os

st.title("Egyptian ID Data Extraction")

frame_placeholder = st.empty()
status_placeholder = st.empty()

camera = cv2.VideoCapture(1)  # or use Streamlit's st.camera_input if manual capture

while True:
    ret, frame = camera.read()
    if not ret:
        status_placeholder.error("Failed to capture from camera.")
        break

    # Run YOLO detection
    detections, all_boxes_found = detect_and_crop(frame)

    # Show frame in Streamlit
    frame_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")

    if all_boxes_found:
        status_placeholder.success("All fields detected with confidence > 80%.")

        # Pass cropped fields to OCR
        extracted_data = extract_text("temp_crops/")
        
        # Insert to database
        insert_to_db(extracted_data)

        # Clean up
        for file in os.listdir("temp_crops/"):
            os.remove(os.path.join("temp_crops/", file))
        break
