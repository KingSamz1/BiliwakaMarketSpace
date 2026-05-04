import streamlit as st
import base64
from datetime import datetime
from database import get_connection, init_db
from utils import apply_theme, guard_logged_in, render_footer, render_topbar

st.set_page_config(page_title="Buy Banner - Biliwaka", page_icon="🛒", layout="wide")
init_db()
apply_theme()
guard_logged_in()
render_topbar()

st.title("🛒 Buy / Submit Vendor Banner")
st.markdown("Get your banner displayed on the MarketSpace page to gain maximum visibility!")
st.caption("Once submitted, our admin team will review and approve your banner.")

# Ensure the vendor_banners table exists safely
with get_connection() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS vendor_banners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            media TEXT NOT NULL,
            is_active INTEGER DEFAULT 0,
            expires_at TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

with st.form("submit_banner_form"):
    st.subheader("📤 Submit Your Banner Image")
    
    upload_method = st.radio("How would you like to add your banner?", ["Upload from Device", "Paste Image URL"], horizontal=True)
    
    banner_url = ""
    
    if upload_method == "Upload from Device":
        uploaded_file = st.file_uploader(
            "Choose an image file", 
            type=['jpg', 'jpeg', 'png', 'webp'],
            help="Recommended: 1200x400px, max 5MB"
        )
        if uploaded_file is not None:
            if uploaded_file.size > 5 * 1024 * 1024:
                st.warning("⚠️ File is too large. Please use an image under 5MB.")
            else:
                bytes_data = uploaded_file.read()
                b64_string = base64.b64encode(bytes_data).decode("utf-8")
                if uploaded_file.type:
                    mime = uploaded_file.type
                else:
                    ext = uploaded_file.name.split('.')[-1].lower()
                    mime_map = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png', 'webp': 'image/webp'}
                    mime = mime_map.get(ext, 'image/jpeg')
                banner_url = f"data:{mime};base64,{b64_string}"
                st.success("✅ Image loaded successfully! Submit the form below to send it for approval.")
    else:
        banner_url = st.text_input("Paste your Banner Image URL *", placeholder="https://imgbb.com/your-image-link.png")
        st.caption("Tip: Upload your image to a free host like ImgBB, then paste the direct link here.")
    
    st.markdown("---")
    st.markdown("### 📋 Banner Guidelines")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.write("- ✅ Recommended size: **1200 x 400 pixels**")
        st.write("- ✅ Format: JPG, PNG, or WebP")
        st.write("- ✅ Max file size: **5MB**")
    with col_g2:
        st.write("- ✅ Content must relate to your products")
        st.write("- ❌ No inappropriate or misleading content")
        st.write("- ⏳ Approval usually takes < 24 hours")

    submit_btn = st.form_submit_button("🚀 Submit for Approval", type="primary", use_container_width=True)
    
    if submit_btn:
        if not banner_url:
            st.error("Please provide or upload a banner image before submitting.")
        elif upload_method == "Upload from Device" and uploaded_file and uploaded_file.size > 5 * 1024 * 1024:
            st.error("Please resize your image to under 5MB before submitting.")
        else:
            with get_connection() as conn:
                conn.execute(
                    "INSERT INTO vendor_banners (user_id, media, is_active, created_at) VALUES (?, ?, 0, ?)",
                    (st.session_state.user['id'], banner_url.strip(), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
            st.success("🎉 Banner submitted successfully! It will appear on MarketSpace once an admin approves it.")
            st.rerun()

st.markdown("---")
st.subheader("📋 Your Submitted Banners")

with get_connection() as conn:
    my_banners = conn.execute(
        "SELECT * FROM vendor_banners WHERE user_id = ? ORDER BY id DESC", 
        (st.session_state.user['id'],)
    ).fetchall()

if not my_banners:
    st.info("You haven't submitted any banners yet.")
else:
    for b in my_banners:
        # FIX: Use bracket notation instead of .get() for sqlite3.Row objects
        is_active = b['is_active']
        expires = b['expires_at'] if 'expires_at' in b.keys() else None
        
        if is_active == 1 and expires:
            status = f"🟢 Active & Live (Expires: {expires})"
        elif is_active == 1:
            status = "🟢 Active & Live"
        else:
            status = "⏳ Pending Approval"
            
        with st.container(border=True):
            cols_info = st.columns([3, 1])
            with cols_info[0]:
                st.markdown(f"**Status:** {status}")
            with cols_info[1]:
                if is_active == 0:
                    if st.button("❌ Cancel Request", key=f"cancel_{b['id']}", use_container_width=True):
                        with get_connection() as conn:
                            conn.execute("DELETE FROM vendor_banners WHERE id = ? AND user_id = ?", (b['id'], st.session_state.user['id']))
                        st.warning("Banner submission cancelled.")
                        st.rerun()
            
            if b['media']:
                try:
                    st.image(b['media'], use_container_width=True)
                except Exception:
                    st.caption("*(Image preview unavailable)*")
            
            st.caption(f"Submitted on: {b['created_at'] if 'created_at' in b.keys() else 'N/A'}")

render_footer()
