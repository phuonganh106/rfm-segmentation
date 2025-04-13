import streamlit as st
st.set_page_config(page_title="Customer Segmentation Project", page_icon="📌")
st.title("🎯 Customer Segmentation Project")

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

# ====== EDA Section ======
st.markdown("<h5>🔎 Exploratory Data Analysis (EDA)</h5>", unsafe_allow_html=True)

# Tab 1: Customer Insights
tab1, tab2, tab3 = st.tabs(["Khách hàng", "Sản phẩm", "Giao dịch"])
with tab1:
    st.markdown("""
    **📌 Đặc điểm khách hàng:**
    - Số KH duy nhất: **3,898**
    - 56% KH tạo 80% doanh thu → Phân bổ không đồng đều.
    """)
    st.image("image/total_revenue_by_category.png", caption="Doanh thu theo tháng")
    st.image("image/revenue_distribution_by_customers.png", caption="Biểu đồ Pareto phân bổ doanh thu theo KH")

with tab2:
    st.markdown("""
    **📌 Phân tích sản phẩm:**
    - Top bán chạy: Sữa, rau củ, bánh mì.
    - Top bán chậm: Đồ chăm sóc thú cưng, snack.
    """)
    st.image("image/total_revenue_by_category.png", caption="Doanh thu theo danh mục")

with tab3:
    st.markdown("""
    **📌 Đặc điểm giao dịch:**
    - Giá trị đơn hàng trung bình: **$20-30**.
    - Mùa vụ rõ rệt (cao điểm Tết, năm học mới).
    """)
    st.image("image/transaction_by_month.png", caption="Số giao dịch theo tháng")
    st.image("image/total_distribution.png", caption="Giá trị đơn hàng")

# ====== RFM Calculation ======
st.markdown("<h5>📊 RFM Analysis</h5>", unsafe_allow_html=True)
st.markdown("""
**Công thức tính RFM:**
- **Recency (R)**: Khoảng thời gian từ lần mua cuối đến nay.
- **Frequency (F)**: Tổng số lần mua.
- **Monetary (M)**: Tổng chi tiêu.
""")
st.image("image/RFM.png", caption="Phân phối R/F/M")

# ====== Basket Analysis ======
st.markdown("<h5>🛒 Basket Analysis</h5>", unsafe_allow_html=True)
st.markdown("""
**Phát hiện chính:**
- Khách thường mua kèm **sữa + rau củ** hoặc **bánh mì + sữa**.
- Sản phẩm bán chậm vẫn xuất hiện trong giỏ hàng cùng sản phẩm chủ lực.
""")
st.image("image/top_20_basket_product.png", caption="Top 20 cặp sản phẩm mua cùng")

# ====== Next Page ======
st.markdown("---")
st.page_link("pages/2_📈_Project_s_Result.py", label="👉 **Next:** Kết quả Clustering và Chiến lược", icon="➡️")
