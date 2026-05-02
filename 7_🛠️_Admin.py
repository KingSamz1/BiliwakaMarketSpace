import streamlit as st
import pandas as pd
from database import get_connection, init_db
from utils import apply_theme, guard_logged_in, render_footer, render_topbar, hide_admin_sidebar_if_not_admin

# --- Security & Setup ---
init_db()
apply_theme()
hide_admin_sidebar_if_not_admin()
render_topbar()

if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("Home.py")
if st.session_state.get("role") != "admin":
    st.error("You do not have permission to view this page.")
    st.switch_page("Home.py")

st.title("🛠️ Admin Control Center")
st.caption("Full overview and management of the Biliwaka platform.")

# --- Fetch Data ---
with get_connection() as conn:
    users = conn.execute("SELECT id, first_name, full_name, email, role, is_subscription FROM users ORDER BY id DESC").fetchall()
    listings = conn.execute("""
        SELECT a.id, a.title, a.category, a.price, a.clicks, a.whatsapp_clicks, a.calls, a.is_active, a.expires_at, u.email AS seller_email
        FROM ads a JOIN users u ON u.id = a.user_id ORDER BY a.id DESC
    """).fetchall()
    banners = conn.execute("SELECT id, media, target_url, expires_at FROM banner_ads ORDER BY id DESC").fetchall()
    ratings = conn.execute("SELECT r.id, r.vendor_id, r.rating, r.created_at, u.full_name FROM ratings r JOIN users u ON u.id = r.vendor_id ORDER BY r.id DESC").fetchall()

# --- PRE-CALCULATE DROPDOWNS OUTSIDE TABS (Fixes blank screen bug) ---
user_options = {f"{row['full_name']} ({row['email']})": row["id"] for row in users if row['role'] != 'admin'}
listing_options = {f"#{row['id']} - {row['title']} ({'Active' if row['is_active'] else 'Hidden'})": row["id"] for row in listings}
feat_options = {f"#{row['id']} - {row['title']}": row["id"] for row in listings}
ban_options = {f"Banner ID {row['id']} (Expires: {row['expires_at']})": row["id"] for row in banners}

# --- Tabbed Interface ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Dashboard", "👥 Users", "📢 Listings", "🖼️ Banners", "⚙️ System", "🎯 Vendor Banners"])

# ==========================================
# TAB 1: DASHBOARD
# ==========================================
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Users", len(users))
    with col2: st.metric("Total Listings", len(listings))
    with col3: 
        total_views = sum(row['clicks'] for row in listings)
        st.metric("Total Views", f"{total_views:,}")
    with col4:
        active_listings = sum(1 for row in listings if row['is_active'] == 1)
        st.metric("Active Listings", active_listings)

    st.markdown("---")
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("📈 Top Performing Listings")
        if listings:
            top_listings = sorted(listings, key=lambda x: x['clicks'], reverse=True)[:5]
            for i, row in enumerate(top_listings):
                st.markdown(f"**{i+1}. {row['title']}**")
                st.caption(f"👁 {row['clicks']} views | 💬 {row['whatsapp_clicks']} WhatsApp | 📞 {row['calls']} Calls")
        else: st.info("No listings yet.")
    with col_right:
        st.subheader("👥 Recent Users")
        if users:
            for row in users[:5]:
                role_badge = "👑 Admin" if row['role'] == 'admin' else "🛒 Vendor" if row['role'] == 'vendor' else "👤 Buyer"
                sub_badge = "⭐ Pro" if row['is_subscription'] else "Free"
                st.markdown(f"**{row['full_name']}** - {role_badge} ({sub_badge})")
                st.caption(f"✉️ {row['email']}")
        else: st.info("No users yet.")

