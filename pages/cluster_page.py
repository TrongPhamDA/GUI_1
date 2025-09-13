# ------------------------------------------------------------------------------
# Import libraries
# ------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import sys
import os
from sklearn.preprocessing import RobustScaler
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
import numpy as np
from sklearn.decomposition import PCA


# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from myfunctions import *
from app_config import *


# ------------------------------------------------------------------------------
# Read data
# ------------------------------------------------------------------------------
df = pd.read_csv(RECENCY_FREQUENCY_MONETARY_CSV, header=0, index_col=0)
df2 = pd.read_csv(RECENCY_FREQUENCY_MONETARY_CSV, header=0, index_col=0)
df3 = pd.read_csv(RECENCY_FREQUENCY_MONETARY_CSV, header=0, index_col=0)


# ------------------------------------------------------------------------------
# processing
# ------------------------------------------------------------------------------
RECENCY_MIN = int(df["recency"].min())
RECENCY_MAX = int(df["recency"].max())
RECENCY_DEFAULT = 45
RECENCY_STEP = 1

FREQUENCY_MIN = int(df["frequency"].min())
FREQUENCY_MAX = int(df["frequency"].max())
FREQUENCY_DEFAULT = 1
FREQUENCY_STEP = 1

MONETARY_MIN = int(df["monetary"].min())
MONETARY_MAX = int(df["monetary"].max())
MONETARY_DEFAULT = 90
MONETARY_STEP = 1


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
# User interface controls
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### RFM slider")
    recency = st.slider(
        "Recency",
        min_value=RECENCY_MIN,
        max_value=RECENCY_MAX,
        value=RECENCY_DEFAULT,
        step=RECENCY_STEP,
        format="%d days"
    )
    frequency = st.slider(
        "Frequency",
        min_value=FREQUENCY_MIN,
        max_value=FREQUENCY_MAX,
        value=FREQUENCY_DEFAULT,
        step=FREQUENCY_STEP,
        format="%d orders"
    )
    monetary = st.slider(
        "Monetary",
        min_value=MONETARY_MIN,
        max_value=MONETARY_MAX,
        value=MONETARY_DEFAULT,
        step=MONETARY_STEP,
        format="$ %d"
    )


# ------------------------------------------------------------------------------
# processing RFM Quartiles
# ------------------------------------------------------------------------------
# Sử dụng hàm fn_RFM_manual để tính nhãn RFM
r_label, f_label, m_label = fn_RFM_manual(sample_df=df, recency=recency, frequency=frequency, monetary=monetary)
rfm_fig, rfm_label_found = fn_chart_R_FM(figsize=(10, 6), dpi=150, r_label=r_label, f_label=f_label, m_label=m_label)


