import streamlit as st

from database import get_connection, init_db
from utils import apply_theme, guard_admin, render_footer, render_theme_toggle, render_topbar

init_db()
render_theme_toggle()
apply_theme()
render_topbar()
guard_admin()

st.title("Admin Panel")
st.caption("Overview of users and listings.")

with get_connection() as conn:
    users = conn.execute(
        "SELECT id, first_name, full_name, email, role, is_subscription FROM users ORDER BY id DESC"
    ).fetchall()
    listings = conn.execute(
        """
        SELECT a.id, a.title, a.category, a.price, a.clicks, a.whatsapp_clicks, a.calls, a.is_active, a.expires_at, u.email AS seller_email
        FROM ads a
        JOIN users u ON u.id = a.user_id
        ORDER BY a.id DESC
        """
    ).fetchall()
    banners = conn.execute("SELECT id, media, target_url, expires_at FROM banner_ads ORDER BY id DESC").fetchall()
    ratings = conn.execute("SELECT id, vendor_id, rating, created_at FROM ratings ORDER BY id DESC").fetchall()

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Users", len(users))
with col2:
    st.metric("Total Listings", len(listings))
col3, col4 = st.columns(2)
with col3:
    st.metric("Banner Ads", len(banners))
with col4:
    st.metric("Ratings", len(ratings))

st.subheader("Users")
if users:
    st.dataframe([dict(row) for row in users], use_container_width=True)
else:
    st.info("No users found.")

st.subheader("Listings")
if listings:
    st.dataframe([dict(row) for row in listings], use_container_width=True)
else:
    st.info("No listings found.")

if listings:
    st.subheader("Moderation")
    listing_options = {f"#{row['id']} - {row['title']}": row["id"] for row in listings}
    selected_label = st.selectbox("Select listing", list(listing_options.keys()))
    selected_id = listing_options[selected_label]
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Hide Listing"):
            with get_connection() as conn:
                conn.execute("UPDATE ads SET is_active = 0 WHERE id = ?", (selected_id,))
            st.success("Listing hidden.")
            st.rerun()
    with col_b:
        if st.button("Show Listing"):
            with get_connection() as conn:
                conn.execute("UPDATE ads SET is_active = 1 WHERE id = ?", (selected_id,))
            st.success("Listing visible.")
            st.rerun()

st.subheader("Banner Ads")
if banners:
    st.dataframe([dict(row) for row in banners], use_container_width=True)
else:
    st.info("No banner ads found.")

st.subheader("Ratings")
if ratings:
    st.dataframe([dict(row) for row in ratings], use_container_width=True)
else:
    st.info("No ratings found.")

render_footer()
