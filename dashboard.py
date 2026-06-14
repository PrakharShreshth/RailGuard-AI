# dashboard.py

import streamlit as st
from database import get_all_detections

st.set_page_config(
    page_title="RailGuard Dashboard",
    layout="wide"
)

st.title("📊 RailGuard Dashboard")

df = get_all_detections()

if len(df) == 0:

    st.warning("No detections found in database.")

else:

    st.subheader("Detection History")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("Defect Distribution")

    st.bar_chart(
        df["defect"].value_counts()
    )

    st.subheader("Risk Level Distribution")

    st.bar_chart(
        df["risk_level"].value_counts()
    )

    st.subheader("Average Risk Score")

    st.metric(
        "Average Risk Score",
        round(df["risk_score"].mean(), 2)
    )

    st.subheader("Latest Detection")

    latest = df.iloc[0]

    st.write(
        f"Defect: {latest['defect']}"
    )

    st.write(
        f"Confidence: {latest['confidence']:.2f}"
    )

    st.write(
        f"Risk Level: {latest['risk_level']}"
    )

    st.write(
        f"Risk Score: {latest['risk_score']}"
    )
