import streamlit as st
from pathlib import Path

from database import get_connection, init_db
from utils import apply_theme, init_session_defaults, render_footer, render_topbar, render_carousel

st.set_page_config(page_title="Biliwaka MarketSpace", page_icon="🛒", layout="wide")
init_session_defaults()
init_db()

# ── SESSION LOGIN FROM QUERY PARAMS ──
if "user" not in st.session_state or st.session_state.user is None:
    params = st.query_params
    if "id" in params and "role" in params:
        st.session_state.user = {"id": int(params["id"]), "role": params["role"]}
        st.session_state.role = params["role"]

# ── REGISTER ALL PAGES (Matches your exact files) ──
all_page_paths = [
    "Home.py",
    "pages/1_🏪_MarketSpace.py",
    "pages/2_📊_Dashboard.py",
    "pages/3_📢_Advertising.py",
    "pages/4_💳_Pay.py",
    "pages/5_💬_Messages.py",
    "pages/6_👤_Profile.py",
    "pages/7_🛠️_Admin.py",
    "pages/8_🛒_Buy_Banner.py",
]

valid_pages = []
for p in all_page_paths:
    if Path(p).exists():
        valid_pages.append(st.Page(p))

# Hide Admin page from non-admins using the correct .path attribute
is_admin = st.session_state.get("role") == "admin"
if not is_admin:
    valid_pages = [p for p in valid_pages if "Admin" not in p.path]

nav = st.navigation(valid_pages)

apply_theme()
render_topbar()

# ── LAYOUT ──
layout = st.columns([1.1, 3.5, 1.3], gap="large")
left_sidebar, center, right_sidebar = layout

