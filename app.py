import streamlit as st
import pandas as pd
import requests

# ----------------------
# CONFIG & PAGE SETUP
# ----------------------
st.set_page_config(page_title="Biliwaka MarketHub", page_icon="🏪", layout="wide")

# ----------------------
# STYLING
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
.main-title { text-align: center; color: #ffd700 !important; font-weight: 800; font-size: 2.5rem; }
.sub-title { text-align: center; color: #a0aec0 !important; font-size: 1.1rem; margin-bottom: 30px; }
.biz-card { background: #262626; padding: 20px; border-radius: 15px; margin-bottom: 20px; border-left: 5px solid #d4af37; }
.wa-btn { padding: 10px 15px; background:#25D366; color:white !important; border-radius:8px; text-decoration:none; }
.price-tag { color:#ffd700 !important; font-weight:bold; }
.meta-text { color:#a0aec0 !important; font-size:0.9rem; }
</style>
""", unsafe_allow_html=True)

# ----------------------
# HELPER FUNCTIONS
# ----------------------
def format_ugx(amount):
    try:
        return f"UGX {int(amount):,}"
    except:
        return amount

# ----------------------
# DATA (DEMO / REPLACE WITH GOOGLE SHEETS OR FIREBASE)
# ----------------------
data = {
    "Business Name": ["Biliwaka Shoes", "Kampala Phones", "Fresh Foods UG"],
    "Category": ["Fashion", "Electronics", "Food & Drinks"],
    "Product": ["Shoes", "iPhones", "Groceries"],
    "Price (UGX)": [50000, 800000, 20000],
    "Contact": ["256712345678", "256701112233", "256778889900"],
    "Location": ["Kampala", "Kikuubo", "Nakasero"],
    "Image URL": ["", "", ""]
}

df = pd.DataFrame(data)

# ----------------------
# FILTERS (FIXED PART)
# ----------------------
search_query = ""
category_filter = "All"

# Sidebar
st.sidebar.markdown("## 🔍 Search")

search_query = st.sidebar.text_input("Search businesses")

category_filter = st.sidebar.selectbox(
    "Filter Category",
    ["All"] + list(df["Category"].unique())
)

# ----------------------
# DEFINE FILTERED DATAFRAME (FIXED ERROR)
# ----------------------
filtered_df = df.copy()

# Search filter
if search_query:
    filtered_df = filtered_df[
        filtered_df["Product"].str.contains(search_query, case=False, na=False) |
        filtered_df["Business Name"].str.contains(search_query, case=False, na=False)
    ]

# Category filter
if category_filter != "All":
    filtered_df = filtered_df[filtered_df["Category"] == category_filter]

# ----------------------
# HEADER
# ----------------------
st.markdown('<div class="main-title">🏪 Biliwaka MarketHub</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Discover. Connect. Trade. Uganda’s Marketplace</div>', unsafe_allow_html=True)

# ----------------------
# COUNT DISPLAY (NOW SAFE)
# ----------------------
st.markdown(f"### Showing {len(filtered_df)} businesses")

# ----------------------
# DISPLAY LISTINGS
# ----------------------
if filtered_df.empty:
    st.warning("No businesses found.")
else:
    for _, row in filtered_df.iterrows():

        wa_link = f"https://wa.me/{row['Contact']}?text=Hello%20I%20saw%20your%20{row['Product']}%20on%20Biliwaka%20MarketHub"

        card = f"""
        <div class="biz-card">
            <h3>{row['Product']}</h3>
            <p class="meta-text">🏢 {row['Business Name']} | 📍 {row['Location']}</p>
            <p class="price-tag">{format_ugx(row['Price (UGX)'])}</p>
            <a href="{wa_link}" target="_blank" class="wa-btn">💬 Contact on WhatsApp</a>
        </div>
        """

        st.markdown(card, unsafe_allow_html=True)

# ----------------------
# FOOTER
# ----------------------
st.markdown("---")
st.markdown("<center style='color:gray'>© 2026 Biliwaka MarketHub</center>", unsafe_allow_html=True)