# ==========================================
# TAB 2: USERS
# ==========================================
with tab2:
    st.subheader("All Registered Users")
    if users:
        st.dataframe(pd.DataFrame([dict(row) for row in users]), use_container_width=True, hide_index=True)
        if user_options:
            st.markdown("---")
            st.subheader("User Management")
            selected_user_label = st.selectbox("Select a user to manage", list(user_options.keys()), key="user_select")
            selected_user_id = None
            if selected_user_label:
                selected_user_id = user_options[selected_user_label]
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.button("🛒 Set as Vendor", use_container_width=True):
                    with get_connection() as conn: conn.execute("UPDATE users SET role = 'vendor' WHERE id = ?", (selected_user_id,))
                    st.success("User role updated to Vendor."); st.rerun()
            with col_b:
                if st.button("👤 Set as Buyer", use_container_width=True):
                    with get_connection() as conn: conn.execute("UPDATE users SET role = 'buyer' WHERE id = ?", (selected_user_id,))
                    st.success("User role updated to Buyer."); st.rerun()
            with col_c:
                if st.button("⚠️ Delete User", use_container_width=True):
                    with get_connection() as conn: conn.execute("DELETE FROM users WHERE id = ? AND role != 'admin'", (selected_user_id,))
                    st.warning("User deleted."); st.rerun()

# ==========================================
# TAB 3: LISTINGS MODERATION
# ==========================================
with tab3:
    st.subheader("All Listings & Moderation")
    if listings:
        st.dataframe(pd.DataFrame([dict(row) for row in listings]), use_container_width=True, hide_index=True)
        if listing_options:
            st.markdown("---")
            st.subheader("Moderation Tools")
            selected_label = st.selectbox("Select listing to moderate", list(listing_options.keys()), key="list_select")
            if selected_label:
                selected_id = listing_options[selected_label]
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("👁 Show Listing", use_container_width=True):
                        with get_connection() as conn: conn.execute("UPDATE ads SET is_active = 1 WHERE id = ?", (selected_id,))
                        st.success("Listing is now visible."); st.rerun()
                with col2:
                    if st.button("🚫 Hide Listing", use_container_width=True):
                        with get_connection() as conn: conn.execute("UPDATE ads SET is_active = 0 WHERE id = ?", (selected_id,))
                        st.success("Listing is now hidden."); st.rerun()
                with col3:
                    if st.button("🗑️ Delete Listing", use_container_width=True):
                        with get_connection() as conn: conn.execute("DELETE FROM ads WHERE id = ?", (selected_id,))
                        st.warning("Listing permanently deleted."); st.rerun()
            
            st.markdown("---")
            st.subheader("⭐ Feature a Listing")
            feat_label = st.selectbox("Select listing to feature", list(feat_options.keys()), key="feat_select")
            if feat_label:
                feat_id = feat_options[feat_label]
                if st.button("Make Featured", use_container_width=True):
                    with get_connection() as conn: conn.execute("UPDATE ads SET is_featured = 1 WHERE id = ?", (feat_id,))
                    st.success("Listing marked as featured!"); st.rerun()
    else:
        st.info("No listings found.")

# ==========================================
# TAB 4: BANNERS
# ==========================================
with tab4:
    st.subheader("Homepage Banner Ads")
    st.caption("Manage the images that rotate on the homepage carousel.")
    if banners:
        st.dataframe(pd.DataFrame([dict(row) for row in banners]), use_container_width=True, hide_index=True)
        if ban_options:
            st.markdown("---")
            st.subheader("Remove Banner")
            ban_label = st.selectbox("Select banner to delete", list(ban_options.keys()), key="ban_select")
            if ban_label:
                ban_id = ban_options[ban_label]
                if st.button("Delete Banner", use_container_width=True):
                    with get_connection() as conn: conn.execute("DELETE FROM banner_ads WHERE id = ?", (ban_id,))
                    st.success("Banner removed."); st.rerun()
    else:
        st.info("No banners in rotation.")
        
    st.markdown("---")
    st.subheader("Add New Banner")
    with st.form("add_banner"):
        new_img_url = st.text_input("Direct Image URL")
        new_target_url = st.text_input("Target URL")
        expire_days = st.number_input("Active days", min_value=1, value=30)
        if st.form_submit_button("Upload Banner"):
            if new_img_url and new_target_url:
                from datetime import date, timedelta
                expires = (date.today() + timedelta(days=expire_days)).isoformat()
                with get_connection() as conn:
                    conn.execute("INSERT INTO banner_ads (media, target_url, expires_at) VALUES (?, ?, ?)", (new_img_url, new_target_url, expires))
                st.success("Banner added!"); st.rerun()
            else: st.error("Please provide both URLs.")

