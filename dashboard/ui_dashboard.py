import streamlit as st
import logging

# -------------------- Logging Configuration --------------------
logger = logging.getLogger("dashboard")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

# -------------------- UI Page Imports --------------------
from ui_summary import show_summary_page
from ui_amf import show_amf_page
from ui_smf import show_smf_page

# -------------------- Streamlit Page Config --------------------
st.set_page_config(
    page_title="5G Core KPI Dashboard",
    layout="wide"  # Use wide layout for metrics + charts
)

# -------------------- Page Selection Sidebar --------------------
pages = {
    "Overview": show_summary_page,
    "AMF": show_amf_page,
    "SMF": show_smf_page
}

selected_page = st.sidebar.selectbox(
    "Select View",                # Sidebar title
    options=list(pages.keys()),   # Dropdown options
    index=0                       # Default to "Overview"
)

# Log the selected page
logger.info(f"User selected dashboard page: {selected_page}")

# -------------------- Render the Selected Page --------------------
try:
    pages[selected_page]()  # Call the corresponding function to render the page
    logger.info(f"Rendered {selected_page} page successfully")
except Exception as e:
    # Log any unexpected errors during page rendering
    logger.exception(f"Failed to render {selected_page} page: {e}")
    st.error(f"Failed to load {selected_page} page. Please try again.")
