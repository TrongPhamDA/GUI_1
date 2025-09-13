# Hotel Data Science Functions
import streamlit as st
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import os
import sys

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app_config import *


# ------------------------------------------------------------------------------
# Render main page header
# ------------------------------------------------------------------------------
def fn_render_mainpage_header(img_src, page_title, description_1, description_2):
    st.markdown(
        f"""
    <div style="background: #fff; border-radius: 18px; box-shadow: 0 4px 24px rgba(30,60,114,0.10); padding: 2.5rem 2rem 2rem 2rem; margin-bottom: 2.5rem;">
        <div style="display: flex; align-items: center;">
            <div style="flex: 0 0 140px; display: flex; align-items: center; justify-content: center; background: #f5f7fa; border-radius: 12px; height: 120px; margin-right: 2.5rem;">
                <img src="{img_src}" width="100" style="display: block;">
            </div>
            <div style="flex: 1;">
                <h1 style="color: #1e3c72; margin-bottom: 0.7rem; font-size: 2.1rem; font-weight: 700; letter-spacing: 0.5px;">
                    {page_title}
                </h1>
                <p style="color: #2a5298; font-size: 1.15rem; margin-bottom: 0.7rem; font-weight: 500;">
                    {description_1}<br>
                    <strong>{description_2}</strong>
                </p>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------------------------
# Render footer
# ------------------------------------------------------------------------------
def fn_render_footer(owner_list, project_info, show_footer=True):
    """
    Render website footer with owner information and project details
    
    Args:
        owner_list: List of owner dictionaries
        project_info: Dictionary with project information
        show_footer: Boolean to control footer display
    """
    if not show_footer:
        return

    # Footer Bottom Section
    st.markdown("---")
    st.markdown(f"© 2025 {project_info['title']}")
    
    # Create columns for owners
    owner_columns = st.columns(len(owner_list))
    
    # Render each owner using loop
    for idx, owner in enumerate(owner_list):
        with owner_columns[idx]:
            # Create two columns for each owner: left for image, right for info
            col_img, col_info = st.columns([1, 2])
            
            with col_img:
                # Display owner image
                st.image(owner['image_src'], caption="")
            
            with col_info:
                # Display owner information
                st.markdown(
                    f"""
                    <div style="padding: 0.5rem;">
                        <div style="font-weight: 600; color: #1e3c72; margin-bottom: 0.3rem; font-size: 1rem;">{owner['name']}</div>
                        <div style="font-style: italic; color: #6c757d; margin-bottom: 0.4rem; font-size: 0.85rem;">{owner['position']}</div>
                        <div style="color: #495057; font-size: 0.8rem; margin-bottom: 0.2rem;">{owner['email']}</div>
                        <div style="color: #495057; font-size: 0.8rem; margin-bottom: 0.2rem;">{owner['phone']}</div>
                        <a href="{owner['website']}" style="color: #007bff; text-decoration: none; font-size: 0.8rem;">GitHub Profile</a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    st.write("---")


# ------------------------------------------------------------------------------
# PDF Display Functions
# ------------------------------------------------------------------------------

def fn_display_report(pdf_path, images_dir, col_num = 2):
    """Display PDF report with download option and images viewer"""
    with open(pdf_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
    
    st.download_button("📄 Download Final Report (PDF)", pdf_bytes, "Final_Report.pdf", "application/pdf")
    st.markdown("---")
    
    st.markdown("#### Slides")
    images_per_row = col_num
    
    # Lấy danh sách tất cả file ảnh trong thư mục và sắp xếp theo thứ tự a-z
    image_files = sorted(glob.glob(f"{images_dir}*.png"))
    
    for idx, image_path in enumerate(image_files):
        if idx % images_per_row == 0:
            cols = st.columns(images_per_row)
        
        with cols[idx % images_per_row]:
            try:
                # Lấy tên file từ đường dẫn
                filename = os.path.basename(image_path)
                st.image(image_path, use_container_width=True, caption=filename)
            except Exception as e:
                st.error(f"Không thể hiển thị ảnh {filename}: {str(e)}")


# ------------------------------------------------------------------------------
# Render input
# ------------------------------------------------------------------------------
def fn_render_input(recency, frequency, monetary, font_size_rem=2.2):
    st.markdown("### Overview input")
    st.markdown("""
    <div style="display: flex; justify-content: space-between; margin-bottom: 2rem;">
      <div style="flex:1; background: #f5f7fa; border-radius: 14px; margin: 0 0.5rem; padding: 1.2rem 0.5rem; text-align: center; box-shadow: 0 2px 8px rgba(30,60,114,0.07);">
        <div style="font-size: 1.05rem; color: #2a5298; font-weight: 500; margin-bottom: 0.2rem;">Recency</div>
        <div style="font-size: {font_size_rem}rem; font-weight: 700; color: #1e3c72;">{recency:,}</div>
        <div style="font-size: 0.95rem; color: #888;">days</div>
      </div>
      <div style="flex:1; background: #f5f7fa; border-radius: 14px; margin: 0 0.5rem; padding: 1.2rem 0.5rem; text-align: center; box-shadow: 0 2px 8px rgba(30,60,114,0.07);">
        <div style="font-size: 1.05rem; color: #2a5298; font-weight: 500; margin-bottom: 0.2rem;">Frequency</div>
        <div style="font-size: {font_size_rem}rem; font-weight: 700; color: #1e3c72;">{frequency:,}</div>
        <div style="font-size: 0.95rem; color: #888;">orders</div>
      </div>
      <div style="flex:1; background: #f5f7fa; border-radius: 14px; margin: 0 0.5rem; padding: 1.2rem 0.5rem; text-align: center; box-shadow: 0 2px 8px rgba(30,60,114,0.07);">
        <div style="font-size: 1.05rem; color: #2a5298; font-weight: 500; margin-bottom: 0.2rem;">Monetary</div>
        <div style="font-size: {font_size_rem}rem; font-weight: 700; color: #1e3c72;">${monetary:,}</div>
        <div style="font-size: 0.95rem; color: #888;">amount total</div>
      </div>
    </div>
    """.format(
        recency=recency,
        frequency=frequency,
        monetary=monetary,
        font_size_rem=font_size_rem
    ), unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# RFM Analysis Functions
# ------------------------------------------------------------------------------
def fn_RFM_manual(sample_df, recency, frequency, monetary):
    def get_label(val, quantiles, labels):
        return labels[np.searchsorted(quantiles, val, side="left")]

    quantiles_r = np.quantile(sample_df["recency"].drop_duplicates(), [0.25, 0.5, 0.75, 1.0])
    quantiles_f = np.quantile(sample_df["frequency"].drop_duplicates(), [0.25, 0.5, 0.75, 1.0])
    quantiles_m = np.quantile(sample_df["monetary"].drop_duplicates(), [0.25, 0.5, 0.75, 1.0])

    r_label = get_label(recency, quantiles_r, [4, 3, 2, 1])
    f_label = get_label(frequency, quantiles_f, [1, 2, 3, 4])
    m_label = get_label(monetary, quantiles_m, [1, 2, 3, 4])

    return int(r_label), int(f_label), int(m_label)


# ------------------------------------------------------------------------------
# RFM Chart
# ------------------------------------------------------------------------------
def fn_chart_R_FM(figsize, dpi, r_label, f_label, m_label):
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    segments = [
        (1, 1, 1, 3, "Lost", "#FFB266"),
        (1, 4, 2, 1, "Can't\nLose\nThem", "#FF6666"),
        (2, 1, 1, 3, "Needs\nAttention", "#6666FF"),
        (3, 3, 2, 2, "Loyal", "#66E0E0"),
        (3, 1, 2, 2, "Potential", "#B0C4DE"),
        (4, 1, 1, 1, "New", "#3399FF"),
        (4, 4, 1, 1, "Champions", "#008080"),
    ]
    label_found = None
    x_point = r_label
    y_point = (f_label + m_label) / 2
    for x, y, w, h, label, color in segments:
        rect = patches.Rectangle(
            (x - 0.5, y - 0.5), w, h, linewidth=1, edgecolor="black", facecolor=color
        )
        ax.add_patch(rect)
        ax.text(
            x - 0.5 + w / 2,
            y - 0.5 + h / 2,
            label,
            ha="center",
            va="center",
            fontsize=9,
            weight="bold",
        )
        # Kiểm tra xem điểm (x_point, y_point) có nằm trong segment này không
        if (x - 0.5) <= x_point <= (x - 0.5 + w) and (y - 0.5) <= y_point <= (y - 0.5 + h):
            label_found = label.replace('\n', ' ')
    ax.set_xlim(0.5, 4.5)
    ax.set_ylim(0.5, 4.5)
    ax.set_xticks([1, 2, 3, 4])
    ax.set_yticks([1, 2, 3, 4])
    ax.set_xlabel("R")
    ax.set_ylabel("( F + M ) / 2")
    map_title = "R(FM) Segments Map"
    ax.set_title(map_title)
    ax.scatter(
        x_point, y_point, 
        s=180, 
        color='red', 
        edgecolor='black', 
        linewidth=2, 
        zorder=10
    )
    # st.pyplot(fig)
    return fig,label_found


# ------------------------------------------------------------------------------
# Show images in a column
# ------------------------------------------------------------------------------
def fn_chart_col(path, reverse=False, show_caption=False):
    image_files = sorted(glob.glob(f"{path}*.png"), reverse=reverse)
    if not image_files:
        st.warning(f"Không có chart nào: {path}")
        return
    for image_path in image_files:
        filename = os.path.basename(image_path)
        st.image(image_path, caption=filename if show_caption else None, use_container_width=True)


# ------------------------------------------------------------------------------
# KMeans input functions
# ------------------------------------------------------------------------------
def fn_kmeans_preprocessing(recency, frequency, monetary):
    def fn_log1p(x):
        return np.log(x + 1)

    # preprocessing
    # log
    recency_log = fn_log1p(recency)
    monetary_log = fn_log1p(monetary)
    # robust scaler
    # Nếu dùng RobustScaler() cho 1 giá trị đơn, scaler sẽ trả về 0.0 vì giá trị duy nhất đó được coi là median, và mọi giá trị đều bị chuẩn hóa về 0.
    recency_robust = fn_robust_scaler(np.array([[recency_log]]))[0][0]  # Kết quả sẽ luôn là 0.0


# ------------------------------------------------------------------------------
# Read markdown table
# ------------------------------------------------------------------------------
def fn_read_markdown(path: str):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    table_lines = [line.strip() for line in lines if "|" in line]
    table_lines = [line for line in table_lines if not set(line.replace("|", "").strip()) <= {"-", ":"}]
    table_data = [line.strip("|").split("|") for line in table_lines]
    table_data = [[col.strip() for col in row] for row in table_data]
    df = pd.DataFrame(table_data[1:], columns=table_data[0])
    return df