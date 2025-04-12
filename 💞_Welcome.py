import streamlit as st

st.set_page_config(page_title="Introduction", page_icon="💞")
st.title("💞 Project Introduction")


# ====== CẤU HÌNH SIDEBAR ======
with st.sidebar:
    st.markdown("""
    **🎯 Segmentation Customer Project**
    *Made by:*
    👩‍💻 **Nguyễn Thị Mai Linh**
    👨‍💻 **Tô Nguyễn Phương Anh**
    *Instructed by:*
    👩‍🏫 **Nguyễn Khuất Thùy Phương**
    *April 2025*
    """)
    st.markdown("---")  # Đường phân cách


# Tạo khoảng trắng (20px)
st.markdown(
    """
    <style>
        .custom-space {
            margin-top: 20px;
            margin-bottom: 20px;
        }
    </style>
    <div class="custom-space"></div>
    """,
    unsafe_allow_html=True
)

# ====== Team & Project Overview ======
st.markdown("<h5>📄 Project Overview</h5>", unsafe_allow_html=True)
st.markdown("""
    Phân tích hành vi khách hàng của cửa hàng bán lẻ **X** (2014-2015) để:
    - Giảm tồn kho
    - Tối ưu chiến dịch marketing
    """)

# ====== Business Problems ======
st.markdown("<h5>📈 Business Challenges</h5>", unsafe_allow_html=True)
st.markdown("""
<div class="highlight-box">
✅ **Vấn đề chính:**
- 80% sản phẩm bán chậm thuộc nhóm **Personal Care, Pet Care, Snacks** → Tồn kho cao.
- 56% KH tạo 80% doanh thu nhưng chưa có chiến lược chăm sóc nhóm trọng điểm.
- Đơn hàng nhỏ (2-3 sản phẩm), chưa khuyến khích mua thêm.
</div>
""", unsafe_allow_html=True)

# ====== Proposed Methods ======
st.markdown("<h5>🔍 Proposed Solutions</h5>", unsafe_allow_html=True)
st.markdown("""
1. **Phân tích RFM + Clustering** để phân nhóm KH:
   - Kết hợp **K-means (Sklearn/PySpark)** và **Hierarchical Clustering**.
   - So sánh kết quả với **Manual Segmentation** (luật tự định nghĩa).

2. **Basket Analysis** để phát hiện sản phẩm hay mua cùng:
   - Tạo combo sản phẩm từ top cặp mua kèm (VD: sữa + rau củ).
""")

# ====== Dataset Preview ======
st.markdown("<h5>📦 Dataset Snapshot</h5>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.image("/content/drive/MyDrive/DL07_K302_ToNguyenPhuongAnh/GUI/image/transaction.png", caption="Giao dịch (38,765 records)")
with col2:
    st.image("/content/drive/MyDrive/DL07_K302_ToNguyenPhuongAnh/GUI/image/product.png", caption="Sản phẩm (167 items)")

# ====== Next Page ======
st.markdown("---")
st.page_link("/content/drive/MyDrive/DL07_K302_ToNguyenPhuongAnh/GUI/pages/1_📌_Customer_Segmentation_Project.py", label="👉 **Next:** Khám phá EDA và Phân tích RFM", icon="➡️")
