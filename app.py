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
h1, h2, h3, h4, h5, h6, p {
    color: #f4f4f4 !important;
}
.main-title {
    text-align: center;
    color: #ffd700 !important;
    font-size: 2.6rem;
    font-weight: 900;
}
.sub-title {
    text-align: center;
    color: #a0aec0 !important;
    margin-bottom: 20px;
}
.biz-card {
    background: #262626;
    padding: 18px;
    border-radius: 15px;
    margin-bottom: 15px;
    border-left: 5px solid #d4af37;
}
.price-tag {
    color:#ffd700 !important;
    font-weight:bold;
}
.meta-text {
    color:#a0aec0 !important;
    font-size:0.9rem;
}
.wa-btn {
    padding: 10px 15px;
    background:#25D366;
    color:white !important;
    border-radius:8px;
    text-decoration:none;
    display:inline-block;
}
</style>
""", unsafe_allow_html=True)

# ----------------------
# DATA
# ----------------------
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Business Name": [
            "Elijah Shoe World",
            "Sarahs Touch Salon"
        ],
        "Category": [
            "Fashion",
            "Beauty"
        ],
        "Product": [
            "Men Leather Shoes",
            "Wigs & Braids"
        ],
        "Price (UGX)": [
            120000,
            "300,000 - 1,500,000"
        ],
        "Contact": [
            "0752694452",
            "0775998783"
        ],
        "Location": [
            "Kampala",
            "Nalumunye"
        ]
    })

df = st.session_state.df

# ----------------------
# HEADER
# ----------------------
st.markdown('<div class="main-title">🏪 Biliwaka MarketSpace</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Discover. Connect. Trade. Uganda’s Marketplace</div>', unsafe_allow_html=True)

# ----------------------
# SEARCH
# ----------------------
search = st.text_input("🔍 Search marketplace")

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["Business Name"].str.contains(search, case=False, na=False) |
        filtered_df["Product"].str.contains(search, case=False, na=False)
    ]

# ----------------------
# DISPLAY LISTINGS
# ----------------------
st.markdown("### 📢 Marketplace Listings")

for _, row in filtered_df.iterrows():

    # ensure proper WhatsApp format
    phone = str(row["Contact"]).strip()

    if phone.startswith("0"):
        phone = "256" + phone[1:]
    elif not phone.startswith("256"):
        phone = "256" + phone

    wa_link = f"https://wa.me/{phone}?text=Hello%20I%20am%20interested%20in%20{row['Product']}"

    st.markdown(f"""
    <div class="biz-card">
        <h3>{row['Product']}</h3>
        <p class="meta-text">🏢 {row['Business Name']} | 📍 {row['Location']}</p>
        <p class="price-tag">💰 {row['Price (UGX)']}</p>
        <a class="wa-btn" href="{wa_link}" target="_blank">💬 WhatsApp</a>
    </div>
    """, unsafe_allow_html=True)

# ----------------------
# CREATE LISTING
# ----------------------
st.markdown("---")
st.markdown("## ➕ Create Listing")

with st.form("create_listing"):

    name = st.text_input("Business Name")

    category = st.selectbox("Category", [
        "Fashion",
        "Beauty",
        "Electronics",
        "Services",
        "Food",
        "Car Dealership 🚗",
        "Real Estate 🏠"
    ])

    product = st.text_input("Product / Service")
    price = st.text_input("Price (UGX)")
    contact = st.text_input("WhatsApp Number (e.g. 077xxxxxxx)")
    location = st.text_input("Location")

    submit = st.form_submit_button("Publish Listing")

    if submit:

        # AUTO FORMAT PHONE
        phone = contact.strip()

        if phone.startswith("0"):
            phone = "256" + phone[1:]
        elif not phone.startswith("256"):
            phone = "256" + phone

        new_row = pd.DataFrame([{
            "Business Name": name,
            "Category": category,
            "Product": product,
            "Price (UGX)": price,
            "Contact": phone,
            "Location": location
        }])

        st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)

        st.success("✅ Listing published successfully!")
        st.rerun()

# ----------------------
# FOOTER
# ----------------------
st.markdown("---")
st.markdown("<center style='color:gray'>© 2026 Biliwaka MarketSpace</center>", unsafe_allow_html=True)