# ------------------------------------------------------------------------------
# processing KMeans Clustering
# ------------------------------------------------------------------------------
# new df cho model
df2 = df2[["customer_id", "recency", "frequency", "monetary"]]
customer_new = pd.DataFrame([{"customer_id": "new_customer", "recency": recency, "frequency": frequency, "monetary": monetary}])
df2 = pd.concat([df2, customer_new], ignore_index=True)
# log scale
df2["recency_log"] = np.log1p(df2["recency"])
df2["monetary_log"] = np.log1p(df2["monetary"])
# RobustScaler: scales but keeps outliers
scaler = RobustScaler()
df2[['recency_log_scaled','frequency_scaled','monetary_log_scaled']] = scaler.fit_transform(
    df2[['recency_log','frequency','monetary_log']]
)
df2_scaled = df2[['recency_log_scaled','frequency_scaled','monetary_log_scaled']]
# Build KMeans model with optimal k=4
kmeans_model = KMeans(
    n_clusters=K_OPT,
    random_state=RANDOM_STATE,
    n_init=10,
    max_iter=300,
    init='k-means++'
)
kmeans_model.fit(df2_scaled)
df2_scaled['cluster'] = kmeans_model.predict(df2_scaled)
df2['cluster'] = df2_scaled['cluster'].values
df2['cluster'] = df2['cluster'].astype(str)
# cluster order and colors
cluster_no = ["2", "1", "0", "3"]
cluster_order = ["Loyal", "Regular", "At-Risk", "Lost"]
cluster_colors = ["#66E0E0", "#6666FF", "#B0C4DE", "#FFB266"]
df2["cluster_label"] = df2["cluster"].map(dict(zip(map(str, cluster_no), cluster_order)))

    
# ------------------------------------------------------------------------------
# processing Hierachical Clustering
# ------------------------------------------------------------------------------
# new df cho model
df3 = df3[["customer_id", "recency", "frequency", "monetary"]]
customer_new = pd.DataFrame([{"customer_id": "new_customer", "recency": recency, "frequency": frequency, "monetary": monetary}])
df3 = pd.concat([df3, customer_new], ignore_index=True)
# log scale
df3["recency_log"] = np.log1p(df3["recency"])
df3["monetary_log"] = np.log1p(df3["monetary"])
# RobustScaler: scales but keeps outliers
scaler = RobustScaler()
df3[['recency_log_scaled','frequency_scaled','monetary_log_scaled']] = scaler.fit_transform(
    df3[['recency_log','frequency','monetary_log']]
)
df3_scaled = df3[['recency_log_scaled','frequency_scaled','monetary_log_scaled']]
# Build Agglomerative Clustering model with optimal k=4
agglo_model = AgglomerativeClustering(
    n_clusters=K_OPT,
    metric='euclidean',
    linkage='ward'
).fit_predict(df3_scaled)
df3_scaled['cluster'] = agglo_model
df3['cluster'] = df3_scaled['cluster'].values
df3['cluster'] = df3['cluster'].astype(str)
# cluster order and colors
cluster_no_3 = ["3", "2", "0", "1"]
cluster_order_3 = ["Loyal", "Regular", "At-Risk", "Lost"]
cluster_colors_3 = ["#66E0E0", "#6666FF", "#B0C4DE", "#FFB266"]
df3["cluster_label"] = df3["cluster"].map(dict(zip(map(str, cluster_no_3), cluster_order_3)))


# ------------------------------------------------------------------------------
# Tô màu cluster
# ------------------------------------------------------------------------------
def fn_get_cluster_color(label_or_num, cluster_no, cluster_order, cluster_colors):
    if str(label_or_num) in cluster_no:
        idx = cluster_no.index(str(label_or_num))
        return cluster_colors[idx]
    elif str(label_or_num) in cluster_order:
        idx = cluster_order.index(str(label_or_num))
        return cluster_colors[idx]
    else:
        return "#808080"



# ------------------------------------------------------------------------------
# processing PCA & chart - sử dụng dữ liệu đã scale có sẵn
# ------------------------------------------------------------------------------
# Sử dụng dữ liệu đã scale từ df3_scaled (đã được tạo ở phần Hierarchical Clustering)

# sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=labels.astype(str), palette="tab10", s=30, ax=ax, legend=True)
# sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=labels.astype(str), palette="tab10", s=30, ax=ax, legend=True)

# ------------------------------------------------------------------------------
# main program
# ------------------------------------------------------------------------------
# Overview input
fn_render_input(recency, frequency, monetary, font_size_rem=3.5)


# chia làm 3 cột
col_RFM, col_KMeans, col_Hierachical = st.columns(3)
with col_RFM:
    st.write("### **RFM Quartiles**")
    st.write("---")    
with col_KMeans:
    st.write("### **KMeans Clusters**")
    st.write("---")    
with col_Hierachical:
    st.write("### **Hierachical Clusters**")
    st.write("---")

# điền kết quả tính toán
col_RFM, col_KMeans, col_Hierachical = st.columns(3)
with col_RFM:
    col1, col2 = st.columns(2)
    with col1:
        st.write("Segment")
    with col2:
        st.write(f"#### {r_label}{f_label}{m_label}")
with col_KMeans:
    col1, col2 = st.columns(2)
    with col1:
        st.write("Cluster")
    with col2:
        st.write(f"#### {df2[df2['customer_id'] == 'new_customer']['cluster'].values[0]}")
with col_Hierachical:
    col1, col2 = st.columns(2)
    with col1:
        st.write("Cluster")
    with col2:
        st.write(f"#### {df3[df3['customer_id'] == 'new_customer']['cluster'].values[0]}")