# ==========================================
# TAB 5: SYSTEM / DB
# ==========================================
with tab5:
    st.subheader("⚙️ System & Database Tools")
    st.warning("Be careful with these tools.", icon="⚠️")
    col_db1, col_db2 = st.columns(2)
    with col_db1:
        st.markdown("### Reset Data")
        if st.button("Clear ALL Ratings", use_container_width=True):
            with get_connection() as conn: conn.execute("DELETE FROM ratings"); st.success("All ratings deleted."); st.rerun()
        if st.button("Clear ALL Banners", use_container_width=True):
            with get_connection() as conn: conn.execute("DELETE FROM banner_ads"); st.success("All banners deleted."); st.rerun()
    with col_db2:
        st.markdown("### Developer Actions")
        if st.button("Force Refresh Session State", use_container_width=True):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.success("Session cleared. Please refresh the page.")
            
    st.markdown("---")
    st.markdown("### Current Database Schema")
    with get_connection() as conn:
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        for table in tables:
            with st.expander(f"Table: {table['name']}"):
                cols = conn.execute(f"PRAGMA table_info({table['name']})").fetchall()
                st.dataframe(pd.DataFrame([dict(c) for c in cols]), use_container_width=True, hide_index=True)

# ==========================================
# TAB 6: VENDOR BANNERS (UPDATED WITH DURATION)
# ==========================================
with tab6:
    st.subheader("🎯 Vendor Banners")
    st.caption("Manage banners purchased by vendors.")
    
    # Ensure expires_at column exists in case table was made before this update
    with get_connection() as conn:
        cols = conn.execute("PRAGMA table_info(vendor_banners)").fetchall()
        col_names = [c['name'] for c in cols]
        if 'expires_at' not in col_names:
            conn.execute("ALTER TABLE vendor_banners ADD COLUMN expires_at TEXT")

    with get_connection() as conn:
        vendor_bans = conn.execute("SELECT vb.id, u.full_name, vb.media, vb.is_active, vb.expires_at, vb.created_at FROM vendor_banners vb JOIN users u ON u.id = vb.user_id ORDER BY vb.is_active ASC, vb.id DESC").fetchall()
    
    if vendor_bans:
        for b in vendor_bans:
            status_str = "🟢 Active" if b['is_active'] == 1 else "⏳ Pending"
            exp_str = f" | Expires: {b['expires_at']}" if b['expires_at'] else ""
            with st.expander(f"{status_str} - Vendor: {b['full_name']} (ID {b['id']}){exp_str}"):
                if b['media']:
                    try:
                        st.image(b['media'], use_container_width=True)
                    except Exception:
                        st.write("*(Image could not be previewed)*")
                
                if b['is_active'] == 0:
                    st.markdown("**Set Duration & Approve:**")
                    c_dur, c_act, c_rej = st.columns([2, 1, 1])
                    with c_dur:
                        duration = st.selectbox("Duration", ["7 Days (1 Week)", "30 Days (1 Month)"], key=f"dur_{b['id']}")
                    with c_act:
                        if st.button("✅ Approve", key=f"approve_{b['id']}", use_container_width=True):
                            days = 7 if "7" in duration else 30
                            with get_connection() as conn:
                                conn.execute("""
                                    UPDATE vendor_banners 
                                    SET is_active = 1, expires_at = date('now', '+' || ? || ' days') 
                                    WHERE id = ?
                                """, (days, b['id']))
                            st.success(f"Approved for {days} days!"); st.rerun()
                    with c_rej:
                        if st.button("❌ Reject", key=f"reject_{b['id']}", use_container_width=True):
                            with get_connection() as conn: conn.execute("DELETE FROM vendor_banners WHERE id = ?", (b['id'],))
                            st.warning("Banner rejected."); st.rerun()
                else:
                    if st.button("🛑 Expire / Remove", key=f"remove_{b['id']}", use_container_width=True):
                        with get_connection() as conn: conn.execute("DELETE FROM vendor_banners WHERE id = ?", (b['id'],))
                        st.warning("Banner removed."); st.rerun()
    else:
        st.info("No vendor banners submitted yet.")

render_footer()