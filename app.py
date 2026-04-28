import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from st_on_hover_tabs import on_hover_tabs
import re

# ----------------------
# CONFIG & PAGE SETUP
# ----------------------
st.set_page_config(page_title="BILIWAKA NALUMUNYE BUSINESS DIRECTORY", page_icon="🏪", layout="wide")

# ----------------------
# CUSTOM CSS STYLING
# ----------------------
st.markdown("""
<style>
    /* Main Theme */
    .stApp { background-color: #f8f9fa; }
    
    /* Header */
    .main-title { text-align: center; color: #1a365d; font-weight: 800; margin-bottom: -20px; font-size: 2.5rem; }
    .sub-title { text-align: center; color: #4a5568; font-size: 1.1rem; margin-bottom: 30px; }
    
    /* Cards */
    .biz-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 6px solid #d69e2e; margin-bottom: 25px; transition: transform 0.2s; }
    .biz-card:hover { transform: translateY(-3px); box-shadow: 0 10px 15px rgba(0,0,0,0.1); }
    
    /* WhatsApp Button */
    .wa-btn { display: inline-block; padding: 10px 20px; background-color: #25D366; color: white !important; text-decoration: none; border-radius: 8px; font-weight: bold; text-align: center; }
    .wa-btn:hover { background-color: #128C7E; color: white !important; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #1a365d; }
    section[data-testid="stSidebar"] .stMarkdown { color: white; }
</style>
""", unsafe_allow_html=True)

# ----------------------
# GOOGLE SHEETS SETUP (DATABASE)
# ----------------------
# Instructions to set this up are below the code!
@st.cache_resource
def connect_to_gsheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        # Streamlit puts your secrets in st.secrets
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        client = gspread.authorize(creds)
        gsheet = client.open("BiliwakaDirectory") # CHANGE THIS TO YOUR EXACT GOOGLE SHEET NAME
        worksheet = gsheet.sheet1
        return worksheet
    except Exception as e:
        st.error("⚠️ Could not connect to Google Sheets. Check your Setup Instructions.")
        return None

worksheet = connect_to_gsheet()

def load_data():
    if worksheet:
        try:
            data = worksheet.get_all_records()
            return pd.DataFrame(data)
        except:
            pass
    # Fallback empty dataframe if no sheet connection
    return pd.DataFrame(columns=["Business Name", "Category", "Product", "Price (UGX)", "Contact", "Location", "Image URL"])

df = load_data()

# ----------------------
# HELPER FUNCTIONS
# ----------------------
def format_ugx(amount):
    try:
        return f"UGX {int(amount):,}"
    except:
        return amount

# ----------------------
# HEADER
# ----------------------
st.markdown('<div class="main-title">🏪 BILIWAKA NALUMUNYE</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Find trusted businesses, products, and services in Kampala & Nalumunye.</div>', unsafe_allow_html=True)

# ----------------------
# SIDEBAR (FILTERS & ADD FORM)
# ----------------------
st.sidebar.markdown("## 🔍 Find Businesses")
search_query = st.sidebar.text_input("Search by name or product...")
category_filter = st.sidebar.selectbox("Filter by Category", ["All"] + sorted(df["Category"].unique().tolist()) if not df.empty else ["All"])

st.sidebar.markdown("---")
st.sidebar.markdown("## ➕ Add Your Business")

with st.sidebar.form("add_business_form"):
    biz_name = st.text_input("Business Name *")
    category = st.selectbox("Category *", ["Fashion", "Beauty", "Electronics", "Services", "Food & Drinks", "Hardware", "Other"])
    product = st.text_input("Product / Service *")
    price = st.number_input("Price (UGX) *", min_value=0, step=1000)
    contact = st.text_input("WhatsApp Number *", placeholder="0752XXXXXX or 256...")
    location = st.text_input("Location *")
    image_url = st.text_input("Image Link (Optional)", placeholder="Paste a URL to a photo")
    
    submitted = st.form_submit_button("Submit Business", use_container_width=True)

    if submitted:
        if biz_name and product and price and contact and location:
            # Clean phone number (remove spaces, add 256 if missing)
            clean_contact = contact.replace(" ", "")
            if clean_contact.startswith("07"):
                clean_contact = "256" + clean_contact[1:]
            
            new_row = {
                "Business Name": biz_name, 
                "Category": category, 
                "Product": product, 
                "Price (UGX)": price, 
                "Contact": clean_contact, 
                "Location": location,
                "Image URL": image_url
            }
            
            # Save to Google Sheets
            if worksheet:
                worksheet.append_row(list(new_row.values()))
                st.success("✅ Business added successfully!")
                st.rerun() # Refresh to show new business
            else:
                st.error("Database not connected.")
        else:
            st.error("Please fill in all required fields.")

# ----------------------
# FILTER LOGIC
# ----------------------
if not df.empty:
    filtered_df = df.copy()
    if search_query:
        filtered_df = filtered_df[filtered_df.apply(lambda row: search_query.lower() in row["Business Name"].lower() or search_query.lower() in row["Product"].lower(), axis=1)]
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df["Category"] == category_filter]
else:
    filtered_df = df

# ----------------------
# DISPLAY PRODUCTS
# ----------------------
st.markdown(f"**Showing {len(filtered_df)} businesses**")

if filtered_df.empty:
    st.info("No businesses found. Try a different search or be the first to add one!")
else:
    for index, row in filtered_df.iterrows():
        wa_link = f"https://wa.me/{row['Contact']}?text=Hello%20I%20saw%20{row['Product']}%20on%20the%20Biliwaka%20Directory"
        image_html = f'<img src="{row["Image URL"]}" style="width:100%; height:180px; object-fit:cover; border-radius:8px;">' if "Image URL" in df.columns and pd.notna(row.get("Image URL")) and row["Image URL"] else '<div style="width:100%; height:180px; background:#e2e8f0; border-radius:8px; display:flex; align-items:center; justify-content:center; color:#718096; font-size:40px;">🏪</div>'
        
        card_html = f"""
        <div class="biz-card">
            {image_html}
            <h3 style="margin-top:10px; color:#1a202c;">{row['Product']}</h3>
            <p style="color:#4a5568; margin-bottom:10px;">🏢 <b>{row['Business Name']}</b> • 📍 {row['Location']}</p>
            <p style="font-size:1.2rem; color:#2d3748; font-weight:bold;">💰 {format_ugx(row['Price (UGX)'])}</p>
            <div style="text-align: right; margin-top:15px;">
                <a href="{wa_link}" target="_blank" class="wa-btn">💬 Order on WhatsApp</a>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

# ----------------------
# FOOTER
# ----------------------
st.markdown("---")
st.markdown('<div style="text-align: center; color: #718096;">© 2026 Biliwaka Nalumunye Business Directories. All rights reserved.</div>', unsafe_allow_html=True)
