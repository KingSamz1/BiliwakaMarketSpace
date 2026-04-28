import datetime
import uuid

import pandas as pd
import streamlit as st


st.set_page_config(page_title="Biliwaka MarketPlace", layout="wide")

st.markdown(
    """
<style>
:root {
    --bg-1: #0f172a;
    --bg-2: #1e293b;
    --card: #111827;
    --card-soft: #1f2937;
    --text: #e5e7eb;
    --muted: #9ca3af;
    --accent: #22c55e;
    --accent-2: #06b6d4;
    --gold: #fbbf24;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top right, #0b1120 0%, var(--bg-1) 35%, var(--bg-2) 100%);
    color: var(--text);
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b1220 0%, #111827 100%);
}

.hero {
    background: linear-gradient(120deg, rgba(34,197,94,0.18), rgba(6,182,212,0.2));
    border: 1px solid rgba(148, 163, 184, 0.25);
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 18px;
}

.hero h1 {
    margin: 0;
    color: white;
}

.hero p {
    color: var(--muted);
    margin-top: 8px;
}

.metric-card {
    background: var(--card-soft);
    border-radius: 14px;
    border-left: 5px solid var(--accent-2);
    padding: 12px;
    margin-bottom: 8px;
}

.listing-card {
    background: linear-gradient(150deg, rgba(17,24,39,0.95), rgba(31,41,55,0.95));
    border-radius: 16px;
    border: 1px solid rgba(148,163,184,0.18);
    padding: 14px;
    margin-bottom: 14px;
}

.listing-title {
    color: white;
    margin-bottom: 6px;
    font-size: 1.25rem;
    font-weight: 700;
}

.badge {
    display: inline-block;
    color: #111827;
    background: var(--gold);
    border-radius: 999px;
    padding: 2px 10px;
    font-size: 0.75rem;
    margin-right: 6px;
}

.subtle {
    color: var(--muted);
    font-size: 0.92rem;
}

.footer {
    text-align: center;
    color: #9ca3af;
    font-size: 0.9rem;
    padding: 20px 0;
}
</style>
""",
    unsafe_allow_html=True,
)


FREE_LIMIT = 4
EXPIRY_DAYS = 45
FEATURED_DAYS = 7
BANNER_DAYS = 7


def now() -> datetime.datetime:
    return datetime.datetime.now()


def to_price_value(value: str) -> float:
    cleaned = "".join(ch for ch in str(value) if ch.isdigit() or ch == ".")
    if not cleaned:
        return 0.0
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def format_ugx(value: str) -> str:
    amount = int(to_price_value(value))
    return f"UGX {amount:,}" if amount > 0 else str(value)


def init_state() -> None:
    if "active_user" not in st.session_state:
        st.session_state.active_user = ""

    if "users" not in st.session_state:
        st.session_state.users = {}

    if "favorites" not in st.session_state:
        st.session_state.favorites = {}

    if "listings" not in st.session_state:
        st.session_state.listings = pd.DataFrame(
            columns=[
                "id",
                "vendor",
                "title",
                "category",
                "condition",
                "description",
                "price",
                "price_value",
                "location",
                "image",
                "featured",
                "featured_until",
                "created_at",
                "expires_at",
                "status",
                "views",
                "whatsapp_clicks",
                "calls",
            ]
        )

    if "banners" not in st.session_state:
        st.session_state.banners = []

    if "ratings" not in st.session_state:
        st.session_state.ratings = []

    if "show_how_to_use" not in st.session_state:
        st.session_state.show_how_to_use = True


def normalize_state_types() -> None:
    # Handles old session formats to prevent cloud/runtime crashes.
    if not isinstance(st.session_state.favorites, dict):
        st.session_state.favorites = {}
    if not isinstance(st.session_state.banners, list):
        st.session_state.banners = []
    if not isinstance(st.session_state.ratings, list):
        st.session_state.ratings = []


def cleanup_expired() -> None:
    df = st.session_state.listings
    if len(df) > 0:
        active = df[df["expires_at"] > now()].copy()
        active.loc[active["featured_until"] <= now(), "featured"] = False
        st.session_state.listings = active

    active_banners = [b for b in st.session_state.banners if b["expires_at"] > now()]
    st.session_state.banners = active_banners


def last_7_days_count(vendor: str) -> int:
    df = st.session_state.listings
    cutoff = now() - datetime.timedelta(days=7)
    if len(df) == 0:
        return 0
    return len(df[(df["vendor"] == vendor) & (df["created_at"] > cutoff)])


