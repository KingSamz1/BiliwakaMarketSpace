# ==============================
# BILIWAKA MARKETSPACE - PRO VERSION (NO ADMIN APPROVAL)
# Firebase + Seller Marketplace + Payments
# ==============================

import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
import requests
import uuid

# ----------------------
# PAGE CONFIG
# ----------------------
st.set_page_config(page_title="Biliwaka MarketSpace", layout="wide")

# ----------------------
# FIREBASE CONFIG
# ----------------------
firebase_config = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "YOUR_PROJECT.firebaseapp.com",
    "projectId": "YOUR_PROJECT_ID",
    "storageBucket": "YOUR_PROJECT.appspot.com",
    "appId": "YOUR_APP_ID"
}

# ----------------------
# INIT FIREBASE
# ----------------------
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
storage = firebase.storage()

# ----------------------
# SESSION STATE
# ----------------------
if "user" not in st.session_state:
    st.session_state.user = None

# ----------------------
# HEADER
# ----------------------
st.title("Biliwaka MarketSpace")
st.markdown("### Discover. Connect. Trade. Uganda’s Digital Marketplace")

# ----------------------
# AUTH
# ----------------------
st.sidebar.title("🔐 Account")
mode = st.sidebar.radio("Access", ["Login", "Register"])

email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

if mode == "Register" and st.sidebar.button("Create Account"):
    try:
        auth.create_user_with_email_and_password(email, password)
        st.sidebar.success("Account created")
    except:
        st.sidebar.error("Failed")

if mode == "Login" and st.sidebar.button("Login"):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        st.session_state.user = user
        st.sidebar.success("Logged in")
    except:
        st.sidebar.error("Login failed")

# ----------------------
# LOAD LISTINGS
# ----------------------
st.subheader("📢 Marketplace Listings")

listings_ref = db.collection("listings")

for doc in listings_ref.stream():
    data = doc.to_dict()

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(f"### {data.get('title')}")
        st.write(data.get("description"))
        st.write(f"📍 {data.get('location')}")

        if data.get("image"):
            st.image(data.get("image"), width=250)

    with col2:
        st.markdown(f"### 💰 UGX {data.get('price'):,}")
        st.markdown(f"📲 [WhatsApp](https://wa.me/{data.get('contact')})")

    st.markdown("---")

# ----------------------
# SELLER DASHBOARD
# ----------------------
if st.session_state.user:

    st.subheader("➕ Sell on MarketSpace")

    with st.form("sell_form"):
        title = st.text_input("Title")
        price = st.number_input("Price", min_value=0)
        location = st.text_input("Location")
        contact = st.text_input("WhatsApp (256xxxx)")
        description = st.text_area("Description")
        image = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

        submit = st.form_submit_button("Publish Listing")

        if submit:
            if not contact.startswith("256"):
                st.error("Phone must start with 256")
            else:
                image_url = ""

                if image:
                    file_id = str(uuid.uuid4())
                    storage.child(f"images/{file_id}.jpg").put(image)
                    image_url = storage.child(f"images/{file_id}.jpg").get_url(None)

                listings_ref.add({
                    "title": title,
                    "price": price,
                    "location": location,
                    "contact": contact,
                    "description": description,
                    "image": image_url,
                    "owner": st.session_state.user["email"]
                })

                st.success("✅ Listing published successfully")

# ----------------------
# PAYMENT SYSTEM
# ----------------------
st.markdown("---")
st.subheader("💳 Mobile Money Payments")

amount = st.number_input("Amount (UGX)", min_value=0)
phone = st.text_input("Phone (256XXXXXXXXX)")

if st.button("Pay with MTN/Airtel MoMo"):

    tx_ref = str(uuid.uuid4())

    url = "https://api.flutterwave.com/v3/payments"

    headers = {
        "Authorization": "Bearer YOUR_FLUTTERWAVE_SECRET_KEY",
        "Content-Type": "application/json"
    }

    payload = {
        "tx_ref": tx_ref,
        "amount": amount,
        "currency": "UGX",
        "payment_options": "mobilemoneyuganda",
        "redirect_url": "https://yourdomain.com",
        "customer": {
            "email": "user@email.com",
            "phonenumber": phone,
            "name": "Biliwaka User"
        }
    }

    res = requests.post(url, json=payload, headers=headers)

    st.json(res.json())

# ----------------------
# FOOTER
# ----------------------
st.markdown("---")
st.write("© 2026 Biliwaka MarketSpace | Uganda Marketplace")
