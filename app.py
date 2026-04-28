import streamlit as st
import pandas as pd
import datetime
import uuid

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Biliwaka MarketSpace", layout="wide")

# =========================
# STYLING
# =========================
st.markdown("""
<style>
[data-testid="stApp"] {
    background: linear-gradient(135deg,#1a1a1a,#2d2d2d);
    color:white;
}
.card {
    background:#262626;
    padding:15px;
    border-radius:15px;
    margin-bottom:15px;
    border-left:5px solid gold;
}
.title {
    text-align:center;
    font-size:2.5rem;
    color:#ffd700;
    font-weight:900;
}
.btn {
    background:#25D366;
    padding:8px 10px;
    border-radius:8px;
    color:white !important;
    text-decoration:none;
    margin-right:5px;
}
.badge {
    color:#ffd700;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DATABASE (SESSION MOCK)
# =========================
if "listings" not in st.session_state:
    st.session_state.listings = pd.DataFrame(columns=[
        "id","vendor","title","price","location",
        "featured","created_at","expires_at",
        "views","whatsapp_clicks","calls"
    ])

if "banners" not in st.session_state:
    st.session_state.banners = []

if "ratings" not in st.session_state:
    st.session_state.ratings = []

if "users" not in st.session_state:
    st.session_state.users = {}

FREE_LIMIT = 4
EXPIRY_DAYS = 45

# =========================
# HELPERS
# =========================
def now():
    return datetime.datetime.now()

def last_7_days(vendor):
    cutoff = now() - datetime.timedelta(days=7)
    return st.session_state.listings[
        (st.session_state.listings["vendor"] == vendor) &
        (st.session_state.listings["created_at"] > cutoff)
    ]

def expired_cleanup():
    df = st.session_state.listings
    if len(df) > 0:
        st.session_state.listings = df[df["expires_at"] > now()]

def share_link(title, type_):
    msg = f"Check this {type_}: {title} on Biliwaka MarketHub"
    return "https://wa.me/?text=" + msg.replace(" ", "%20")

# =========================
# HEADER
# =========================
st.markdown('<div class="title">🏪 Biliwaka MarketSpace</div>', unsafe_allow_html=True)

# =========================
# LOGIN SYSTEM
# =========================
st.sidebar.title("Vendor Login")

user = st.sidebar.text_input("Phone / Email")

if st.sidebar.button("Login"):
    st.session_state.active_user = user
    st.success("Logged in")

vendor = st.session_state.get("active_user", None)

# =========================
# BANNER ADS (10 SLOT CAROUSEL)
# =========================
st.markdown("## 📢 Banner Ads (UGX 20,000 / week)")

for ad in st.session_state.banners[:10]:
    if ad["type"] == "image":
        st.image(ad["file"], use_container_width=True)
    else:
        st.video(ad["file"])

st.markdown("---")

# =========================
# LISTINGS DISPLAY
# =========================
st.markdown("## 📢 Marketplace Listings")

expired_cleanup()

df = st.session_state.listings.sort_values(by="featured", ascending=False)

for _, row in df.iterrows():

    wa = f"https://wa.me/{row['vendor']}?text=Interested%20in%20{row['title']}"
    call = f"tel:{row['vendor']}"
    share = share_link(row["title"], "listing")

    st.markdown(f"""
    <div class="card">
        <h3>{row['title']}</h3>
        <p>📍 {row['location']}</p>
        <p class="badge">💰 {row['price']}</p>

        <a class="btn" href="{wa}" target="_blank">WhatsApp</a>
        <a class="btn" href="{call}">Call</a>
        <a class="btn" href="{share}" target="_blank">Share</a>
    </div>
    """, unsafe_allow_html=True)

# =========================
# CREATE LISTING (RULE ENGINE)
# =========================
st.markdown("---")
st.markdown("## ➕ Create Listing")

with st.form("listing"):

    title = st.text_input("Title")
    price = st.text_input("Price")
    location = st.text_input("Location")
    featured = st.checkbox("⭐ Featured Ad (40K / 7 days)")

    submit = st.form_submit_button("Publish")

    if submit:

        if not vendor:
            st.error("Login required")
            st.stop()

        recent = last_7_days(vendor)

        # FREE RULE
        if len(recent) >= FREE_LIMIT and not featured:
            st.error("Limit reached (4 per 7 days)")
            st.stop()

        listing = {
            "id": str(uuid.uuid4()),
            "vendor": vendor,
            "title": title,
            "price": price,
            "location": location,
            "featured": featured,
            "created_at": now(),
            "expires_at": now() + datetime.timedelta(days=EXPIRY_DAYS),
            "views": 0,
            "whatsapp_clicks": 0,
            "calls": 0
        }

        st.session_state.listings = pd.concat(
            [st.session_state.listings, pd.DataFrame([listing])],
            ignore_index=True
        )

        if featured:
            st.markdown("""
            💰 Pay Featured Ad:
            https://wa.me/256775998783?text=FEATURED%2040000%20UGX%207%20DAYS
            """)

        st.success("Published")
        st.rerun()

# =========================
# BANNER ADS CREATOR
# =========================
st.markdown("---")
st.markdown("## 📢 Create Banner Ad (UGX 20,000)")

with st.form("banner"):

    file = st.file_uploader("Upload Image / Video")
    type_ = st.selectbox("Type", ["image","video"])

    submit = st.form_submit_button("Create Banner")

    if submit and file:

        st.session_state.banners.append({
            "file": file,
            "type": type_,
            "created_at": now(),
            "expires_at": now() + datetime.timedelta(days=7)
        })

        st.markdown("""
        💰 Pay Banner:
        https://wa.me/256775998783?text=BANNER%2020000%20UGX%207%20DAYS
        """)

        st.success("Banner added")

# =========================
# RATINGS SYSTEM
# =========================
st.markdown("---")
st.markdown("## ⭐ Rate Vendors")

vendor_id = st.text_input("Vendor Phone")
rating = st.slider("Rating", 1, 5)
review = st.text_area("Review")

if st.button("Submit Rating"):
    st.session_state.ratings.append({
        "vendor": vendor_id,
        "rating": rating,
        "review": review
    })
    st.success("Submitted")

# =========================
# SHOW RATINGS
# =========================
if st.session_state.ratings:
    st.markdown("## ⭐ Vendor Ratings")

    rdf = pd.DataFrame(st.session_state.ratings)

    for v in rdf["vendor"].unique():
        avg = rdf[rdf["vendor"] == v]["rating"].mean()
        st.write(f"{v} → ⭐ {round(avg,1)}")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("<center style='color:gray'>© 2026 Biliwaka MarketSpace </center>", unsafe_allow_html=True)
