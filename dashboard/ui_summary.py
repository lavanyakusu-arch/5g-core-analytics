import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import logging

# -------------------- Logging Configuration --------------------
logger = logging.getLogger("dashboard_summary")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

# -------------------- API Endpoints --------------------
API_URL = "http://127.0.0.1:8000/summary"
API_SNSSAI_URL = "http://127.0.0.1:8000/snssai"

def show_summary_page():
    """
    Renders the 5G Core Network KPI Summary page
    - Left column: KPIs
    - Right column: Success rate indicators
    - Pie chart: Session distribution by slice
    """
    st.title("📊 5G Core Network KPI Summary")

    # -------------------- Fetch KPI Summary Data --------------------
    try:
        logger.info("Fetching KPI summary from API")
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        logger.debug(f"KPI summary data fetched: {data}")
    except Exception as e:
        logger.exception("Failed to fetch KPI summary")
        st.error(f"Failed to fetch data from API: {e}")
        st.stop()

    # -------------------- Layout: KPIs & Indicators --------------------
    left_col, right_col = st.columns([2, 1])

    # ---------------- LEFT COLUMN: Key KPIs ----------------
    with left_col:
        st.markdown("### 📌 Key KPIs")

        st.metric("📱 Registered UEs", value=data["registered_ues"])
        st.metric("🔗 PDU Sessions Established", value=data["pdu_sessions_established"])
        st.metric("❌ Registration Failures", value=data["registration_failures"])
        st.metric("❌ PDU Session Failures", value=data["pdu_session_failures"])

    # ---------------- RIGHT COLUMN: Success Rate Indicators ----------------
    with right_col:
        st.subheader("🎯 Success Rate Indicators")

        st.write("Registration Success")
        st.progress(min(data["registration_success_rate"] / 100, 1.0))
        st.caption(f"{data['registration_success_rate']}%")

        st.write("PDU Session Success")
        st.progress(min(data["session_success_rate"] / 100, 1.0))
        st.caption(f"{data['session_success_rate']}%")

    # -------------------- Fetch SNSSAI / Slice Data --------------------
    try:
        logger.info("Fetching SNSSAI slice data from API")
        response = requests.get(API_SNSSAI_URL, timeout=5)
        response.raise_for_status()
        snssai_data = response.json()
        logger.debug(f"SNSSAI data fetched: {snssai_data}")
    except Exception as e:
        logger.exception("Failed to fetch SNSSAI data")
        st.error(f"Failed to fetch data from API: {e}")
        st.stop()

    slices = []
    session_counts = []

    for slice_name, value in snssai_data.items():
        slices.append(slice_name)
        session_counts.append(value["sessions"])

    total_sessions = sum(session_counts)
    percentages = [(count / total_sessions) * 100 if total_sessions > 0 else 0
                   for count in session_counts]

    st.divider()

    # -------------------- Layout: Session Distribution Pie Chart --------------------
    left_col, right_col = st.columns([2, 1])

    # LEFT COLUMN: Pie Chart
    with left_col:
        st.subheader("📊 Session Distribution by Network Slice")

        fig, ax = plt.subplots(figsize=(6, 6))

        # Explode URLLC slice slightly for emphasis
        explode = [0.05 if s == "URLLC" else 0 for s in slices]

        ax.pie(
            session_counts,
            labels=slices,
            autopct=lambda p: f"{p:.1f}%",
            startangle=90,
            explode=explode,
            shadow=True,
            wedgeprops={"edgecolor": "white"}
        )

        ax.set_title("📊 Sessions by Slice")
        ax.axis("equal")  # Ensure perfect circle
        st.pyplot(fig)
        logger.info("Rendered session distribution pie chart")

    # RIGHT COLUMN: Slice Metrics
    with right_col:
        st.markdown("### Number of Sessions per Slice")
        for slice_name, data in snssai_data.items():
            st.metric(label=f"{slice_name} Sessions", value=data["sessions"])

    st.caption("Data source: FastAPI 5G Core Analytics Service")
