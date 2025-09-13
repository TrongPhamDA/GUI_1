# ------------------------------------------------------------------------------
# Import libraries
# ------------------------------------------------------------------------------
import streamlit as st
import sys
import os


# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from myfunctions import *
from app_config import *


# ------------------------------------------------------------------------------
# Render main page header
# ------------------------------------------------------------------------------
fn_render_mainpage_header(
    img_src=IMG_SRC,
    page_title=PAGE_TITLE,
    description_1=DESCRIPTION_1,
    description_2=DESCRIPTION_2,
)


# ------------------------------------------------------------------------------
# Read data
# ------------------------------------------------------------------------------
st.write("RFM Quartiles")
df_rfm = fn_read_markdown(MARKDOWN_rfm)
df_rfm['Cluster'] = df_rfm.index
df_rfm = df_rfm[['Cluster'] + [col for col in df_rfm.columns if col != 'Cluster']]
st.write(df_rfm)

st.write("KMeans Clusters")
st.write(fn_read_markdown(MARKDOWN_kmeans))

st.write("Hierachical Clusters")
st.write(fn_read_markdown(MARKDOWN_hierachical))

# ------------------------------------------------------------------------------
# Render footer
fn_render_footer(OWNER, PROJECT_INFO, SHOW_FOOTER)
# ------------------------------------------------------------------------------