import streamlit as st
import matplotlib.pyplot as plt
import requests
import logging

# -------------------- Logging Configuration --------------------
logger = logging.getLogger("dashboard_smf")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

# -------------------- API Endpoint --------------------
API_URL = "http://127.0.0.1:8000/smf"

def show_smf_page():
    """
    Renders the SMF KPI Summary page:
    - Displays PDU, Policy, and PFCP KPIs
    - Shows success/failure rates as a bar chart
    """
    st.title("📊 SMF KPI Summary")

    # -------------------- Fetch Data from API --------------------
    try:
        logger.info("Fetching SMF KPI data from API")
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        logger.debug(f"SMF KPI data fetched: {data}")
    except Exception as e:
        logger.exception("Failed to fetch SMF KPI data")
        st.error(f"Failed to fetch data from API: {e}")
        st.stop()

    # -------------------- Extract KPIs and Rates --------------------
    smf_kpis = data["kpis"]
    smf_rates = {
        "PDU Session Establishment Success": data["rates"]["PDU Session Establishment Success Rate"],
        "PDU Session Establishment Failure": data["rates"]["PDU Session Establishment Failure Rate"],
        "SM Policy Association Success": data["rates"]["SM Policy Association Success Rate"],
        "SM Policy Association Failure": data["rates"]["SM Policy Association Failure Rate"],
        "PFCP Session Success": data["rates"]["PFCP Session Success Rate"],
        "PFCP Session Failure": data["rates"]["PFCP Session Failure Rate"]
    }

    # -------------------- PDU Session KPIs --------------------
    st.markdown("🔹 **PDU Session KPIs**")
    col1, col2, col3 = st.columns(3)
    col1.metric("1️⃣ PDU Session Requests", smf_kpis["pdu_session_establishment_request"])
    col2.metric("2️⃣ PDU Sessions Established", smf_kpis["pdu_session_establishment_complete"])
    col3.metric("3️⃣ PDU Session Failures", smf_kpis["pdu_session_establishment_reject"])

    # -------------------- Policy Association KPIs --------------------
    st.markdown("🔹 **Policy Association KPIs**")
    col4, col5, col6 = st.columns(3)
    col4.metric("4️⃣ Policy Requests", smf_kpis["sm_policy_association_request"])
    col5.metric("5️⃣ Policy Success", smf_kpis["sm_policy_association_response"])
    col6.metric("6️⃣ Policy Failure", smf_kpis["sm_policy_association_failure"])

    # -------------------- PFCP Session KPIs --------------------
    st.markdown("🔹 **PFCP Session KPIs**")
    col7, col8, col9 = st.columns(3)
    col7.metric("7️⃣ PFCP Requests", smf_kpis["pfcp_session_establishment_request"])
    col8.metric("8️⃣ PFCP Success", smf_kpis["pfcp_session_establishment_response"])
    col9.metric("9️⃣ PFCP Failure", smf_kpis["pfcp_session_establishment_failure"])

    # -------------------- Success / Failure Rates Bar Chart --------------------
    st.subheader("📊 SMF Success and Failure Rates (%)")

    outcomes = list(smf_rates.keys())
    percentages = list(smf_rates.values())

    # Success → green, Failure → red
    colors = ["#28a745" if "Success" in outcome else "#dc3545" for outcome in outcomes]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(outcomes, percentages, color=colors)

    # Add percentage labels above each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # X coordinate
            height + 1,                          # Slightly above bar
            f"{height:.2f}%",                    # Label text
            ha="center",
            va="bottom"
        )

    ax.set_ylim(0, 100)
    ax.set_ylabel("Percentage (%)")
    ax.set_title("SMF PDU / Policy / PFCP Success & Failure Rates")

    # Rotate X-axis labels for readability
    plt.xticks(rotation=20, ha="right")

    st.pyplot(fig)
    logger.info("Rendered SMF KPI metrics and bar chart successfully")