with left_sidebar:
    st.markdown('<div class="block"><b>Quick Menu</b></div>', unsafe_allow_html=True)
    
    # Use st.link_button for sub-page navigation (st.switch_page crashes if used inside the main entry file)
    menu_items = [
        ("📦 Listings", "pages/1_🏪_MarketSpace.py"),
        ("📊 Dashboard", "pages/2_📊_Dashboard.py"),
        ("💬 Messages", "pages/5_💬_Messages.py"),
        ("🚀 Advertising", "pages/3_📢_Advertising.py"),
        ("💳 Payment", "pages/4_💳_Pay.py"),
    ]
    
    for label, page in menu_items:
        if Path(page).exists():
            st.link_button(label, f"/{page}", use_container_width=True)

    # Show Admin button ONLY if user is admin
    if is_admin and Path("pages/7_🛠️_Admin.py").exists():
        st.markdown("<div style='margin:0.5rem 0;'></div>", unsafe_allow_html=True)
        st.link_button("🛠️ Admin Panel", "/pages/7_🛠️_Admin.py", use_container_width=True, type="secondary")

    st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)
    st.markdown('''
    <div class="block" style="border-left:3px solid #25D366;padding-left:12px;">
        <b>Become a Vendor</b><br>
        Post products and services for free.<br><br>
        <span style="background:#25D366;color:#fff;padding:2px 8px;border-radius:10px;font-size:0.75rem;font-weight:700;">4 FREE ADS / 7 DAYS</span>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('''
    <div class="block" style="border-left:3px solid #3b82f6;padding-left:12px;">
        <b>Follow Us</b><br>
        <span style="opacity:0.8;">WhatsApp</span> • 
        <span style="opacity:0.8;">Facebook</span><br>
        <span style="opacity:0.8;">Instagram</span> • 
        <span style="opacity:0.8;">TikTok</span>
    </div>
    ''', unsafe_allow_html=True)

# ── CENTER CONTENT ──
with center:

    # --- Carousel ---
    carousel_media = []
    banner_path = Path(__file__).parent / "assets" / "banner.png"
    if banner_path.exists():
        carousel_media.append(str(banner_path))
    with get_connection() as conn:
        db_banners = conn.execute("SELECT media FROM banner_ads WHERE expires_at >= date('now') ORDER BY id DESC").fetchall()
        for b in db_banners:
            if b['media']:
                carousel_media.append(b['media'])
    if not carousel_media:
        carousel_media.append("https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=1200&q=80")
    render_carousel(carousel_media, auto_slide=True, interval=10000)

    # --- Share button ---
    st.markdown("""
    <div style="text-align: center; margin: 1rem 0;">
        <button onclick="if(navigator.share){navigator.share({title:'Biliwaka MarketSpace',text:'Check out this amazing Ugandan marketplace!',url:window.location.href})}else{prompt('Copy this link:',window.location.href)}" 
                style="background: linear-gradient(135deg, #25D366, #128C7E); color: white; border: none; padding: 10px 25px; border-radius: 30px; font-weight: 700; cursor: pointer; box-shadow: 0 4px 15px rgba(37,211,102,0.3);">📤 Share Biliwaka</button>
    </div>
    """, unsafe_allow_html=True)

    # --- Categories ---
    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown('<p style="font-size:1.1rem;font-weight:700;color:#e5e7eb;margin-bottom:0.8rem;">🏷️ Browse by Category</p>', unsafe_allow_html=True)
    categories = [
        ("💻", "Electronics", "#3b82f6"), ("👗", "Fashion", "#ec4899"), ("🛋️", "Home & Office", "#f59e0b"),
        ("🚗", "Vehicles", "#8b5cf6"), ("🏠", "Property", "#14b8a6"), ("📱", "Phones", "#06b6d4"),
        ("💄", "Beauty", "#f43f5e"), ("🌱", "Agriculture", "#22c55e"), ("🛠️", "Services", "#6366f1"),
    ]
    cat_cols = st.columns(3)
    for idx, (icon, item, color) in enumerate(categories):
        with cat_cols[idx % 3]:
            st.markdown(f'''
            <div style="background:linear-gradient(135deg, {color}15, {color}08);border:1px solid {color}30;border-radius:10px;padding:12px 16px;cursor:pointer;transition:all 0.2s;"
                 onmouseover="this.style.borderColor='{color}';this.style.transform='translateY(-2px)'"
                 onmouseout="this.style.borderColor='{color}30';this.style.transform='translateY(0)'">
                <span style="font-size:1.3rem;">{icon}</span>
                <span style="color:#e5e7eb;font-weight:600;margin-left:8px;font-size:0.9rem;">{item}</span>
            </div>
            ''', unsafe_allow_html=True)

    # --- Featured Listings ---
    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown('<p style="font-size:1.1rem;font-weight:700;color:#e5e7eb;margin-bottom:0.8rem;">⭐ Featured Listings</p>', unsafe_allow_html=True)

    db_items = []
    with get_connection() as conn:
        featured = conn.execute("SELECT a.*, u.full_name FROM ads a JOIN users u ON u.id = a.user_id WHERE a.is_active = 1 AND a.is_featured = 1 ORDER BY a.clicks DESC LIMIT 4").fetchall()
        for row in featured:
            imgs = [m.strip() for m in row['media'].split(',') if m.strip()] if row['media'] else []
            valid = [img for img in imgs if 'watch?v=' not in img and (img.startswith('http') or img.startswith('data:'))]
            db_items.append((row['title'], f"UGX {row['price']:,.0f}", row['full_name'], valid[0] if valid else "", row['category'], row['discount']))

    if not db_items:
        db_items = [
            ("HP Laptop 8GB RAM", "UGX 750,000", "Sejuku, Wakiso", "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80", "Electronics", 0),
            ("Modern 3 Bedroom House", "UGX 1,200,000 / Month", "Katale, Wakiso", "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=900&q=80", "Property", 0),
            ("Toyota Premio 2016", "UGX 38,000,000", "Nalumunye, Wakiso", "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?auto=format&fit=crop&w=900&q=80", "Vehicles", 0),
            ("Solar Panel 250W", "UGX 350,000", "Katale, Wakiso", "https://images.unsplash.com/photo-1509391366360-2e959784a276?auto=format&fit=crop&w=900&q=80", "Electronics", 0),
        ]

    cards = st.columns(2)
    for i, (title, price, location, image_url, category, discount) in enumerate(db_items):
        discount_html = ""
        if discount and discount > 0:
            discount_html = f'<div style="position:absolute;top:10px;right:10px;background:#ef4444;color:white;padding:3px 10px;border-radius:20px;font-size:0.7rem;font-weight:800;">-{discount}%</div>'
        with cards[i % 2]:
            st.markdown(f'''
            <div style="background:#111827;border-radius:12px;border:1px solid #1f2937;overflow:hidden;position:relative;transition:all 0.2s;cursor:pointer;"
                 onmouseover="this.style.borderColor='#374151';this.style.boxShadow='0 8px 25px rgba(0,0,0,0.4)'"
                 onmouseout="this.style.borderColor='#1f2937';this.style.boxShadow='none'">
                <div style="position:relative;">
                    {discount_html}
                    {"<img src='" + image_url + "' style='width:100%;height:200px;object-fit:cover;' onerror=\"this.style.display='none'\">" if image_url else '<div style="width:100%;height:200px;background:#1f2937;display:flex;align-items:center;justify-content:center;color:#4b5563;font-size:2rem;">🖼️</div>'}
                </div>
                <div style="padding:14px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <span style="background:#f59e0b20;color:#f59e0b;padding:2px 8px;border-radius:6px;font-size:0.7rem;font-weight:700;">⭐ FEATURED</span>
                        <span style="color:#6b7280;font-size:0.75rem;">📁 {category}</span>
                    </div>
                    <div style="font-weight:700;color:#e5e7eb;font-size:0.95rem;margin-bottom:6px;">{title}</div>
                    <div style="color:#fbbf24;font-weight:800;font-size:1.15rem;margin-bottom:4px;">{price}</div>
                    <div style="color:#6b7280;font-size:0.8rem;">📍 {location}</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)

    # --- How it works ---
    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown('<p style="font-size:1.1rem;font-weight:700;color:#e5e7eb;margin-bottom:1rem;">🚀 How It Works</p>', unsafe_allow_html=True)

    steps = [
        ("1", "👤", "Create Account", "Sign up for free in seconds", "#3b82f6"),
        ("2", "📸", "Post Your Ad", "Add photos and description", "#22c55e"),
        ("3", "💬", "Get Customers", "Receive calls and messages", "#f59e0b"),
        ("4", "📈", "Grow Business", "Expand and reach more people", "#8b5cf6"),
    ]
    flow = st.columns(4)
    for col, (num, icon, title, desc, color) in zip(flow, steps):
        with col:
            st.markdown(f'''
            <div style="text-align:center;padding:20px 10px;">
                <div style="width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,{color},{color}aa);display:flex;align-items:center;justify-content:center;margin:0 auto 12px;font-size:1.5rem;box-shadow:0 4px 15px {color}30;">{icon}</div>
                <div style="color:{color};font-size:0.7rem;font-weight:800;letter-spacing:1px;margin-bottom:4px;">STEP {num}</div>
                <div style="color:#e5e7eb;font-weight:700;font-size:0.9rem;margin-bottom:4px;">{title}</div>
                <div style="color:#6b7280;font-size:0.78rem;">{desc}</div>
            </div>
            ''', unsafe_allow_html=True)

