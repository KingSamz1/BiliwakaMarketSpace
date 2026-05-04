import streamlit as st
import pandas as pd
from database import get_connection, init_db
from utils import apply_theme, init_session_defaults, render_footer, render_topbar, guard_logged_in

st.set_page_config(page_title="My Dashboard - Biliwaka", page_icon="📊", layout="wide")
init_session_defaults()
init_db()
apply_theme()
guard_logged_in()
render_topbar()

user = st.session_state.user

if user['role'] == 'buyer':
    st.title("Welcome to Biliwaka! 👋")
    st.warning("Switch your account role to **Vendor** to create listings.")
    render_footer()
    st.stop()

st.title(f"Welcome back, {user['first_name']} 👋")

# Quick Stats
with get_connection() as conn:
    my_ads = conn.execute("SELECT * FROM ads WHERE user_id = ?", (user['id'],)).fetchall()
    active_ads = [ad for ad in my_ads if ad['is_active'] == 1]
    total_views = sum(ad['clicks'] for ad in my_ads)
    
col1, col2, col3 = st.columns(3)
col1.metric("My Listings", len(my_ads))
col2.metric("Active", len(active_ads))
col3.metric("Total Views", f"{total_views:,}")

st.markdown("---")

# --- EDIT MODAL ---
if "edit_id" not in st.session_state: st.session_state.edit_id = None

if st.session_state.edit_id is not None:
    st.subheader("✏️ Edit Listing")
    with get_connection() as conn: ad = conn.execute("SELECT * FROM ads WHERE id = ?", (st.session_state.edit_id,)).fetchone()
    if ad:
        with st.form("edit_form"):
            c1, c2 = st.columns(2)
            with c1:
                new_title = st.text_input("Title", value=ad['title'])
                new_cat = st.selectbox("Category", ["Fashion", "Beauty", "Electronics", "Services", "Food", "Vehicles", "Property", "Agriculture"], index=["Fashion", "Beauty", "Electronics", "Services", "Food", "Vehicles", "Property", "Agriculture"].index(ad['category']) if ad['category'] in ["Fashion", "Beauty", "Electronics", "Services", "Food", "Vehicles", "Property", "Agriculture"] else 0)
                new_price = st.number_input("Price (UGX)", value=ad['price'])
                new_phone = st.text_input("Listing Phone", value=ad['phone'])
            with c2:
                new_desc = st.text_area("Description", value=ad['description'], height=120)
                new_discount = st.number_input("Discount %", min_value=0.0, max_value=90.0, value=float(ad['discount']), step=5.0)
            st.markdown("**📸 Image URLs (Max 10, one per line)**")
            existing = ad['media'].split(',') if ad['media'] else []
            new_img = st.text_area("URLs", value="\n".join(existing), height=100)
            cs, cc = st.columns(2)
            with cs:
                if st.form_submit_button("💾 Save Changes", use_container_width=True):
                    imgs = [u.strip() for u in new_img.split('\n') if u.strip()][:10]
                    with get_connection() as conn:
                        conn.execute("UPDATE ads SET title=?, category=?, price=?, description=?, media=?, discount=?, phone=? WHERE id=?", (new_title, new_cat, new_price, new_desc, ",".join(imgs), new_discount, new_phone, st.session_state.edit_id))
                    st.session_state.edit_id = None; st.success("Listing updated!"); st.rerun()
            with cc:
                if st.form_submit_button("❌ Cancel", use_container_width=True): st.session_state.edit_id = None; st.rerun()

# --- CREATE SECTION ---
st.subheader("➕ Create New Listing")
with st.form("create_form"):
    c1, c2 = st.columns(2)
    with c1:
        new_title = st.text_input("Title *")
        new_cat = st.selectbox("Category *", ["Fashion", "Beauty", "Electronics", "Services", "Food", "Vehicles", "Property", "Agriculture"])
        new_price = st.number_input("Price (UGX) *", min_value=0)
        new_phone = st.text_input("Contact Phone *")
    with c2:
        new_desc = st.text_area("Description *", height=120)
        st.file_uploader("📸 Upload Images", type=['jpg', 'png', 'jpeg', 'webp'], accept_multiple_files=True, key="dash_upload")
        st.text_area("Image URLs", height=70, key="dash_urls")
    if st.form_submit_button("🚀 Publish Listing", type="primary", use_container_width=True):
        if not new_title or not new_price or not new_phone or not new_desc: st.error("Fill in all required fields.")
        else:
            import base64
            imgs = []
            uploaded = st.session_state.get("dash_upload")
            if uploaded:
                for f in uploaded:
                    bytes_data = f.read()
                    b64 = base64.b64encode(bytes_data).decode()
                    imgs.append(f"data:image/png;base64,{b64}")
            urls = st.session_state.get("dash_urls", "")
            if urls: imgs.extend([u.strip() for u in urls.split('\n') if u.strip()])
            with get_connection() as conn:
                conn.execute("""INSERT INTO ads(user_id, phone, title, description, media, is_featured, clicks, whatsapp_clicks, calls, is_active, created_at, expires_at, category, price) VALUES (?, ?, ?, ?, ?, 0, 0, 0, 0, 1, date('now'), date('now', '+45 days'), ?, ?)""", (user['id'], new_phone, new_title, new_desc, ",".join(imgs[:10]), new_cat, new_price))
            st.success("Listing published!"); st.rerun()

st.markdown("---")
st.subheader("📋 My Listings")
if my_ads:
    st.dataframe(pd.DataFrame([dict(ad) for ad in my_ads])[["id", "title", "category", "price", "clicks", "is_active"]], use_container_width=True, hide_index=True)
else:
    st.info("No listings yet. Create one above!")

render_footer()
