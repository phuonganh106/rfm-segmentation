import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from sklearn.preprocessing import RobustScaler

st.set_page_config(page_title="GUI", page_icon="🔮")

# ====== SIDEBAR ======
with st.sidebar:
    st.markdown("""
    **🎯 Segmentation Customer Project**

    
    *Made by:*
    
    👩‍💻 **Nguyễn Thị Mai Linh**
    
    👨‍💻 **Tô Nguyễn Phương Anh**

    
    *Instructed by:*
    👩‍🏫 **Khuất Thùy Phương**
    
    *April 2025*
    """)
    st.markdown("---")  # Đường phân cách

# 1. Load model & sample data
try:
  kmeans_model = joblib.load('kmeans_model.pkl')
  scaler = joblib.load('scaler.pkl')

  sample_data = pd.read_csv('RFM_data.csv', header=0)
  customer_dict = sample_data.set_index('Member_number').to_dict('index')

  st.session_state.update({
      'model': kmeans_model,
      'scaler': scaler,
      'customer_dict': customer_dict
  })
except Exception as e:
  st.error(f"Error loading model: {str(e)}")
  st.stop()

# 2. Display model's information
with st.expander("ℹ️ Model's Information"):
  st.write("**Model is using now:**")
  st.write(f"- Clustering: {kmeans_model.n_clusters}")
  st.write(f"- Algorithm: {kmeans_model.__class__.__name__}")
  st.write(f"- Scaler: {scaler.__class__.__name__}")

  st.markdown("""
  **Segmentation Criteria:**

  - **Recency (R):** Days since last purchase
  - **Frequency (F):** Total number of transactions
  - **Monetary (M):** Total spending amount
  """)

  st.markdown("""
    **Cluster Characteristics:**
    
    | Segment   | Avg Recency | Avg Frequency | Avg Monetary |
    |-----------|-------------|---------------|--------------|
    | Dormant   | 427 days    | 2 orders      | $45          |
    | At Risk   | 124 days    | 3 orders      | $51          |
    | Loyal     | 119 days    | 5 orders      | $110         |
    | VIP       | 89 days     | 7 orders      | $194         |
    """)
    
  st.write("**Training data's information**")
  st.write(f"- Number of customers: {len(sample_data)}")
  st.write("- Number of transaction: 14962")
  st.write("**Clustering distribution:**")
  st.bar_chart(sample_data['Cluster'].value_counts())

# 3. Input data option
st.title("🔮 Customer Segmention RFM")

st.markdown("<h5>Choose input method:</h5>", unsafe_allow_html=True)
input_method = st.radio(
    "",
    options=[
        "🔎 Search by MemberID",
        "✍️ Input R,F,M information",
        "📤 Upload file (csv, excel)"
    ],
    horizontal=True
)

# 4. Input data method
if input_method == "🔎 Search by MemberID":
    st.markdown("<h5>Searching Customer's Information</h5>", unsafe_allow_html=True)

    # Load sample customer IDs
    try:
      customer_ids_df = pd.read_csv('customer.csv')
      sample_customers = customer_ids_df.head(18)
      
      st.markdown("**Sample Customer IDs:**")

      # CSS grid 
      st.markdown("""
      <style>
      .member-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
          gap: 10px;
          margin: 15px 0;
      }
      .member-item {
        background: #f0f2f6;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        font-family: monospace;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
      }
      .member-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
      }
      </style>
      """, unsafe_allow_html=True)

      # Create grid
      members_html = "<div class='member-grid'>" + \
        "".join([f"<div class='member-item'>{m}</div>" for m in sample_customers['Member_number']]) + \
        "</div>"
      st.markdown(members_html, unsafe_allow_html=True)

    except Exception as e:
      st.warning(f"Could not load customer IDs: {str(e)}")

    col1, col2 = st.columns([3, 1])
    with col1:
      customer_id = st.text_input("Enter customer ID:", 
                                      placeholder="Ex: 3949")
    with col2:
      st.write("")
      st.write("")
      search_clicked = st.button("🔍 Search")

    if search_clicked:
      if customer_id.strip() == "":
        st.warning("Please enter a customer ID")
      else:
        try:
          customer_id = int(customer_id)
          if customer_id in st.session_state.customer_dict:
            customer_info = st.session_state.customer_dict[customer_id]

            # Load transaction history
            try:
              transactions_df = pd.read_csv('customer_transaction.csv')
              customer_transactions = transactions_df[transactions_df['Member_number'] == customer_id].reset_index(drop=True)
                            
              if not customer_transactions.empty:
                st.markdown("### Transaction History")

                cols_to_show = {
                    'Member_number': 'Customer ID',
                    'Date': 'Purchase Date',
                    'productName': 'Product',
                    'Revenue': 'Price',
                    'items': 'Quantity'
                }

                with st.container():
                  st.dataframe(customer_transactions.rename(columns=cols_to_show)[cols_to_show.values()],
                                height=200,
                                column_config={
                                    "Price": st.column_config.NumberColumn(format="$%.2f"),
                                    "Purchase Date": st.column_config.DateColumn(format="YYYY-MM-DD")
                                },
                                use_container_width=True
                  )
            except Exception as e:
              st.warning(f"Could not load transaction history: {str(e)}")

                # Display customer details
            st.markdown("### Customer RFM Details")
            with st.container():
              col1, col2, col3 = st.columns([1, 1, 1])
              with col1:
                st.metric("Recency", customer_info['Recency'], help="Days since last purchase")
              with col2:
                st.metric("Frequency", customer_info['Frequency'], help="Total transactions")
              with col3:
                st.metric("Monetary", f"${customer_info['Monetary']:,.0f}", help="Total spending")

            # Segmentation prediction
            X = [[customer_info['Recency'], customer_info['Frequency'], customer_info['Monetary']]]
            X_scaled = st.session_state.scaler.transform(X)
            cluster = st.session_state.model.predict(X_scaled)[0]

            segment_names = {
                  0: "Loyal",
                  1: "Dormant",
                  2: "VIP",
                  3: "At Risk"
            }
            st.success(f"**Customer segmentation:** {segment_names[cluster]}")

          else:
            st.warning("Customer ID not found. Please try another ID.")
        except ValueError:
          st.error("Please enter a valid numeric customer ID")

