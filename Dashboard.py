import streamlit as st

from datetime import datetime, timedelta

from database import get_connection, init_db
from utils import apply_theme, guard_logged_in, render_footer, render_theme_toggle, render_topbar

init_db()
render_theme_toggle()
apply_theme()
render_topbar()
guard_logged_in()

st.title("Dashboard")
user = st.session_state.user
st.write(f"Logged in as: **{user['full_name']}** ({user['role']})")

st.subheader("📊 Vendor Dashboard")
with st.form("new_ad", clear_on_submit=True):
    title = st.text_input("Title")
    description = st.text_area("Description")
    media = st.text_input("Image/Video URL")
    phone = st.text_input("Phone (for WhatsApp/Call links)")
    price = st.number_input("Price (UGX)", min_value=0.0, step=1000.0)
    category = st.selectbox(
        "Category",
        ["Electronics", "Fashion", "Home & Office", "Vehicles", "Property", "Phones", "Beauty", "Agriculture", "Services", "General"],
    )
    featured = st.checkbox("Featured (UGX 20,000/week)")
    submit = st.form_submit_button("Post Ad")

if submit:
    if not title.strip() or not description.strip():
        st.error("Title and description are required.")
    else:
        week_ago = datetime.now() - timedelta(days=7)
        with get_connection() as conn:
            count = conn.execute(
                """
                SELECT COUNT(*) AS n
                FROM ads
                WHERE user_id = ? AND created_at > ?
                """,
                (user["id"], week_ago.strftime("%Y-%m-%d")),
            ).fetchone()["n"]

            # Non-subscription vendors are limited to 4 ads every 7 days.
            if (not user.get("is_subscription", False)) and count >= 4 and not featured:
                st.error("Limit reached (4 ads / 7 days). Upgrade to subscription or use featured.")
            else:
                now = datetime.now()
                expiry = now + timedelta(days=45)
                if featured:
                    expiry = now + timedelta(days=7)
                conn.execute(
                    """
                    INSERT INTO ads(
                        user_id, phone, title, description, media, is_featured, clicks, whatsapp_clicks, calls, is_active,
                        created_at, expires_at, category, price
                    )
                    VALUES (?, ?, ?, ?, ?, ?, 0, 0, 0, 1, ?, ?, ?, ?)
                    """,
                    (
                        user["id"],
                        phone.strip(),
                        title.strip(),
                        description.strip(),
                        media.strip(),
                        int(featured),
                        now.strftime("%Y-%m-%d"),
                        expiry.strftime("%Y-%m-%d"),
                        category,
                        price,
                    ),
                )
                st.success("Ad posted.")

st.subheader("Your ads")
with get_connection() as conn:
    rows = conn.execute(
        """
        SELECT id, title, category, price, is_featured, clicks, whatsapp_clicks, calls, is_active, expires_at
        FROM ads
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user["id"],),
    ).fetchall()

if not rows:
    st.info("No ads yet.")
else:
    for row in rows:
        featured_class = "featured" if row["is_featured"] else ""
        st.markdown(
            f"<div class='listing-card {featured_class}'><b>#{row['id']} {row['title']}</b>"
            f"<div class='listing-price'>UGX {row['price']:.0f}</div>"
            f"<small>{row['category']} | Views: {row['clicks']} | WhatsApp: {row['whatsapp_clicks']} | Calls: {row['calls']}"
            f" | {'Active' if row['is_active'] else 'Hidden'} | Expires: {row['expires_at']}</small></div>",
            unsafe_allow_html=True,
        )

with get_connection() as conn:
    avg_rating_row = conn.execute(
        "SELECT ROUND(AVG(rating), 2) AS avg_rating, COUNT(*) AS n FROM ratings WHERE vendor_id = ?",
        (user["id"],),
    ).fetchone()
col1, col2 = st.columns(2)
with col1:
    st.metric("Average Vendor Rating", avg_rating_row["avg_rating"] or 0)
with col2:
    st.metric("Total Ratings", avg_rating_row["n"])

if user["role"] == "admin":
    st.subheader("Admin quick actions")
    with st.form("new_banner", clear_on_submit=True):
        media = st.text_input("Banner media URL")
        target_url = st.text_input("Target URL", value="https://example.com")
        days = st.number_input("Days until banner expiry", min_value=1, value=7)
        add_banner = st.form_submit_button("Add Banner Ad")
    if add_banner and media.strip():
        with get_connection() as conn:
            expires_at = (datetime.now() + timedelta(days=int(days))).strftime("%Y-%m-%d")
            conn.execute(
                "INSERT INTO banner_ads(media, target_url, expires_at) VALUES (?, ?, ?)",
                (media.strip(), target_url.strip(), expires_at),
            )
        st.success("Banner added.")

render_footer()