# ── RIGHT SIDEBAR ──
with right_sidebar:
    st.markdown('''
    <div style="background:linear-gradient(135deg,#25D36615,#128C7E10);border:1px solid #25D36630;border-radius:12px;padding:16px;text-align:center;">
        <div style="font-size:1.8rem;margin-bottom:6px;">🆓</div>
        <div style="color:#e5e7eb;font-weight:700;font-size:0.95rem;margin-bottom:8px;">Post for Free</div>
        <div style="color:#9ca3af;font-size:0.78rem;line-height:1.6;">
            4 free ads every 7 days<br>
            Featured ads available<br>
            No hidden fees
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("<div style='margin:0.8rem 0;'></div>", unsafe_allow_html=True)

    st.markdown('''
    <div style="background:linear-gradient(135deg,#3b82f615,#6366f110);border:1px solid #3b82f630;border-radius:12px;padding:16px;">
        <div style="color:#e5e7eb;font-weight:700;font-size:0.95rem;margin-bottom:10px;">Why Biliwaka?</div>
        <div style="color:#9ca3af;font-size:0.82rem;line-height:2;">
            ✅ 100% free to list<br>
            ✅ Connect directly<br>
            ✅ Trusted vendors<br>
            ✅ WhatsApp integration<br>
            ✅ Wide coverage
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("<div style='margin:0.8rem 0;'></div>", unsafe_allow_html=True)

    with get_connection() as conn:
        total_users = conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()["n"]
        total_ads = conn.execute("SELECT COUNT(*) AS n FROM ads").fetchone()["n"]
    st.markdown(f'''
    <div style="background:#111827;border:1px solid #1f2937;border-radius:12px;padding:16px;">
        <div style="color:#e5e7eb;font-weight:700;font-size:0.95rem;margin-bottom:12px;">📊 Platform Stats</div>
        <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
            <span style="color:#9ca3af;font-size:0.82rem;">Vendors</span>
            <span style="color:#fbbf24;font-weight:800;font-size:0.95rem;">{total_users}</span>
        </div>
        <div style="height:4px;background:#1f2937;border-radius:2px;overflow:hidden;margin-bottom:14px;">
            <div style="height:100%;width:{min(total_users * 2, 100)}%;background:linear-gradient(90deg,#fbbf24,#f59e0b);border-radius:2px;"></div>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
            <span style="color:#9ca3af;font-size:0.82rem;">Listings</span>
            <span style="color:#25D366;font-weight:800;font-size:0.95rem;">{total_ads}</span>
        </div>
        <div style="height:4px;background:#1f2937;border-radius:2px;overflow:hidden;">
            <div style="height:100%;width:{min(total_ads * 2, 100)}%;background:linear-gradient(90deg,#25D366,#128C7E);border-radius:2px;"></div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

render_footer()
