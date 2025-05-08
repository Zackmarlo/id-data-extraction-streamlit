import streamlit as st
import cv2
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from YOLO import detect_and_crop
from OCR import extract_text
from database import insert_to_db
import os
import shutil


# Define the VideoProcessor class to process the webcam feed
class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.detections_done = False

    def transform(self, frame):
        # Convert the frame to numpy array (BGR format)
        img = frame.to_ndarray(format="bgr24")

        # Run YOLO detection on the frame
        detections, all_boxes_found = detect_and_crop(img)

        # If detections are found, add the labels to the frame
        if detections:
            for detection in detections:
                # Assuming each detection is a tuple (x, y, w, h, label, confidence)
                x, y, w, h, label, confidence = detection
                color = (0, 255, 0)  # Green for bounding box
                thickness = 2

                # Draw the bounding box
                cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness)

                # Draw the label (with confidence)
                label_text = f"{label}: {confidence:.2f}"
                cv2.putText(img, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, thickness)

        # Display the frame with the labels on Streamlit
        frame_placeholder.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), channels="RGB")

        # If all boxes are found, handle OCR and database insertion
        if all_boxes_found and not self.detections_done:
            self.detections_done = True
            # Save the crops from YOLO detection for OCR
            crop_folder = "temp_crops/"
            if not os.path.exists(crop_folder):
                os.makedirs(crop_folder)
            
            for idx, crop in enumerate(detections):
                crop_path = os.path.join(crop_folder, f"crop_{idx}.jpg")
                cv2.imwrite(crop_path, crop)

            # OCR extraction
            extracted_data = extract_text(crop_folder)

            # Insert extracted data into DB
            insert_to_db(extracted_data)

            # Clean up temporary crops
            shutil.rmtree(crop_folder)

        # Return the frame to keep displaying in Streamlit
        return img

# Streamlit app layout
st.title("Egyptian ID Data Extraction")

frame_placeholder = st.empty()
status_placeholder = st.empty()

# Streamlit WebRTC to access webcam
webrtc_streamer(
    key="example",
    video_processor_factory=VideoProcessor,
)

# We update status based on detections
if "detections_done" in st.session_state and st.session_state.detections_done:
    status_placeholder.success("All fields detected with confidence > 80%. Data inserted to database.")
else:
    status_placeholder.info("Waiting for ID to be scanned...")

# You can add additional UI elements for feedback and actions here
