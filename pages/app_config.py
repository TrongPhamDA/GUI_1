# Hotel Data Science: Application Configuration Reference
"""
Configuration file containing default values for the hotel recommendation application.
This file centralizes all configurable parameters for easy maintenance and updates.
"""

# ------------------------------------------------------------------------------
# UI Configuration
# ------------------------------------------------------------------------------

# Main page header configuration
IMG_SRC = "https://play-lh.googleusercontent.com/V0UiCdeHUvWqto46My2GrMoCPZKVPUOLG8UpIQwP2FRLQ3kaEqT9V1Ufj6iQa4Sz5ck"
PAGE_TITLE = "Customer Segmentation"

# Page descriptions
DESCRIPTION_1 = "Boost loyalty and revenue with smart customer segmentation"
DESCRIPTION_2 = "powered by RFM and machine learning"

# ------------------------------------------------------------------------------
# File Paths
# ------------------------------------------------------------------------------

# Data files
TRANSACTIONS_CSV = "input/MLTT_01_df_trans_pre.csv"
RECENCY_FREQUENCY_MONETARY_CSV = "input/MLTT_02_df_RFM_scored.csv"

# Report files
FINAL_REPORT = "static/Final_Report.pdf"
FINAL_REPORT_IMAGES_DIR = "static/final_report/"
COL_NUM = 2

# Final report images directory
CHARTS_rfm = "static/chart/rfm/"
CHARTS_kmeans = "static/chart/kmeans/"
CHARTS_hierachical = "static/chart/hierachical/"

# Markdown: segment characteristics
MARKDOWN_rfm = "markdown/rfm_segment_desc.md"
MARKDOWN_kmeans = "markdown/kmeans_segment_desc.md"
MARKDOWN_hierachical = "markdown/hierachical_segment_desc.md"

# ------------------------------------------------------------------------------
# Owner Information
# ------------------------------------------------------------------------------

# Owner 1 - Phạm Ngọc Trọng
OWNER_1 = {
    "name": "Phạm Ngọc Trọng",
    "position": "Owner",
    "email": "phanlong.trong@gmail.com",
    "phone": "034 981 6784",
    "website": "https://www.facebook.com/TrongPhamDA",
    "image_src": "static/owner.png"
}

# Owner 2 - Trần Đình Hùng
OWNER_2 = {
    "name": "Trần Đình Hùng",
    "position": "Business Domain Advisor", 
    "email": "tdhung.dl@gmail.com",
    "phone": "000 0000 000",
    "website": "https://github.com/trandinhhung",
    "image_src": "static/team_member.png"
}

# Owner 3 - Khuất Phương
OWNER_3 = {
    "name": "Khuất Thùy Phương",
    "position": "Instructor",
    "email": "tubirona@gmail.com",
    "phone": "000 0000 000",
    "website": "https://github.com/khuatphuong",
    "image_src": "static/instructor.png"
}

# Combined owners list
OWNER = [OWNER_1, OWNER_2, OWNER_3]

# Project Information
PROJECT_INFO = {
    "title": "Customer Segmentation",
    "course": "DL07_K306",
    "submission_date": "13/09/2025",
    "university": "Data Science & Machine Learning Certificate"
}

# ------------------------------------------------------------------------------
# Display Configuration
# ------------------------------------------------------------------------------

# Footer display control
SHOW_FOOTER = True

# ------------------------------------------------------------------------------
# KMeans config
# ------------------------------------------------------------------------------
RANDOM_STATE = 42
K_OPT = 4