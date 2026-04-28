import streamlit as st
import pandas as pd

# ----------------------
# CONFIG
# ----------------------
st.set_page_config(page_title="BILIWAKA NALUMUNYE BUSINESS DIRECTORY", layout="wide")

# ----------------------
# SESSION STORAGE (IMPORTANT FIX)
# ----------------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "Business Name": ["Elijah Shoe World", "Sarahs Touch Salon"],
        "Category": ["Fashion", "Beauty"],
        "Product": ["Men Leather Shoes", "Wigs & Braids"],
        "Price (UGX)": [120000, 80000],
        "Contact": ["0752694452", "0780000000"],
        "Location": ["Kampala", "Nalumunye"]
    })

df = st.session_state.data

# ----------------------
# SIDEBAR FILTER
# ----------------------
st.sidebar.title("Filter Listings")

category_filter = st.sidebar.selectbox(
    "Select Category",
    ["All"] + list(df["Category"].unique())
)

search = st.sidebar.text_input("Search business or product")

# ----------------------
# HEADER
# ----------------------
st.title("🏪 BILIWAKA NALUMUNYE BUSINESS DIRECTORY")
st.write("Find trusted businesses, products, and services in Kampala & Nalumunye.")

# ----------------------
# FILTER LOGIC
# ----------------------
filtered_df = df.copy()

if category_filter != "All":
    filtered_df = filtered_df[filtered_df["Category"] == category_filter]

if search:
    filtered_df = filtered_df[
        filtered_df["Business Name"].str.contains(search, case=False, na=False) |
        filtered_df["Product"].str.contains(search, case=False, na=False)
    ]

# ----------------------
# DISPLAY LISTINGS
# ----------------------
st.subheader("📢 Marketplace Listings")

if filtered_df.empty:
    st.warning("No businesses found.")
else:
    for _, row in filtered_df.iterrows():

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"### {row['Product']}")
            st.write(f"**Business:** {row['Business Name']}")
            st.write(f"**Category:** {row['Category']}")
            st.write(f"**Location:** {row['Location']}")

        with col2:
            st.write(f"💰 UGX {row['Price (UGX)']:,}")
            wa = f"https://wa.me/{row['Contact']}"
            st.markdown(f"[💬 Order on WhatsApp]({wa})")

        st.markdown("---")

# ----------------------
# ADD BUSINESS FORM
# ----------------------
st.subheader("➕ Add Your Business")

with st.form("add_business_form"):

    business_name = st.text_input("Business Name")
    category = st.selectbox("Category", ["Fashion", "Beauty", "Electronics", "Services", "Food", "Other"])
    product = st.text_input("Product/Service")
    price = st.number_input("Price (UGX)", min_value=0)
    contact = st.text_input("WhatsApp Number (e.g. 2567XXXXXXX or 075XXXXXXX)")
    location = st.text_input("Location")

    submitted = st.form_submit_button("Submit")

    if submitted:

        if business_name and product and contact:

            # normalize phone
            if contact.startswith("07"):
                contact = "256" + contact[1:]

            new_row = pd.DataFrame([{
                "Business Name": business_name,
                "Category": category,
                "Product": product,
                "Price (UGX)": price,
                "Contact": contact,
                "Location": location
            }])

            st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)

            st.success("✅ Business added successfully!")
            st.rerun()

        else:
            st.error("Please fill in all required fields")

# ----------------------
# FOOTER
# ----------------------
st.markdown("---")
st.write("© 2026 Biliwaka Nalumunye Business Directory")
