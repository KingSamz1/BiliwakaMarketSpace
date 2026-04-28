import streamlit as st
import pandas as pd

# ----------------------
# CONFIG
# ----------------------
st.set_page_config(page_title="Biliwaka MarketSpace", page_icon="🏪", layout="wide")

# ----------------------
# STYLING
# ----------------------
st.markdown("""
<style>
[data-testid="stApp"] {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    color: #f4f4f4;
}
h1, h2, h3, h4, h5, h6, p, span {
    color: #f4f4f4 !important;
}
.main-title {
    text-align: center;
    color: #ffd700 !important;
    font-size: 2.5rem;
    font-weight: 800;
}
.sub-title {
    text-align: center;
    color: #a0aec0 !important;
    margin-bottom: 25px;
}
.card {
    background: #262626;
    padding: 18px;
    border-radius: 15px;
    margin-bottom: 15px;
    border-left: 5px solid #d4af37;
}
.tag {
    color: #ffd700 !important;
    font-weight: bold;
}
.btn {
    background: #25D366;
    padding: 8px 12px;
    border-radius: 8px;
    color: white !important;
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)

# ----------------------
# INITIAL DATA
# ----------------------
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame([
        {
            "Type": "Product",
            "Title": "Elijah Leather Shoes",
            "Category": "Fashion",
            "Details": "Premium leather men shoes",
            "Price": "120,000 UGX",
            "Location": "Kampala",
            "Contact": "0752694452"
        },
        {
            "Type": "Service",
            "Title": "Sarahs Touch Salon",
            "Category": "Beauty",
            "Details": "Wigs, braids, makeup services",
            "Price": "300,000 - 1,500,000 UGX",
            "Location": "Nalumunye",
            "Contact": "0775998783"
        },
        {
            "Type": "Car",
            "Title": "Toyota Premio 2015",
            "Category": "Cars",
            "Details": "Clean, fuel efficient, automatic",
            "Price": "25,000,000 UGX",
            "Location": "Kampala",
            "Contact": "0701112233"
        },
        {
            "Type": "Property",
            "Title": "2 Bedroom House for Rent",
            "Category": "Real Estate",
            "Details": "Self-contained house in good area",
            "Price": "800,000 UGX / month",
            "Location": "Kampala - Kira",
            "Contact": "0788889990"
        }
    ])

df = st.session_state.df

# ----------------------
# HEADER
# ----------------------
st.markdown('<div class="main-title">🏪 Biliwaka MarketSpace</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Multi-Category Marketplace • Cars • Property • Services • Products</div>', unsafe_allow_html=True)

# ----------------------
# FILTERS
# ----------------------
col1, col2 = st.columns(2)

with col1:
    type_filter = st.selectbox("Filter Type", ["All", "Product", "Service", "Car", "Property"])

with col2:
    search = st.text_input("Search marketplace")

filtered_df = df.copy()

if type_filter != "All":
    filtered_df = filtered_df[filtered_df["Type"] == type_filter]

if search:
    filtered_df = filtered_df[
        filtered_df["Title"].str.contains(search, case=False, na=False) |
        filtered_df["Details"].str.contains(search, case=False, na=False)
    ]

# ----------------------
# LISTINGS
# ----------------------
st.markdown("### 📢 Marketplace Listings")

if filtered_df.empty:
    st.warning("No listings found.")
else:
    for _, row in filtered_df.iterrows():

        wa = f"https://wa.me/{row['Contact']}?text=Hello%20I%20am%20interested%20in%20{row['Title']}"

        st.markdown(f"""
        <div class="card">
            <h3>{row['Title']}</h3>
            <p class="tag">[{row['Type']}] • {row['Category']}</p>
            <p>{row['Details']}</p>
            <p><b>💰 {row['Price']}</b></p>
            <p>📍 {row['Location']}</p>
            <a class="btn" href="{wa}" target="_blank">💬 Contact Seller</a>
        </div>
        """, unsafe_allow_html=True)

# ----------------------
# CREATE LISTING
# ----------------------
st.markdown("---")
st.markdown("## ➕ Create Listing")

with st.form("create_listing"):

    listing_type = st.selectbox("Listing Type", ["Product", "Service", "Car", "Property"])
    title = st.text_input("Title")
    category = st.text_input("Category")
    details = st.text_area("Details / Description")
    price = st.text_input("Price")
    location = st.text_input("Location")
    contact = st.text_input("WhatsApp Number")

    submit = st.form_submit_button("Publish Listing")

    if submit:
        new_row = pd.DataFrame([{
            "Type": listing_type,
            "Title": title,
            "Category": category,
            "Details": details,
            "Price": price,
            "Location": location,
            "Contact": contact
        }])

        st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)

        st.success("✅ Listing published successfully!")
        st.rerun()

# ----------------------
# FOOTER
# ----------------------
st.markdown("---")
st.markdown("<center style='color:gray'>© 2026 Biliwaka MarketSpace • Uganda Multi-Category Marketplace</center>", unsafe_allow_html=True)