# điền tên cluster
col_RFM, col_KMeans, col_Hierachical = st.columns(3)
with col_RFM:
    col1, col2 = st.columns(2)
    with col1:
        st.write("Label")
    with col2:
        st.write(f"#### {rfm_label_found}")
with col_KMeans:
    col1, col2 = st.columns(2)
    with col1:
        st.write("Label")
    with col2:
        st.write(f"#### {df2[df2['customer_id'] == 'new_customer']['cluster_label'].values[0]}")
with col_Hierachical:
    col1, col2 = st.columns(2)
    with col1:
        st.write("Label")
    with col2:
        st.write(f"#### {df3[df3['customer_id'] == 'new_customer']['cluster_label'].values[0]}")
# biểu đồ
col_RFM, col_KMeans, col_Hierachical = st.columns(3)
with col_RFM:
    st.write("R-FM Charts")
    st.pyplot(rfm_fig)
# Tạo dữ liệu chung cho PCA (sử dụng df3_scaled làm base)
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import silhouette_score

# Sử dụng cùng 1 bộ dữ liệu cho PCA
X_common = df3_scaled[['recency_log_scaled','frequency_scaled','monetary_log_scaled']].copy()
pca = PCA(n_components=2)
X_pca_common = pca.fit_transform(X_common)

# Tạo KMeans labels trên cùng dữ liệu
kmeans_common = KMeans(n_clusters=4, random_state=RANDOM_STATE, max_iter=100, n_init=10, tol=0.0001)
kmeans_labels_common = kmeans_common.fit_predict(X_common)
sil_kmeans = silhouette_score(X_common, kmeans_labels_common)

# Tạo Hierarchical labels trên cùng dữ liệu  
hier_common = AgglomerativeClustering(n_clusters=4, linkage="ward")
hier_labels_common = hier_common.fit_predict(X_common)
sil_hier = silhouette_score(X_common, hier_labels_common)

with col_KMeans:
    st.write("KMeans & PCA (k=2)")
    sns.set_style("whitegrid")
    sns.set_palette("tab10")
    
    fig_kmeans, ax_kmeans = plt.subplots(figsize=(6, 4))
    sns.scatterplot(x=X_pca_common[:, 0], y=X_pca_common[:, 1], hue=kmeans_labels_common.astype(str), s=30, ax=ax_kmeans, legend=True)
    # ax_kmeans.set_title(f"KMeans (k=4), Silhouette={sil_kmeans:.3f}")
    ax_kmeans.set_xlabel("PC1")
    ax_kmeans.set_ylabel("PC2")
    st.pyplot(fig_kmeans)

with col_Hierachical:
    st.write("Hierarchical PCA")
    fig_hier, ax_hier = plt.subplots(figsize=(6, 4))
    sns.scatterplot(x=X_pca_common[:, 0], y=X_pca_common[:, 1], hue=hier_labels_common.astype(str), s=30, ax=ax_hier, legend=True)
    # ax_hier.set_title(f"Hierarchical (k=4), Silhouette={sil_hier:.3f}")
    ax_hier.set_xlabel("PC1")
    ax_hier.set_ylabel("PC2")
    st.pyplot(fig_hier)

# đặc tính của segments
col_RFM, col_KMeans, col_Hierachical = st.columns(3)
with col_RFM:
    st.write("---")
    st.write("#### **Characteristics**")
    fn_chart_col(path=CHARTS_rfm, reverse=True)
with col_KMeans:
    st.write("---")
    st.write("####")
    fn_chart_col(path=CHARTS_kmeans)
with col_Hierachical:
    st.write("---")
    st.write("####")
    fn_chart_col(path=CHARTS_hierachical)

# đặc tính của segments: bằng chữ
# fn_read_markdown(path=MARKDOWN_rfm)
# fn_read_markdown(path=MARKDOWN_kmeans)
# fn_read_markdown(path=MARKDOWN_hierachical)


# ------------------------------------------------------------------------------
# Render footer
fn_render_footer(OWNER, PROJECT_INFO, SHOW_FOOTER)
# ------------------------------------------------------------------------------