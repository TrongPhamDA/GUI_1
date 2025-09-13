# ------------------------------------------------------------------------------
# Import libraries
# ------------------------------------------------------------------------------
import streamlit as st

# ------------------------------------------------------------------------------
# Page definitions
# ------------------------------------------------------------------------------
home_page = st.Page("pages/home_page.py", title="Get started", icon=":material/launch:")
cluster_page = st.Page("pages/cluster_page.py", title="Customer segmentation", icon=":material/people:")
cluster_desc_page = st.Page("pages/cluster_desc_page.py", title="Segment description", icon=":material/people:")
info_page = st.Page("pages/final_report_page.py", title="Final report", icon=":material/book:")

# ------------------------------------------------------------------------------
# Navigation structure
# ------------------------------------------------------------------------------
pg = st.navigation(
    {
        "Get Started": [home_page],
        "Segment clustering": [cluster_page, cluster_desc_page],
        "About This Project": [info_page],
    }
)

# ------------------------------------------------------------------------------
# App configuration
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Customer Segmentation",
    page_icon=":material/shopping_cart:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"Get Help": "mailto:phanlong.trong@gmail.com"},
)

# ------------------------------------------------------------------------------
# Run application
# ------------------------------------------------------------------------------
pg.run()
