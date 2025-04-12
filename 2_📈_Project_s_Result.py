import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Result", page_icon="📊")
st.title("📊 Result of the project")

# ====== GIỚI THIỆU MÔ HÌNH ======
st.markdown("""
<h3 style='border-bottom: 1px solid #ff4b4b; padding-bottom: 8px;'>1. Giới Thiệu Thuật Toán KMeans</h3>
""", unsafe_allow_html=True)

st.markdown("""
**KMeans** là thuật toán học máy không giám sát, tự động nhóm các khách hàng có hành vi tương đồng vào cùng cụm.
Ứng dụng trong phân khúc khách hàng:
- 🔍 Phát hiện nhóm khách hàng ẩn dựa trên RFM
- 🎯 Hiểu đặc điểm từng phân khúc (tần suất mua, chi tiêu,...)
- ✨ Cá nhân hóa chiến dịch marketing
""")

# ====== DỮ LIỆU MẪU (thay bằng data thực tế của bạn) ======
cluster_data = pd.DataFrame({
    "Cluster": ["Loyal", "Dormant", "VIP", "At Risk"],
    "RecencyMean": [119, 427, 89, 124],
    "FrequencyMean": [5, 2, 7, 3],
    "MonetaryMean": [110, 45, 194, 51],
    "Count": [1252, 889, 460, 1297],
    "Percent": [32.12, 22.81, 11.80, 33.27]
})

# ====== PHẦN 1: TỔNG QUAN KẾT QUẢ ======
st.markdown("""
<h3 style='border-bottom: 2px solid #ff4b4b; padding-bottom: 8px;'>1. Tổng Quan Phân Cụm</h3>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.image("/content/drive/MyDrive/DL07_K302_ToNguyenPhuongAnh/GUI/image/Elbow_sklearn.png", caption="Elbow method")
    st.markdown("""
    **Thuật toán:** K-Means (Sklearn)
    **Số cụm tối ưu:** 4 (Elbow Method)
    """)

with col2:
    st.markdown("""
    **Tổng khách hàng:** 3,898
    **Biến sử dụng:** Recency (R), Frequency (F), Monetary (M)
    """)

# ====== PHẦN 2: TRỰC QUAN HÓA DỮ LIỆU ======
st.markdown("""
<h3 style='border-bottom: 2px solid #ff4b4b; padding-bottom: 8px;'>2. Biểu Đồ Phân Cụm</h3>
""", unsafe_allow_html=True)

# Tạo bubble chart với Plotly
fig = px.scatter(
    cluster_data,
    x="RecencyMean",
    y="MonetaryMean",
    size="Count",
    color="Cluster",
    hover_name="Cluster",
    hover_data={"FrequencyMean": True},
    labels={
        "RecencyMean": "Recency (ngày)",
        "MonetaryMean": "Monetary ($)",
        "FrequencyMean": "Frequency"
    },
    title="Phân Bổ 4 Nhóm Khách Hàng Theo RFM"
)
st.plotly_chart(fig, use_container_width=True)

st.image("/content/drive/MyDrive/DL07_K302_ToNguyenPhuongAnh/GUI/image/Sklearn_kmeans.png", caption="Tree map")

# ====== PHẦN 3: BẢNG KẾT QUẢ CHI TIẾT ======
st.markdown("""
<h3 style='border-bottom: 2px solid #ff4b4b; padding-bottom: 8px;'>3. Chi Tiết Các Nhóm Khách Hàng</h3>
""", unsafe_allow_html=True)

# Hiển thị bảng dữ liệu
st.dataframe(
    cluster_data.style.format({
        "RecencyMean": "{:.0f}",
        "MonetaryMean": "{:.0f}",
        "Percent": "{:.2f}%"
    }),
    column_config={
        "Cluster": "Nhóm KH",
        "RecencyMean": "Recency (ngày)",
        "FrequencyMean": "Frequency",
        "MonetaryMean": "Monetary ($)",
        "Count": "Số lượng",
        "Percent": "Tỷ lệ"
    },
    hide_index=True,
    use_container_width=True
)

# ====== PHẦN 4: INSIGHTS VÀ CHIẾN LƯỢC ======
st.markdown("""
<h3 style='border-bottom: 2px solid #ff4b4b; padding-bottom: 8px;'>4. Insights & Chiến Lược Marketing</h3>
""", unsafe_allow_html=True)

# Tạo tabs cho từng nhóm
tab1, tab2, tab3, tab4 = st.tabs(["VIP", "Loyal", "At Risk", "Dormant"])

with tab1:
    st.markdown("""
    **🔴 Đặc điểm:**
    - Recency thấp nhất (89 ngày)
    - Chi tiêu cao nhất ($194/đơn)
    - Tần suất mua: 7 lần

    **🎯 Chiến lược:**
    - Ưu đãi đặc biệt (VIP membership)
    - Early access sản phẩm mới
    - Quà tặng cao cấp dịp đặc biệt
    """)

with tab2:
    st.markdown("""
    **🔵 Đặc điểm:**
    - Recency trung bình (119 ngày)
    - Chi tiêu ổn định ($110/đơn)
    - Tần suất mua: 5 lần

    **🎯 Chiến lược:**
    - Chương trình tích điểm thưởng
    - Gói subscription định kỳ
    - Ưu đãi combo sản phẩm
    """)

with tab3:
    st.markdown("""
    **🟠 Đặc điểm:**
    - Recency cao (124 ngày)
    - Chi tiêu thấp ($51/đơn)
    - Tần suất mua: 3 lần

    **🎯 Chiến lược:**
    - Email win-back campaign
    - Freeship cho đơn tiếp theo
    - Flash sale sản phẩm yêu thích
    """)

with tab4:
    st.markdown("""
    **⚫ Đặc điểm:**
    - Recency rất cao (427 ngày)
    - Chi tiêu thấp nhất ($45/đơn)
    - Tần suất mua: 2 lần

    **🎯 Chiến lược:**
    - Khuyến mãi sốc (50% off)
    - Survey lý do không quay lại
    - Target quảng cáo lại
    """)

# ====== Next Page ======
st.markdown("---")
st.page_link("/content/drive/MyDrive/DL07_K302_ToNguyenPhuongAnh/GUI/pages/3_🧮_GUI.py", label="👉 **Next:** Customer Segmentation App", icon="➡️")