def get_rating_summary(vendor: str) -> tuple[float, int]:
    vendor_ratings = [r["rating"] for r in st.session_state.ratings if r["vendor"] == vendor]
    if not vendor_ratings:
        return 0.0, 0
    avg = round(sum(vendor_ratings) / len(vendor_ratings), 1)
    return avg, len(vendor_ratings)


def share_link(title: str, item_type: str) -> str:
    msg = f"Check this {item_type}: {title} on Biliwaka MarketPlace"
    return "https://wa.me/?text=" + msg.replace(" ", "%20")


def safe_html(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


init_state()
normalize_state_types()
cleanup_expired()


st.markdown(
    """
<div class="hero">
    <h1>🏪 Biliwaka MarketPlace</h1>
    <p>Modern marketplace for buying, selling, featured ads, banner campaigns, and trusted vendor ratings.</p>
</div>
""",
    unsafe_allow_html=True,
)

if st.session_state.show_how_to_use:
    st.info("Welcome! Start here: how to use Biliwaka MarketPlace.")
    with st.expander("📘 How to use this marketplace", expanded=True):
        st.markdown(
            """
1. Browse listings using search, category, location, and sorting.
2. Login from the sidebar with phone/email to publish and manage ads.
3. Create listings (first 4 in 7 days are free; featured ads are paid).
4. Use WhatsApp/Call buttons to contact vendors quickly.
5. Rate vendors to build trust and use favorites to save listings.
"""
        )
        if st.button("Got it, hide guide"):
            st.session_state.show_how_to_use = False
            st.rerun()


st.sidebar.title("Account")
auth_value = st.sidebar.text_input("Phone or Email", value=st.session_state.active_user)
if st.sidebar.button("Login / Switch User"):
    st.session_state.active_user = auth_value.strip()
    st.success("Logged in.")

if st.sidebar.button("Logout"):
    st.session_state.active_user = ""
    st.info("Logged out.")

vendor = st.session_state.active_user
st.sidebar.caption(f"Active user: `{vendor}`" if vendor else "Not logged in")


if vendor and vendor not in st.session_state.favorites:
    st.session_state.favorites[vendor] = []


df = st.session_state.listings.copy()
if len(df) > 0:
    df = df.sort_values(by=["featured", "created_at"], ascending=[False, False])

total_listings = len(df)
featured_count = int(df["featured"].sum()) if len(df) > 0 else 0
active_vendors = df["vendor"].nunique() if len(df) > 0 else 0
avg_price = int(df["price_value"].mean()) if len(df) > 0 else 0

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.markdown(f'<div class="metric-card"><b>Active Listings</b><br>{total_listings}</div>', unsafe_allow_html=True)
col_m2.markdown(f'<div class="metric-card"><b>Featured Ads</b><br>{featured_count}</div>', unsafe_allow_html=True)
col_m3.markdown(f'<div class="metric-card"><b>Active Vendors</b><br>{active_vendors}</div>', unsafe_allow_html=True)
col_m4.markdown(
    f'<div class="metric-card"><b>Average Price</b><br>{"UGX {:,}".format(avg_price) if avg_price else "N/A"}</div>',
    unsafe_allow_html=True,
)


st.markdown("## 📢 Banner Ads (UGX 20,000 / week)")
if st.session_state.banners:
    banner_cols = st.columns(2)
    for i, ad in enumerate(st.session_state.banners[:10]):
        with banner_cols[i % 2]:
            st.caption(f"Campaign ends: {ad['expires_at'].strftime('%d %b %Y')}")
            if ad["type"] == "image":
                st.image(ad["file"], use_container_width=True)
            else:
                st.video(ad["file"])
else:
    st.info("No active banners yet.")

st.markdown("---")
st.markdown("## 🔎 Discover Listings")

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([2, 1, 1, 1])
with filter_col1:
    search_term = st.text_input("Search title, description, or vendor")
with filter_col2:
    categories = ["All"] + (sorted(df["category"].dropna().unique().tolist()) if len(df) > 0 else [])
    chosen_category = st.selectbox("Category", categories)
with filter_col3:
    location_options = ["All"] + (sorted(df["location"].dropna().unique().tolist()) if len(df) > 0 else [])
    chosen_location = st.selectbox("Location", location_options)
with filter_col4:
    sort_by = st.selectbox("Sort", ["Newest", "Price: Low to High", "Price: High to Low", "Most Viewed"])

featured_only = st.checkbox("Show featured only", value=False)

filtered = df.copy()
if len(filtered) > 0:
    if search_term:
        term = search_term.lower().strip()
        filtered = filtered[
            filtered["title"].str.lower().str.contains(term, na=False)
            | filtered["description"].str.lower().str.contains(term, na=False)
            | filtered["vendor"].str.lower().str.contains(term, na=False)
        ]
    if chosen_category != "All":
        filtered = filtered[filtered["category"] == chosen_category]
    if chosen_location != "All":
        filtered = filtered[filtered["location"] == chosen_location]
    if featured_only:
        filtered = filtered[filtered["featured"] == True]

    if sort_by == "Price: Low to High":
        filtered = filtered.sort_values(by="price_value", ascending=True)
    elif sort_by == "Price: High to Low":
        filtered = filtered.sort_values(by="price_value", ascending=False)
    elif sort_by == "Most Viewed":
        filtered = filtered.sort_values(by="views", ascending=False)
    else:
        filtered = filtered.sort_values(by="created_at", ascending=False)

if len(filtered) == 0:
    st.warning("No listings matched your filters.")
else:
    for _, row in filtered.iterrows():
        listing_id = row["id"]
        listing_index = st.session_state.listings.index[st.session_state.listings["id"] == listing_id]
        avg_rating, rating_count = get_rating_summary(row["vendor"])
        rating_text = f"⭐ {avg_rating} ({rating_count})" if rating_count else "No ratings yet"

        with st.container(border=True):
            st.markdown(
                f"""
<div class="listing-card">
    <div class="listing-title">{safe_html(row["title"])}</div>
    <span class="badge">{safe_html(row["category"])}</span>
    <span class="badge">{safe_html(row["condition"])}</span>
    <p class="subtle">Vendor: {safe_html(row["vendor"])} | {rating_text}</p>
    <p>{safe_html(row["description"])}</p>
    <p>📍 {safe_html(row["location"])} | 💰 <b>{format_ugx(row["price"])}</b></p>
    <p class="subtle">Views: {int(row["views"])} | WhatsApp clicks: {int(row["whatsapp_clicks"])} | Calls: {int(row["calls"])}</p>
</div>
""",
                unsafe_allow_html=True,
            )

            if row["image"]:
                st.image(row["image"], use_container_width=True)

            action_col1, action_col2, action_col3, action_col4 = st.columns(4)

            with action_col1:
                if st.button("👁 View", key=f"view_{listing_id}"):
                    if len(listing_index) > 0:
                        st.session_state.listings.at[listing_index[0], "views"] += 1
                        st.rerun()

            with action_col2:
                if st.button("💬 WhatsApp", key=f"wa_{listing_id}"):
                    if len(listing_index) > 0:
                        st.session_state.listings.at[listing_index[0], "whatsapp_clicks"] += 1
                    wa_url = f"https://wa.me/{row['vendor']}?text=Interested%20in%20{row['title']}"
                    st.link_button("Open WhatsApp", wa_url, use_container_width=True)

            with action_col3:
                if st.button("📞 Call", key=f"call_{listing_id}"):
                    if len(listing_index) > 0:
                        st.session_state.listings.at[listing_index[0], "calls"] += 1
                    st.link_button("Call Vendor", f"tel:{row['vendor']}", use_container_width=True)

            with action_col4:
                st.link_button("🔗 Share", share_link(row["title"], "listing"), use_container_width=True)

            if vendor:
                favs = st.session_state.favorites.setdefault(vendor, [])
                in_fav = listing_id in favs
                if st.button("⭐ Remove Favorite" if in_fav else "⭐ Save Favorite", key=f"fav_{listing_id}_{vendor}"):
                    if in_fav:
                        favs.remove(listing_id)
                    else:
                        favs.append(listing_id)
                    st.session_state.favorites[vendor] = favs
                    st.rerun()

            if vendor and row["vendor"] == vendor:
                if st.button("🗑 Delete My Listing", key=f"del_{listing_id}"):
                    st.session_state.listings = st.session_state.listings[st.session_state.listings["id"] != listing_id]
                    st.success("Listing deleted.")
                    st.rerun()


st.markdown("---")
st.markdown("## ➕ Create Listing")

with st.form("listing_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        title = st.text_input("Title")
        category = st.selectbox("Category", ["Electronics", "Fashion", "Vehicles", "Property", "Home", "Services", "Other"])
        condition = st.selectbox("Condition", ["Brand New", "Like New", "Used", "Refurbished"])
        price = st.text_input("Price (UGX)")
    with c2:
        location = st.text_input("Location")
        description = st.text_area("Description")
        photo = st.file_uploader("Photo", type=["png", "jpg", "jpeg"], accept_multiple_files=False)
        featured = st.checkbox("⭐ Featured Ad (40K / 7 days)")

    publish = st.form_submit_button("Publish Listing")

if publish:
    if not vendor:
        st.error("Login required before publishing.")
    elif not title.strip() or not price.strip() or not location.strip():
        st.error("Title, price, and location are required.")
    else:
        recent_count = last_7_days_count(vendor)
        if recent_count >= FREE_LIMIT and not featured:
            st.error("Free listing limit reached (4 in 7 days). Upgrade to featured.")
        else:
            listing = {
                "id": str(uuid.uuid4()),
                "vendor": vendor,
                "title": title.strip(),
                "category": category,
                "condition": condition,
                "description": description.strip(),
                "price": price.strip(),
                "price_value": to_price_value(price),
                "location": location.strip(),
                "image": photo.getvalue() if photo else None,
                "featured": featured,
                "featured_until": now() + datetime.timedelta(days=FEATURED_DAYS) if featured else now(),
                "created_at": now(),
                "expires_at": now() + datetime.timedelta(days=EXPIRY_DAYS),
                "status": "active",
                "views": 0,
                "whatsapp_clicks": 0,
                "calls": 0,
            }

            st.session_state.listings = pd.concat([st.session_state.listings, pd.DataFrame([listing])], ignore_index=True)
            if featured:
                st.info("Pay Featured Ad: https://wa.me/256775998783?text=FEATURED%2040000%20UGX%207%20DAYS")
            st.success("Listing published successfully.")
            st.rerun()


st.markdown("---")
st.markdown("## 📢 Create Banner Ad (UGX 20,000 / week)")
with st.form("banner_form", clear_on_submit=True):
    banner_file = st.file_uploader("Upload Banner Image/Video", type=["png", "jpg", "jpeg", "mp4", "mov"])
    banner_type = st.selectbox("Banner Type", ["image", "video"])
    create_banner = st.form_submit_button("Create Banner")

if create_banner:
    if not vendor:
        st.error("Login required before creating a banner.")
    elif not banner_file:
        st.error("Upload a banner file first.")
    else:
        st.session_state.banners.append(
            {
                "id": str(uuid.uuid4()),
                "owner": vendor,
                "file": banner_file.getvalue(),
                "type": banner_type,
                "created_at": now(),
                "expires_at": now() + datetime.timedelta(days=BANNER_DAYS),
            }
        )
        st.info("Pay Banner: https://wa.me/256775998783?text=BANNER%2020000%20UGX%207%20DAYS")
        st.success("Banner campaign submitted.")


st.markdown("---")
st.markdown("## ⭐ Rate Vendors")
with st.form("rating_form", clear_on_submit=True):
    rated_vendor = st.text_input("Vendor Phone or Email")
    rating = st.slider("Rating", 1, 5, 5)
    review = st.text_area("Review")
    submit_rating = st.form_submit_button("Submit Rating")

if submit_rating:
    if not rated_vendor.strip():
        st.error("Vendor ID is required.")
    else:
        st.session_state.ratings.append(
            {
                "id": str(uuid.uuid4()),
                "vendor": rated_vendor.strip(),
                "rating": int(rating),
                "review": review.strip(),
                "created_at": now(),
            }
        )
        st.success("Rating submitted.")


if st.session_state.ratings:
    st.markdown("## 📊 Vendor Reputation Board")
    ratings_df = pd.DataFrame(st.session_state.ratings)
    rep = (
        ratings_df.groupby("vendor")
        .agg(avg_rating=("rating", "mean"), reviews=("rating", "count"))
        .sort_values(by=["avg_rating", "reviews"], ascending=[False, False])
    )
    rep["avg_rating"] = rep["avg_rating"].round(2)
    st.dataframe(rep, use_container_width=True)


if vendor:
    st.markdown("---")
    st.markdown("## 🧑‍💼 My Dashboard")

    my_listings = st.session_state.listings[st.session_state.listings["vendor"] == vendor]
    my_favorites = st.session_state.favorites.get(vendor, [])
    my_views = int(my_listings["views"].sum()) if len(my_listings) > 0 else 0
    my_leads = int(my_listings["whatsapp_clicks"].sum() + my_listings["calls"].sum()) if len(my_listings) > 0 else 0

    d1, d2, d3, d4 = st.columns(4)
    d1.metric("My Listings", len(my_listings))
    d2.metric("My Total Views", my_views)
    d3.metric("My Leads", my_leads)
    d4.metric("Saved Favorites", len(my_favorites))

    if my_favorites:
        st.markdown("### ⭐ My Favorite Listings")
        fav_df = st.session_state.listings[st.session_state.listings["id"].isin(my_favorites)]
        if len(fav_df) > 0:
            st.dataframe(
                fav_df[["title", "price", "location", "vendor", "views", "whatsapp_clicks", "calls"]],
                use_container_width=True,
            )
        else:
            st.caption("No active favorite listings right now.")

st.markdown("---")
st.markdown('<div class="footer">© 2026 Biliwaka MarketPlace</div>', unsafe_allow_html=True)
