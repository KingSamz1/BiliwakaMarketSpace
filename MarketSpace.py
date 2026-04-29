import streamlit as st

from database import get_connection, init_db
from utils import apply_theme, render_footer, render_theme_toggle, render_topbar

init_db()
render_theme_toggle()
apply_theme()
render_topbar()

st.title("📢 MarketSpace")

with get_connection() as conn:
    st.subheader("🔥 Sponsored (UGX 40,000/week)")
    banners = conn.execute(
        """
        SELECT id, media, target_url
        FROM banner_ads
        WHERE expires_at > date('now')
        LIMIT 10
        """
    ).fetchall()

if banners:
    cols = st.columns(len(banners))
    for i, banner in enumerate(banners):
        with cols[i]:
            media = banner["media"]
            if ".mp4" in media:
                st.video(media)
            else:
                st.image(media, use_container_width=True)
            st.markdown(f"[Visit Sponsor]({banner['target_url']})")
else:
    st.info("No sponsored banners right now.")

with get_connection() as conn:
    ads = conn.execute(
        """
        SELECT
            a.id,
            a.user_id,
            a.title,
            a.description,
            a.media,
            a.is_featured,
            a.phone,
            a.price,
            a.category,
            a.clicks,
            u.full_name
        FROM ads a
        JOIN users u ON u.id = a.user_id
        WHERE a.expires_at > date('now') AND a.is_active = 1
        ORDER BY a.is_featured DESC, a.id DESC
        """
    ).fetchall()

search = st.text_input("Search listings")
category = st.selectbox(
    "Category filter",
    ["All", "Electronics", "Fashion", "Home & Office", "Vehicles", "Property", "Phones", "Beauty", "Agriculture", "Services", "General"],
)

filtered_ads = []
for ad in ads:
    if search and search.lower() not in (ad["title"] + " " + ad["description"]).lower():
        continue
    if category != "All" and ad["category"] != category:
        continue
    filtered_ads.append(ad)

for ad in filtered_ads:
    featured_class = "featured" if ad["is_featured"] else ""
    st.markdown(f"<div class='listing-card {featured_class}'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])

    with col1:
        if ad["media"] and ".mp4" in ad["media"]:
            st.video(ad["media"])
        elif ad["media"]:
            st.image(ad["media"], use_container_width=True)
        else:
            st.info("No media")

    with col2:
        st.subheader(ad["title"])
        st.write(ad["description"])
        st.write(f"Price: UGX {ad['price']:.0f} | Category: {ad['category']}")
        st.caption(f"Vendor: {ad['full_name']} | Clicks: {ad['clicks']}")

        if ad["is_featured"]:
            st.success("⭐ Featured (UGX 20,000/week)")

        if st.button(f"View {ad['id']}", key=f"view_{ad['id']}"):
            with get_connection() as conn:
                conn.execute("UPDATE ads SET clicks = clicks + 1 WHERE id = ?", (ad["id"],))
            st.success("Click tracked.")

        if ad["phone"]:
            if st.button("📲 WhatsApp", key=f"wa_{ad['id']}"):
                with get_connection() as conn:
                    conn.execute("UPDATE ads SET whatsapp_clicks = whatsapp_clicks + 1 WHERE id = ?", (ad["id"],))
                st.link_button("Open WhatsApp", f"https://wa.me/{ad['phone']}")
            if st.button("📞 Call", key=f"call_{ad['id']}"):
                with get_connection() as conn:
                    conn.execute("UPDATE ads SET calls = calls + 1 WHERE id = ?", (ad["id"],))
                st.link_button("Call Vendor", f"tel:{ad['phone']}")
        st.markdown(f"🔗 https://yourdomain.com/ad/{ad['id']}")

        rating = st.slider("Rate Vendor", 1, 5, 3, key=f"rate_{ad['id']}")
        if st.button("Submit Rating", key=f"s{ad['id']}"):
            with get_connection() as conn:
                conn.execute(
                    "INSERT INTO ratings(vendor_id, rating, created_at) VALUES (?, ?, date('now'))",
                    (ad["user_id"], rating),
                )
            st.success("Rating saved.")

    st.markdown("</div>", unsafe_allow_html=True)

render_footer()
