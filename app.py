import streamlit as st
import pandas as pd
import requests

# ----------------------
# CONFIG & PAGE SETUP
# ----------------------
st.set_page_config(page_title="Biliwaka MarketHub", page_icon="🏪", layout="wide")

# ----------------------
# STYLING (Dark Mode Ready!)
# ----------------------
st.markdown("""
<style>
[data-testid="stApp"] {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    color: #f4f4f4;
}
h1, h2, h3, h4, h5, h6, p, span, li, label {
    color: #f4f4f4 !important;
}
input, select, textarea {
    color: #f4f4f4 !important;
}
.stTextInput > div > div {
    background-color: rgba(42, 42, 42, 0.8) !important;
    border: 1px solid #444 !important;
}
.stSelectbox > div {
    background-color: rgba(42, 42, 42, 0.8) !important;
    color: #f4f4f4 !important;
}
.main-title { text-align: center; color: #ffd700 !important; font-weight: 800; margin-bottom: -20px; font-size: 2.5rem; text-transform: uppercase; letter-spacing: 2px; }
.sub-title { text-align: center; color: #a0aec0 !important; font-size: 1.1rem; margin-bottom: 30px; }
.biz-card { background: #262626; padding: 25px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); border-left: 6px solid #d4af37; margin-bottom: 25px; transition: transform 0.2s; }
.biz-card:hover { transform: translateY(-3px); box-shadow: 0 10px 15px rgba(212, 175, 55, 0.15); }
.wa-btn { display: inline-block; padding: 10px 20px; background-color: #25D366; color: white !important; text-decoration: none; border-radius: 8px; font-weight: bold; text-align: center; }
.wa-btn:hover { background-color: #128C7E; color: white !important; }
.price-tag { font-size: 1.3rem; color: #ffd700 !important; font-weight: bold; }
.meta-text { color: #a0aec0 !important; font-size: 0.9rem; }
.section-header { color: #ffd700 !important; font-size: 1.5rem; margin-top: 20px; border-bottom: 2px solid #444; padding-bottom: 5px; display: inline-block; }
section[data-testid="stSidebar"] { background-color: #111111 !important; }
section[data-testid="stSidebar"] .stMarkdown { color: #f4f4f4 !important; }
</style>
""", unsafe_allow_html=True)

# ----------------------
# HELPER FUNCTIONS
# ----------------------
FORM_URL = st.secrets.get("FORM_URL", "")

def format_ugx(amount):
    try:
        return f"UGX {int(amount):,}"
    except:
        return amount

def get_sheet_id():
    try:
        start = FORM_URL.find("/d/") + 3
        end = FORM_URL.find("/", start)
        return FORM_URL[start:end]
    except:
        return ""

def fetch_data():
    try:
        sheet_id = get_sheet_id()
        sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        return pd.read_csv(sheet_url)
    except:
        return pd.DataFrame(columns=["Business Name", "Category", "Product", "Price (UGX)", "Contact", "Location", "Image URL"])

def submit_to_sheet(data_dict):
    try:
        fake_form_id = "e/1FAIpQLSddeF5o3DFr4a0AmlbdIrzwBP-YZnzyN_iJjb6QCbIfkgmjrw"
        payload = {f"{fake_form_id}.response": "", "fbzx": ""}
        for key, value in data_dict.items():
            payload[f"{fake_form_id}.entry.{key}"] = str(value)
        requests.post(f"https://docs.google.com/forms/d/{get_sheet_id()}/formResponse", data=payload)
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

# ----------------------
# LOAD DATA
# ----------------------
df = fetch_data()

# ----------------------
# HEADER
# ----------------------
st.markdown('<div class="main-title">🏪 Biliwaka MarketHub</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Discover. Connect. Trade. Uganda’s Digital Marketplace.</div>', unsafe_allow_html=True)

# ----------------------
# SIDEBAR
# ----------------------
st.sidebar.markdown("## 🔍 Find Businesses")
search_query = st.sidebar.text_input("Search by name or product...")

if not df.empty:
    category_filter = st.sidebar.selectbox("Filter by Category", ["All"] + sorted(df["Category"].unique().tolist()))
else:
    category_filter = "All"

st.sidebar.markdown("---")
st.sidebar.markdown("## ➕ Add Your Business")

with st.sidebar.form("add_business_form"):
    biz_name = st.text_input("Business Name *")
    category = st.selectbox("Category *", ["Fashion", "Beauty", "Electronics", "Services", "Food & Drinks", "Hardware", "Other"])
    product = str(st.text_input("Product / Service *"))
    price = st.number_input("Price (UGX) *", min_value=0, step=1000)
    contact = st.text_input("WhatsApp Number *", placeholder="0752XXXXXX")
    location = st.text_input("Location *")
    image_url = st.text_input("Image Link (Optional)")
    
    submitted = st.form_submit_button("Submit Business", use_container_width=True)

    if submitted:
        if biz_name and product and price and contact and location:
            clean_contact = contact.replace(" ", "")
            if clean_contact.startswith("07"):
                clean_contact = "256" + clean_contact[1:]
            
            form_data = {
                "Business Name": biz_name, 
                "Category": category, 
                "Product": product, 
                "Price (UGX)": str(price), 
                "Contact": clean_contact, 
                "Location": location, 
                "Image URL": image_url
            }
            
            if submit_to_sheet(form_data):
                st.success("✅ Business added successfully!")
                st.rerun()
            else:
                st.error("Failed to connect to Google Form.")
        else:
            st.error("Please fill in all required fields.")

# ----------------------
# DISPLAY PRODUCTS
# ----------------------
st.markdown(f"**Showing {len(filtered_df)} businesses**")

if filtered_df.empty:
    st.info("No businesses found. Be the first to add one using the menu on the left!")
else:
    for index, row in filtered_df.iterrows():
        wa_link = f"https://wa.me/{row['Contact']}?text=Hello%20I%20saw%20{row['Product']}%20on%20the%20Biliwaka%20MarketHub"
        
        img = row.get("Image URL", "")
        image_html = f'<img src="{img}" style="width:100%; height:180px; object-fit:cover; border-radius:12px; border: 2px solid #444;">' if pd.notna(img) and img != "" else '<div style="width:100%; height:180px; background: linear-gradient(135deg, #333 0%, #444 100%); border-radius:12px; border: 2px solid #444; display:flex; align-items:center; justify-content:center; color:#888;"><div style="text-align:center"><span style="📸</span><br><span style="font-size:12px; color:#888;">No Image</span></div></div>'
        
        card_html = f"""
        <div class="biz-card">
            {image_html}
            <h3 style="margin-top:10px; color:#f4f4f4;">{row['Product']}</h3>
            <p class="meta-text">🏢 <b>{row['Business Name']}</b> • 📍 {row['Location']}</p>
            <p class="price-tag">💰 {format_ugx(row['Price (UGX)'])}</p>
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
st.markdown('<div style="text-align: center; color: #888; font-size: 13px;">© 2026 Biliwaka MarketHub. All rights reserved.</div>', unsafe_allow_html=True)
