import streamlit as st
import pandas as pd

# ----------------------
# CONFIG
# ----------------------
st.set_page_config(page_title="BILIWAKA NALUMUNYE BUSINESS DIRECTORY", layout="wide")

# ----------------------
# SAMPLE DATA
# ----------------------
data = {
    "Business Name": ["Elijah Shoe World", "Sarahs Touch Salon"],
    "Category": ["Fashion", "Beauty"],
    "Product": ["Men Leather Shoes", "Wigs & Braids"],
    "Price (UGX)": [120000, 80000],
    "Contact": ["0752694452", "0780000000"],
    "Location": ["Kampala", "Nalumunye"]
}

df = pd.DataFrame(data)

# ----------------------
# SIDEBAR (FILTERS)
# ----------------------
st.sidebar.title("Filter Listings")
category_filter = st.sidebar.selectbox("Select Category", ["All"] + list(df["Category"].unique()))

# ----------------------
# HEADER
# ----------------------
st.title("BILIWAKA NALUMUNYE BUSINESS DIRECTORY")
st.write("Find trusted businesses, products, and services in Kampala & Nalumunye.")

# ----------------------
# FILTER LOGIC
# ----------------------
if category_filter != "All":
    filtered_df = df[df["Category"] == category_filter]
else:
    filtered_df = df

# ----------------------
# DISPLAY PRODUCTS
# ----------------------
st.subheader("Marketplace Listings")

for index, row in filtered_df.iterrows():
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### {row['Product']}")
            st.write(f"**Business:** {row['Business Name']}")
            st.write(f"**Category:** {row['Category']}")
            st.write(f"**Location:** {row['Location']}")
        
        with col2:
            st.write(f"💰 UGX {row['Price (UGX)']}")
            whatsapp_link = f"https://wa.me/{row['Contact']}"
            st.markdown(f"[Order on WhatsApp]({whatsapp_link})")
        
        st.markdown("---")

# ----------------------
# ADD BUSINESS FORM
# ----------------------
st.subheader("Add Your Business")

with st.form("add_business_form"):
    business_name = st.text_input("Business Name")
    category = st.selectbox("Category", ["Fashion", "Beauty", "Electronics", "Services"])
    product = st.text_input("Product/Service")
    price = st.number_input("Price (UGX)", min_value=0)
    contact = st.text_input("WhatsApp Number (e.g. 2567XXXXXXX)")
    location = st.text_input("Location")

    submitted = st.form_submit_button("Submit")

    if submitted:
        new_data = pd.DataFrame({
            "Business Name": [business_name],
            "Category": [category],
            "Product": [product],
            "Price (UGX)": [price],
            "Contact": [contact],
            "Location": [location]
        })

        df = pd.concat([df, new_data], ignore_index=True)
        st.success("Business added successfully!")

# ----------------------
# FOOTER
# ----------------------
st.markdown("---")
st.write("© 2026 Biliwaka Nalumunye Business Directories")
