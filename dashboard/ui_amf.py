import streamlit as st
import matplotlib.pyplot as plt
import requests
import logging

# -------------------- Logging Configuration --------------------
logger = logging.getLogger("dashboard_amf")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

# -------------------- API Endpoint --------------------
API_URL = "http://127.0.0.1:8000/amf"

def show_amf_page():
    """
    Renders the AMF KPI Summary page:
    - Displays registration & authentication KPIs
    - Shows success/failure rates as a bar chart
    """
    st.title("📊 AMF KPI Summary")

    # -------------------- Fetch Data from API --------------------
    try:
        logger.info("Fetching AMF KPI data from API")
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        logger.debug(f"AMF KPI data fetched: {data}")
    except Exception as e:
        logger.exception("Failed to fetch AMF KPI data")
        st.error(f"Failed to fetch data from API: {e}")
        st.stop()

    # -------------------- Extract KPIs and Rates --------------------
    kpis = data["kpis"]
    rates = {
        "Registration Success": data["rates"]["Registration Success Rate"],
        "Registration Failure": data["rates"]["Registration Failure Rate"],
        "Authentication Success": data["rates"]["Authentication Success Rate"],
        "Authentication Failure": data["rates"]["Authentication Failure Rate"]
    }

    # -------------------- Registration KPIs --------------------
    st.markdown("🔹 **Registration KPIs**")
    col1, col2, col3 = st.columns(3)
    col1.metric("1️⃣ Registration Requests Received", kpis["registration_request"])
    col2.metric("2️⃣ Registration Success", kpis["registration_success"])
    col3.metric("3️⃣ Registration Reject", kpis["registration_reject"])

    # -------------------- Authentication KPIs --------------------
    st.markdown("🔹 **Authentication KPIs**")
    col4, col5, col6 = st.columns(3)
    col4.metric("4️⃣ Authentication Requests", kpis["authentication_request"])
    col5.metric("5️⃣ Authentication Success", kpis["authentication_success"])
    col6.metric("6️⃣ Authentication Failure", kpis["authentication_failure"])

    # -------------------- Success / Failure Rates Bar Chart --------------------
    st.subheader("📊 AMF Success and Failure Rates (%)")

    outcomes = list(rates.keys())
    percentages = list(rates.values())

    # Success → green, Failure → red
    colors = ["#28a745" if "Success" in outcome else "#dc3545" for outcome in outcomes]

    # Create the bar chart
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(outcomes, percentages, color=colors)

    # Add percentage labels above each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # X coordinate
            height + 1,                          # Slightly above bar
            f'{height:.2f}%',                    # Label text
            ha='center',
            va='bottom'
        )

    ax.set_ylim(0, 100)
    ax.set_ylabel("Percentage (%)")
    ax.set_title("AMF Registration & Authentication Success / Failure Rates")

    # Rotate X-axis labels for readability
    plt.xticks(rotation=20, ha="right")

    st.pyplot(fig)
    logger.info("Rendered AMF KPI metrics and bar chart successfully")
