import base64
import datetime
import hashlib
import hmac
import sqlite3
import uuid

import pandas as pd
import streamlit as st


st.set_page_config(page_title="Biliwaka MarketPlace", layout="wide")

st.markdown(
    """
<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top right, #0b1120 0%, #0f172a 35%, #1e293b 100%);
    color: #e5e7eb;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b1220 0%, #111827 100%);
}
.hero {
    background: linear-gradient(120deg, rgba(34,197,94,0.18), rgba(6,182,212,0.2));
    border: 1px solid rgba(148,163,184,0.25);
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 12px;
}
.footer {
    text-align: center;
    color: #9ca3af;
    font-size: 0.9rem;
    padding: 16px 0;
}
</style>
""",
    unsafe_allow_html=True,
)

DB_PATH = "market.db"
FREE_LIMIT = 4
LISTING_EXPIRY_DAYS = 45
FEATURED_DAYS = 7
BANNER_DAYS = 7
ADMIN_PASSWORD_HASH = "093637e073b29dd5a1fa6116724340442a9ec80e8f569eb3ea949063ad3e64a9"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


conn = get_conn()


def init_db() -> None:
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS vendors(
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                whatsapp_phone TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS listings(
                id TEXT PRIMARY KEY,
                vendor_id TEXT NOT NULL,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                item_condition TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                location TEXT NOT NULL,
                featured INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                views INTEGER DEFAULT 0,
                whatsapp_clicks INTEGER DEFAULT 0,
                calls INTEGER DEFAULT 0,
                FOREIGN KEY(vendor_id) REFERENCES vendors(id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS banner_ads(
                id TEXT PRIMARY KEY,
                vendor_id TEXT NOT NULL,
                media_b64 TEXT NOT NULL,
                media_type TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                FOREIGN KEY(vendor_id) REFERENCES vendors(id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ratings(
                id TEXT PRIMARY KEY,
                vendor_id TEXT NOT NULL,
                rating INTEGER NOT NULL,
                comment TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(vendor_id) REFERENCES vendors(id)
            )
            """
        )


def ensure_listings_visibility_column() -> None:
    # Adds an admin-controlled "visibility" flag for moderation.
    existing = conn.execute("PRAGMA table_info(listings)").fetchall()
    cols = {r["name"] for r in existing}
    if "is_active" not in cols:
        with conn:
            conn.execute("ALTER TABLE listings ADD COLUMN is_active INTEGER DEFAULT 1")


def ensure_session() -> None:
    if "vendor_id" not in st.session_state:
        st.session_state.vendor_id = None
    if "show_help" not in st.session_state:
        st.session_state.show_help = True
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False


def now() -> datetime.datetime:
    return datetime.datetime.now()


def now_iso() -> str:
    return now().isoformat()


def future_iso(days: int) -> str:
    return (now() + datetime.timedelta(days=days)).isoformat()


def hash_pass(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_pass(password: str, stored_hash: str) -> bool:
    return hash_pass(password) == stored_hash


def verify_admin_password(password: str) -> bool:
    candidate = hash_pass(password)
    return hmac.compare_digest(candidate, ADMIN_PASSWORD_HASH)


def clean_phone_for_uganda(raw: str) -> str:
    digits = "".join(ch for ch in str(raw) if ch.isdigit())
    if not digits:
        return ""
    if digits.startswith("256"):
        local = digits[3:]
    elif digits.startswith("0"):
        local = digits[1:]
    else:
        local = digits
    return f"256{local}"


def can_post_free(vendor_id: str) -> bool:
    week_ago = (now() - datetime.timedelta(days=7)).isoformat()
    cur = conn.execute(
        "SELECT COUNT(*) AS c FROM listings WHERE vendor_id=? AND created_at>=?",
        (vendor_id, week_ago),
    )
    return cur.fetchone()["c"] < FREE_LIMIT


def get_vendor(vendor_id: str | None) -> sqlite3.Row | None:
    if not vendor_id:
        return None
    cur = conn.execute("SELECT * FROM vendors WHERE id=?", (vendor_id,))
    return cur.fetchone()


def cleanup_expired() -> None:
    now_s = now_iso()
    with conn:
        conn.execute("DELETE FROM listings WHERE expires_at < ?", (now_s,))
        conn.execute("DELETE FROM banner_ads WHERE expires_at < ?", (now_s,))


def share_link(title: str) -> str:
    msg = f"Check this listing: {title} on Biliwaka MarketPlace"
    return "https://wa.me/?text=" + msg.replace(" ", "%20")


def seed_prelistings() -> None:
    seeds = [
        {
            "name": "Elijah Shoe World",
            "phone": "0775000101",
            "wa": "0775000101",
            "title": "Elijah Shoe World",
            "category": "Fashion",
            "condition": "Brand New",
            "description": "Quality men and women shoes, office shoes, sneakers, and school shoes at fair prices.",
            "price": 85000.0,
            "location": "Kampala",
        },
        {
            "name": "Mafashid Collections",
            "phone": "0775000102",
            "wa": "0775000102",
            "title": "Mafashid Collections",
            "category": "Fashion",
            "condition": "Brand New",
            "description": "Trendy shoe collections with new arrivals weekly, including casual, official, and party footwear.",
            "price": 95000.0,
            "location": "Kampala",
        },
        {
            "name": "Sarahs Touch Salon",
            "phone": "0775000103",
            "wa": "0775000103",
            "title": "Sarahs Touch Salon",
            "category": "Salon",
            "condition": "Like New",
            "description": "Professional salon services: braiding, hair treatment, manicure, pedicure, and bridal touch-ups.",
            "price": 40000.0,
            "location": "Kampala",
        },
    ]
    with conn:
        for item in seeds:
            phone = clean_phone_for_uganda(item["phone"])
            wa = clean_phone_for_uganda(item["wa"])
            existing_vendor = conn.execute("SELECT id FROM vendors WHERE phone=?", (phone,)).fetchone()
            if existing_vendor:
                vendor_id = existing_vendor["id"]
            else:
                vendor_id = str(uuid.uuid4())
                conn.execute(
                    "INSERT INTO vendors (id,name,phone,password_hash,whatsapp_phone,created_at) VALUES (?,?,?,?,?,?)",
                    (
                        vendor_id,
                        item["name"],
                        phone,
                        hash_pass(str(uuid.uuid4())),
                        wa,
                        now_iso(),
                    ),
                )

            existing_listing = conn.execute(
                "SELECT id FROM listings WHERE vendor_id=? AND title=?",
                (vendor_id, item["title"]),
            ).fetchone()
            if not existing_listing:
                conn.execute(
                    """
                    INSERT INTO listings (
                        id,vendor_id,title,category,item_condition,description,price,location,featured,created_at,expires_at,views,whatsapp_clicks,calls
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        str(uuid.uuid4()),
                        vendor_id,
                        item["title"],
                        item["category"],
                        item["condition"],
                        item["description"],
                        item["price"],
                        item["location"],
                        1,
                        now_iso(),
                        future_iso(LISTING_EXPIRY_DAYS),
                        0,
                        0,
                        0,
                    ),
                )


def render_help_box() -> None:
    if not st.session_state.show_help:
        return
    st.info("Welcome to Biliwaka MarketPlace. Read this quick guide first.")
    with st.expander("📘 How to use", expanded=True):
        st.markdown(
            """
1. Open **Auth** and register or log in.
2. During sign up, enter your WhatsApp/Call number.  
   This becomes the default contact for your listings.
3. You can change this later in **Settings**.
4. Create a listing from **Create Listing**.
5. Buyers use WhatsApp/Call buttons that match your saved number.
"""
        )
        if st.button("Got it, hide help"):
            st.session_state.show_help = False
            st.rerun()


def auth_tab() -> None:
    st.subheader("Sign up or Log in")
    login_tab, signup_tab = st.tabs(["Log in", "Sign up"])

    with signup_tab:
        st.markdown("### Create account")
        s_name = st.text_input("Business Name", key="signup_name")
        s_phone = st.text_input("Login Phone", key="signup_phone")
        s_whatsapp = st.text_input("WhatsApp/Call Number", key="signup_wa")
        st.caption("You can change this in Settings later.")
        s_password = st.text_input("Password", type="password", key="signup_pass")
        if st.button("Sign up", key="signup_btn"):
            formatted_login = clean_phone_for_uganda(s_phone)
            formatted_wa = clean_phone_for_uganda(s_whatsapp)
            if not s_name.strip() or not formatted_login or not formatted_wa or not s_password:
                st.error("All fields are required.")
                return
            try:
                with conn:
                    conn.execute(
                        "INSERT INTO vendors (id,name,phone,password_hash,whatsapp_phone,created_at) VALUES (?,?,?,?,?,?)",
                        (
                            str(uuid.uuid4()),
                            s_name.strip(),
                            formatted_login,
                            hash_pass(s_password),
                            formatted_wa,
                            now_iso(),
                        ),
                    )
                st.success("Account created. You can now log in.")
            except sqlite3.IntegrityError:
                st.error("Phone already exists. Try logging in.")

    with login_tab:
        st.markdown("### Log in")
        l_phone = st.text_input("Phone", key="login_phone")
        l_password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Log in", key="login_btn"):
            formatted_phone = clean_phone_for_uganda(l_phone)
            cur = conn.execute("SELECT * FROM vendors WHERE phone=?", (formatted_phone,))
            vendor = cur.fetchone()
            if vendor and verify_pass(l_password, vendor["password_hash"]):
                st.session_state.vendor_id = vendor["id"]
                st.success("Logged in.")
                st.rerun()
            else:
                st.error("Invalid phone or password.")


def settings_tab(vendor: sqlite3.Row | None) -> None:
    st.subheader("Settings")
    if not vendor:
        st.warning("Log in to use settings.")
        return
    st.write(f"Logged in as: **{vendor['name']}**")
    new_name = st.text_input("Business Name", value=vendor["name"])
    new_whatsapp = st.text_input("Default WhatsApp/Call Number", value=vendor["whatsapp_phone"])
    st.caption("This number is used automatically on all your listing buttons.")
    if st.button("Save settings"):
        normalized = clean_phone_for_uganda(new_whatsapp)
        if not new_name.strip() or not normalized:
            st.error("Provide valid name and number.")
            return
        with conn:
            conn.execute(
                "UPDATE vendors SET name=?, whatsapp_phone=? WHERE id=?",
                (new_name.strip(), normalized, vendor["id"]),
            )
        st.success("Settings updated.")
        st.rerun()

    if st.button("Logout"):
        st.session_state.vendor_id = None
        st.success("Logged out.")
        st.rerun()


def create_listing_tab(vendor: sqlite3.Row | None) -> None:
    st.subheader("Create Listing")
    if not vendor:
        st.warning("Please log in first.")
        return

    if not can_post_free(vendor["id"]):
        st.warning("Free limit reached (4 listings in 7 days). Use Featured listing.")

    with st.form("create_listing", clear_on_submit=True):
        title = st.text_input("Title")
        category = st.selectbox("Category", ["Electronics", "Fashion", "Salon", "Vehicles", "Property", "Home", "Services", "Other"])
        item_condition = st.selectbox("Condition", ["Brand New", "Like New", "Used", "Refurbished"])
        price = st.number_input("Price (UGX)", min_value=0.0, step=1000.0)
        location = st.text_input("Location")
        description = st.text_area("Description")
        featured = st.checkbox("Featured Ad (UGX 40,000 / 7 days)")
        submitted = st.form_submit_button("Publish")

    if submitted:
        if not title.strip() or not location.strip() or price <= 0:
            st.error("Title, location and valid price are required.")
            return
        if not featured and not can_post_free(vendor["id"]):
            st.error("Free posting limit reached. Enable featured ad.")
            return

        expiry_days = FEATURED_DAYS if featured else LISTING_EXPIRY_DAYS
        with conn:
            conn.execute(
                """
                INSERT INTO listings (
                    id,vendor_id,title,category,item_condition,description,price,location,featured,created_at,expires_at,views,whatsapp_clicks,calls
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    str(uuid.uuid4()),
                    vendor["id"],
                    title.strip(),
                    category,
                    item_condition,
                    description.strip(),
                    float(price),
                    location.strip(),
                    1 if featured else 0,
                    now_iso(),
                    future_iso(expiry_days),
                    0,
                    0,
                    0,
                ),
            )
        if featured:
            st.info("Pay Featured Ad: https://wa.me/256775998783?text=FEATURED%2040000%20UGX%207%20DAYS")
        st.success("Listing published.")
        st.rerun()


def create_banner_tab(vendor: sqlite3.Row | None) -> None:
    st.subheader("Create Banner Ad")
    if not vendor:
        st.warning("Please log in first.")
        return

    with st.form("banner_form", clear_on_submit=True):
        file = st.file_uploader("Upload image/video", type=["png", "jpg", "jpeg", "mp4", "mov"])
        submit = st.form_submit_button("Publish Banner (UGX 20,000)")
    if submit:
        if not file:
            st.error("Please upload media.")
            return
        media_b64 = base64.b64encode(file.read()).decode()
        with conn:
            conn.execute(
                "INSERT INTO banner_ads (id,vendor_id,media_b64,media_type,created_at,expires_at) VALUES (?,?,?,?,?,?)",
                (
                    str(uuid.uuid4()),
                    vendor["id"],
                    media_b64,
                    file.type,
                    now_iso(),
                    future_iso(BANNER_DAYS),
                ),
            )
        st.info("Pay Banner: https://wa.me/256775998783?text=BANNER%2020000%20UGX%207%20DAYS")
        st.success("Banner added.")
        st.rerun()


def marketplace_tab(vendor: sqlite3.Row | None) -> None:
    st.subheader("Marketplace")
    cur = conn.execute(
        """
        SELECT l.*, v.name AS vendor_name, v.whatsapp_phone AS vendor_phone
        FROM listings l
        JOIN vendors v ON l.vendor_id = v.id
        WHERE l.expires_at > ?
          AND l.is_active = 1
        ORDER BY l.featured DESC, l.created_at DESC
        """
        ,
        (now_iso(),),
    )
    rows = cur.fetchall()
    if not rows:
        st.info("No active listings yet.")
    else:
        listing_df = pd.DataFrame([dict(r) for r in rows])
        q = st.text_input("Search")
        if q.strip():
            pattern = q.strip().lower()
            listing_df = listing_df[
                listing_df["title"].str.lower().str.contains(pattern, na=False)
                | listing_df["description"].str.lower().str.contains(pattern, na=False)
                | listing_df["location"].str.lower().str.contains(pattern, na=False)
            ]
        for _, row in listing_df.iterrows():
            badge = "🔥 FEATURED" if int(row["featured"]) == 1 else ""
            st.markdown(f"### {row['title']} {badge}")
            st.write(f"Vendor: {row['vendor_name']}")
            st.write(f"Price: UGX {int(row['price']):,}")
            st.write(f"Location: {row['location']}")
            st.write(row["description"] or "-")
            cols = st.columns(3)
            wa_message = f"Hello, I am interested in {row['title']} and I saw it on Biliwaka MarketPlace."
            wa_url = f"https://wa.me/{row['vendor_phone']}?text={wa_message.replace(' ', '%20')}"
            call_url = f"tel:{row['vendor_phone']}"

            with cols[0]:
                if st.button("WhatsApp", key=f"wa_{row['id']}"):
                    with conn:
                        conn.execute(
                            "UPDATE listings SET whatsapp_clicks=whatsapp_clicks+1 WHERE id=?",
                            (row["id"],),
                        )
                    st.link_button("Open WhatsApp", wa_url)
            with cols[1]:
                if st.button("Call", key=f"call_{row['id']}"):
                    with conn:
                        conn.execute("UPDATE listings SET calls=calls+1 WHERE id=?", (row["id"],))
                    st.link_button("Call Vendor", call_url)
            with cols[2]:
                st.link_button("Share", share_link(row["title"]))

            if vendor and vendor["id"] == row["vendor_id"]:
                if st.button("Delete listing", key=f"del_{row['id']}"):
                    with conn:
                        conn.execute("DELETE FROM listings WHERE id=?", (row["id"],))
                    st.success("Deleted.")
                    st.rerun()
            st.markdown("---")

    st.markdown("### Sponsored Banners")
    b_cur = conn.execute(
        """
        SELECT * FROM banner_ads
        ORDER BY created_at DESC
        LIMIT 10
        """
    )
    ads = b_cur.fetchall()
    if not ads:
        st.caption("No active banners.")
    else:
        for ad in ads:
            media = base64.b64decode(ad["media_b64"])
            if "video" in ad["media_type"]:
                st.video(media)
            else:
                st.image(media, use_container_width=True)


def ratings_tab(vendor: sqlite3.Row | None) -> None:
    st.subheader("Ratings")
    if not vendor:
        st.warning("Please log in to rate vendors.")
        return
    target_phone = st.text_input("Vendor phone to rate")
    score = st.slider("Rating", 1, 5, 5)
    comment = st.text_area("Comment")
    if st.button("Submit rating"):
        cleaned = clean_phone_for_uganda(target_phone)
        target = conn.execute("SELECT id FROM vendors WHERE phone=?", (cleaned,)).fetchone()
        if not target:
            st.error("Vendor not found.")
            return
        with conn:
            conn.execute(
                "INSERT INTO ratings (id,vendor_id,rating,comment,created_at) VALUES (?,?,?,?,?)",
                (str(uuid.uuid4()), target["id"], int(score), comment.strip(), now_iso()),
            )
        st.success("Rating submitted.")

    rep = conn.execute(
        """
        SELECT v.name, v.phone, ROUND(AVG(r.rating), 2) AS avg_rating, COUNT(r.id) AS review_count
        FROM ratings r
        JOIN vendors v ON v.id = r.vendor_id
        GROUP BY r.vendor_id
        ORDER BY avg_rating DESC, review_count DESC
        """
    ).fetchall()
    if rep:
        st.dataframe(pd.DataFrame([dict(x) for x in rep]), use_container_width=True)


def admin_panel_tab() -> None:
    st.subheader("Admin Panel")
    if not st.session_state.is_admin:
        st.warning("Admin access required.")
        pwd = st.text_input("Admin password", type="password")
        if st.button("Unlock Admin"):
            if verify_admin_password(pwd):
                st.session_state.is_admin = True
                st.success("Admin unlocked.")
                st.rerun()
            else:
                st.error("Invalid admin password.")
        return

    listings = conn.execute(
        """
        SELECT l.id,
               l.title,
               l.category,
               l.item_condition,
               l.description,
               l.price,
               l.location,
               l.featured,
               l.is_active,
               l.expires_at,
               v.name AS vendor_name
        FROM listings l
        JOIN vendors v ON v.id = l.vendor_id
        ORDER BY l.created_at DESC
        """
    ).fetchall()

    if not listings:
        st.info("No listings in the database yet.")
        return

    st.markdown("### Moderate / Configure Listings")
    listing_ids = [r["id"] for r in listings]
    selected_id = st.selectbox("Pick a listing", listing_ids)
    selected = next((r for r in listings if r["id"] == selected_id), None)

    if selected is None:
        st.error("Listing not found.")
        return

    st.write(
        f"**{selected['title']}** by {selected['vendor_name']} · "
        f"Category: {selected['category']} · Price: UGX {int(selected['price']):,} · "
        f"Status: {'Active' if selected['is_active'] == 1 else 'Hidden'}"
    )

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("Hide listing", key="hide_listing_btn"):
            with conn:
                conn.execute("UPDATE listings SET is_active=0 WHERE id=?", (selected_id,))
            st.success("Listing hidden.")
            st.rerun()
    with col_b:
        if st.button("Show listing", key="show_listing_btn"):
            with conn:
                conn.execute("UPDATE listings SET is_active=1 WHERE id=?", (selected_id,))
            st.success("Listing shown.")
            st.rerun()

    with col_c:
        if st.button("Delete listing permanently", key="delete_listing_btn"):
            with conn:
                conn.execute("DELETE FROM listings WHERE id=?", (selected_id,))
            st.success("Listing deleted permanently.")
            st.rerun()

    with st.expander("Edit listing details", expanded=False):
        cat_options = ["Electronics", "Fashion", "Salon", "Vehicles", "Property", "Home", "Services", "Other"]
        # Include any additional categories found in DB.
        db_cats = sorted({r["category"] for r in listings if r["category"]})
        for c in db_cats:
            if c not in cat_options:
                cat_options.append(c)

        condition_options = ["Brand New", "Like New", "Used", "Refurbished"]
        with st.form("edit_listing_form"):
            new_title = st.text_input("Title", value=selected["title"])
            new_category = st.selectbox("Category", cat_options, index=cat_options.index(selected["category"]) if selected["category"] in cat_options else 0)
            new_condition = st.selectbox("Condition", condition_options, index=condition_options.index(selected["item_condition"]) if selected["item_condition"] in condition_options else 0)
            new_description = st.text_area("Description", value=selected["description"] or "")
            new_price = st.number_input("Price (UGX)", min_value=0.0, step=1000.0, value=float(selected["price"]))
            new_location = st.text_input("Location", value=selected["location"])
            new_featured = st.checkbox("Featured", value=selected["featured"] == 1)
            new_visibility = st.checkbox("Visible to buyers", value=selected["is_active"] == 1)

            if st.form_submit_button("Save changes"):
                with conn:
                    conn.execute(
                        """
                        UPDATE listings
                        SET title=?,
                            category=?,
                            item_condition=?,
                            description=?,
                            price=?,
                            location=?,
                            featured=?,
                            is_active=?
                        WHERE id=?
                        """,
                        (
                            new_title.strip(),
                            new_category,
                            new_condition,
                            new_description.strip(),
                            float(new_price),
                            new_location.strip(),
                            1 if new_featured else 0,
                            1 if new_visibility else 0,
                            selected_id,
                        ),
                    )
                st.success("Listing updated.")
                st.rerun()

    c1 = conn.execute("SELECT COUNT(*) AS c FROM vendors").fetchone()["c"]
    c2 = conn.execute("SELECT COUNT(*) AS c FROM listings").fetchone()["c"]
    c3 = conn.execute("SELECT COUNT(*) AS c FROM banner_ads").fetchone()["c"]
    c4 = conn.execute("SELECT COUNT(*) AS c FROM ratings").fetchone()["c"]
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Vendors", c1)
    m2.metric("Listings", c2)
    m3.metric("Banners", c3)
    m4.metric("Ratings", c4)

    if st.button("Lock Admin"):
        st.session_state.is_admin = False
        st.success("Admin locked.")
        st.rerun()


init_db()
ensure_listings_visibility_column()
ensure_session()
cleanup_expired()
seed_prelistings()
active_vendor = get_vendor(st.session_state.vendor_id)

st.markdown(
    """
<div class="hero">
    <h1>🏪 Biliwaka MarketPlace</h1>
    <p>Buy. Sell. Promote. Connect fast with verified WhatsApp contact links.</p>
</div>
""",
    unsafe_allow_html=True,
)

render_help_box()

if st.sidebar.button("❓ Help"):
    st.session_state.show_help = True
    st.rerun()

st.sidebar.markdown("### Navigation")
pages = ["Marketplace", "Auth", "Create Listing", "Banner Ad", "Ratings", "Settings", "Admin Panel"]
default_page = "Marketplace" if active_vendor else "Auth"
page = st.sidebar.radio("Go to", pages, index=pages.index(default_page))

if active_vendor:
    st.sidebar.success(f"Logged in: {active_vendor['name']}")
    st.sidebar.caption(f"Default contact: {active_vendor['whatsapp_phone']}")
else:
    st.sidebar.info("Not logged in")

if page == "Marketplace":
    marketplace_tab(active_vendor)
elif page == "Auth":
    auth_tab()
elif page == "Create Listing":
    create_listing_tab(active_vendor)
elif page == "Banner Ad":
    create_banner_tab(active_vendor)
elif page == "Ratings":
    ratings_tab(active_vendor)
elif page == "Settings":
    settings_tab(active_vendor)
elif page == "Admin Panel":
    admin_panel_tab()

st.markdown("---")
st.markdown('<div class="footer">© 2026 Biliwaka MarketPlace</div>', unsafe_allow_html=True)
