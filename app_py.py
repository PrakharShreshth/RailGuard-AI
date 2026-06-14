import streamlit as st
from ultralytics import YOLO
from PIL import Image
import tempfile
import os

from risk_engine import calculate_risk
from database import create_table, insert_detection

# -----------------------------
# Create Database Table
# -----------------------------
create_table()

# -----------------------------
# Load Latest YOLO Model
# -----------------------------
model = YOLO(
    r"C:\Users\Prakhar\railguard\runs\detect\train-3\weights\best.pt"
)

# -----------------------------
# Streamlit Page Setup
# -----------------------------
st.set_page_config(page_title="RailGuard AI")

st.title("🚆 RailGuard AI")
st.subheader("Railway Track Defect Detection")

# -----------------------------
# Upload Image
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Railway Track Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Image",
        use_container_width=True
    )

    # -----------------------------
    # Save Temporary Image
    # -----------------------------
    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    )

    temp_path = temp_file.name
    temp_file.close()

    image.save(temp_path)

    # -----------------------------
    # YOLO Prediction
    # -----------------------------
    results = model.predict(
        source=temp_path,
        conf=0.001
    )

    boxes = results[0].boxes

    st.markdown("---")
    st.subheader("Raw YOLO Predictions")

    detected_class = "normal_track"
    highest_conf = 0.0

    if len(boxes) == 0:

        st.write("No detections found")

        detected_class = "normal_track"
        highest_conf = 1.0

    else:

        for box in boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            defect = model.names[class_id]

            st.write(
                f"Class: {defect} | Confidence: {confidence:.4f}"
            )

            if confidence > highest_conf:
                highest_conf = confidence
                detected_class = defect

    # -----------------------------
    # Risk Calculation
    # -----------------------------
    risk_level, risk_score = calculate_risk(
        detected_class
    )

    # -----------------------------
    # Inspection Report
    # -----------------------------
    st.markdown("---")
    st.subheader("Inspection Report")

    st.write(f"Defect: {detected_class}")
    st.write(f"Confidence: {highest_conf:.4f}")
    st.write(f"Risk Level: {risk_level}")
    st.write(f"Risk Score: {risk_score}")

    if detected_class == "crack":

        st.error(
            "🚨 Crack Detected - Immediate Maintenance Required"
        )

    elif detected_class == "bolt_missing":

        st.warning(
            "⚠ Bolt Missing Detected"
        )

    elif detected_class == "clip_missing":

        st.warning(
            "⚠ Clip Missing Detected"
        )

    else:

        st.success(
            "✅ Track Appears Safe"
        )

    # -----------------------------
    # Save Detection To Database
    # -----------------------------
    insert_detection(
        defect=detected_class,
        confidence=highest_conf,
        risk_level=risk_level,
        risk_score=risk_score
    )

    # -----------------------------
    # Show Detection Image
    # -----------------------------
    plotted = results[0].plot()

    st.image(
        plotted,
        caption="Detection Result",
        use_container_width=True
    )

    # -----------------------------
    # Delete Temp File
    # -----------------------------
    try:
        os.remove(temp_path)
    except:
        pass