elif input_method == "✍️ Input R,F,M information":
    st.markdown("<h5>Input R,F,M information</h5>", unsafe_allow_html=True)

    # Initialize session state for storing entries if not exists
    if 'rfm_entries' not in st.session_state:
        st.session_state.rfm_entries = pd.DataFrame(columns=['Recency', 'Frequency', 'Monetary'])

    st.markdown("""
    ##### 📋 Input Guidelines

    **For optimal segmentation results, please follow these recommendations when entering values:**

    <div style="background:#f8f9fa; padding:15px; border-radius:8px; margin-top:10px">
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
            <div style="border-left: 3px solid #3498db; padding-left: 10px;">
                <h6 style="margin:0; color:#2c3e50">🕒 Recency</h6>
                <p style="margin:5px 0"><b>Range:</b> 1-500 days</p>
                <p style="margin:5px 0"><i>Example values:</i></p>
                <ul style="margin-top:5px; padding-left:20px">
                    <li>Recent: 1-30 days</li>
                    <li>Moderate: 31-90 days</li>
                </ul>
            </div>

            <div style="border-left: 3px solid #e74c3c; padding-left:10px;">
                <h6 style="margin:0; color:#2c3e50">🔢 Frequency</h6>
                <p style="margin:5px 0"><b>Range:</b> 1-30 orders</p>
                <p style="margin:5px 0"><i>Example values:</i></p>
                <ul style="margin-top:5px; padding-left:20px">
                    <li>New: 1-2 orders</li>
                    <li>Regular: 3-5 orders</li>
                </ul>
            </div>

            <div style="border-left: 3px solid #2ecc71; padding-left: 10px;">
                <h6 style="margin:0; color:#2c3e50">💰 Monetary</h6>
                <p style="margin:5px 0"><b>Range:</b> $1-$1000</p>
                <p style="margin:5px 0"><i>Example values:</i></p>
                <ul style="margin-top:5px; padding-left:20px">
                    <li>Small: $1-$50</li>
                    <li>Medium: $51-$200</li>
                </ul>
            </div>
        </div>

        <div style="margin-top:15px; padding:10px; background:#fff8e6; border-radius:5px">
            <small>💡 <b>Tip:</b> Compare your input with our <a href="#model-s-information">segment benchmarks</a> above for reference.</small>
        </div>
    </div>   
    """, unsafe_allow_html=True)

    # Input form
    with st.form("input_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            recency = st.number_input("Recency (days)", min_value=1, max_value=500, value=0, step=1)
        with col2:
            frequency = st.number_input("Frequency (times)", min_value=1, max_value=30, value=0, step=1)
        with col3:
            monetary = st.number_input("Monetary (USD)", min_value=1.0, max_value=1000.0, value=0.0)

        submitted = st.form_submit_button("➕ Add Entry")

    # Handle form submission
    if submitted:
      if recency <= 0 or frequency <= 0 or monetary <= 0:
        st.error("All values must be greater than 0! Please check your input.")
      else:
        new_entry = pd.DataFrame([[recency, frequency, monetary]],
                               columns=['Recency', 'Frequency', 'Monetary'])
        st.session_state.rfm_entries = pd.concat([st.session_state.rfm_entries, new_entry], ignore_index=True)
        st.success("Entry added successfully!")

    # Display current entries table
    if not st.session_state.rfm_entries.empty:
        st.markdown("**Current Entries**")
        st.dataframe(st.session_state.rfm_entries.style.format({
            'Monetary': '${:,.2f}'
        }), height=200)

        # Clear all button (outside the form)
        if st.button("❌ Clear All Entries"):
            st.session_state.rfm_entries = pd.DataFrame(columns=['Recency', 'Frequency', 'Monetary'])
            st.success("All entries cleared!")
            st.rerun()

        # Analyze section (with instruction text)
        st.markdown("---")
        st.markdown("**If you have finished entering information, click the button below to analyze**")

        if st.button("📈 Analyze Segments", type="primary"):
            with st.spinner("Analyzing segments..."):
                X = st.session_state.rfm_entries[['Recency', 'Frequency', 'Monetary']]
                X_scaled = st.session_state.scaler.transform(X)
                clusters = st.session_state.model.predict(X_scaled)

                segment_names = {
                    0: "Loyal",
                    1: "Dormant",
                    2: "VIP",
                    3: "At Risk"
                }

                result_df = st.session_state.rfm_entries.copy()
                result_df['Segment'] = [segment_names[c] for c in clusters]

                st.success("Analysis complete!")
                st.dataframe(result_df.style.format({
                    'Monetary': '${:,.2f}'
                }), height=400)

                # Show distribution
                st.markdown("**Segmentation Distribution**")
                seg_counts = result_df['Segment'].value_counts().reset_index()
                seg_counts.columns = ['Segment', 'Count']
                fig = px.pie(seg_counts, values='Count', names='Segment',
                             title="Customer Segments Distribution")
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No entries yet. Please add some RFM data using the form above.")

else: # Upload file
  st.markdown("<h5>📤 Upload file</h5>", unsafe_allow_html=True)
  with st.expander("📝 File Format Requirements", expanded=True):
    st.markdown("""
        **Please ensure your file contains these exact column names:**
        - `CustomerID`: Unique customer identifier (numeric)
        - `Recency`: Days since last purchase (integer)
        - `Frequency`: Total number of transactions (integer)
        - `Monetary`: Total spending amount (numeric)
        
        **Example format:**
        ```csv
        CustomerID,Recency,Frequency,Monetary
        1001,30,5,1250.50
        1002,90,2,800.00
        1003,15,8,3400.75
        ```
        
        **Notes:**
        - File must be CSV or Excel format
        - First row should be column headers
        - Missing values will cause errors
    """)

  uploaded_file = st.file_uploader("Choose a file (csv/excel)", type=["csv", "xlsx", "xls"])

  if uploaded_file:
      # Try only for reading file
      try:
          if uploaded_file.name.endswith('.csv'):
              df = pd.read_csv(uploaded_file)
          elif uploaded_file.name.endswith(('.xlsx', '.xls')):
              df = pd.read_excel(uploaded_file, engine='openpyxl')
      except:
          st.error("Unsupported file format. Please upload a CSV or Excel file.")
          st.stop()

      # Check columns
      required_cols = ["CustomerID", "Recency", "Frequency", "Monetary"]
      if not all(col in df.columns for col in required_cols):
          missing = [col for col in required_cols if col not in df.columns]
          st.error(f"The uploaded file is missing required columns: {', '.join(missing)}.")
          st.stop()

      # Check if model and scaler are loaded
      if 'scaler' not in st.session_state or 'model' not in st.session_state:
          st.error("Scaler or model not loaded. Please train or upload the model first.")
          st.stop()

      with st.spinner("Analyzing..."):
          # Scale
          X = df[['Recency', 'Frequency', 'Monetary']]
          X_scaled = st.session_state.scaler.transform(X)

          # Predict
          df["Cluster"] = st.session_state.model.predict(X_scaled)

          # Segment mapping
          segment_map = {
              0: "Loyal",
              1: "Dormant",
              2: "VIP",
              3: "At Risk"
          }
          df["Segment"] = df["Cluster"].map(segment_map)

          st.session_state['upload_result'] = df

      st.success(f"Complete analysing {len(df)} customers!")

      # Display results
      st.dataframe(
          df.style.format({
              "Recency": "{:.0f}",
              "Frequency": "{:.0f}",
              "Monetary": "${:,.0f}",
          }),
          height=400
      )

      # Export
      st.download_button(
          label="📥 Result's download",
          data=df.to_csv(index=False).encode('utf-8'),
          file_name='RFM_result.csv',
      )
