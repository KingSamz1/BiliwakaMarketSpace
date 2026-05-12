import streamlit as st
from pathlib import Path

from database import get_connection, init_db
from utils import apply_theme, init_session_defaults, render_footer, render_topbar, render_carousel

st.set_page_config(page_title="Biliwaka MarketSpace", page_icon="🛒", layout="wide")
init_session_defaults()
init_db()
if "user" not in st.session_state or st.session_state.user is None:
    params = st.query_params
    if "id" in params and "role" in params:
        st.session_state.user = {"id": int(params["id"]), "role": params["role"]}
        st.session_state.role = params["role"]

apply_theme()
render_topbar()

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("### 📋 Menu")
    if st.button("🏠 Home", use_container_width=True, key="m_home"): st.switch_page("Home.py")
    if st.button("📦 Listings", use_container_width=True, key="m_list"): st.switch_page("pages/1_🏪_MarketSpace.py")
    if st.button("📊 Dashboard", use_container_width=True, key="m_dash"): st.switch_page("pages/2_📊_Dashboard.py")
    if st.button("🚀 Advertising", use_container_width=True, key="m_adv"): st.switch_page("pages/3_📢_Advertising.py")
    if st.button("💳 Payment", use_container_width=True, key="m_pay"): st.switch_page("pages/4_💳_Pay.py")
    if st.button("🛒 Buy Banner", use_container_width=True, key="m_banner"): st.switch_page("pages/6_🛒_Buy_Banner.py")
    if st.session_state.get("role") == "admin":
        if st.button("🛠️ Admin Panel", use_container_width=True, key="m_admin"): st.switch_page("pages/7_🛠️_Admin.py")
        if st.button("👤 Profile", use_container_width=True, key="m_prof"): st.switch_page("pages/6_👤_Account.py")
    if st.button("🔐 Login", use_container_width=True, key="m_login"): st.switch_page("pages/5_🔐_Login.py")
    if not st.session_state.get("user"):
        if st.button("📝 Register", use_container_width=True, key="m_reg"): st.switch_page("pages/4_📝_Register.py")

    st.markdown("---")
    st.markdown('''
    <div style="border-left:3px solid #25D366;padding-left:12px;">
        <b>Become a Vendor</b><br>
        Post products and services for free.<br><br>
        <span style="background:#25D366;color:#fff;padding:2px 8px;border-radius:10px;font-size:0.75rem;font-weight:700;">4 FREE ADS / 7 DAYS</span>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown("<div style='margin:0.5rem;'></div>", unsafe_allow_html=True)
    st.markdown('''
    <div style="border-left:3px solid #3b82f6;padding-left:12px;">
        <b>Follow Us</b><br>
        <span style="opacity:0.8;">WhatsApp • Facebook</span><br>
        <span style="opacity:0.8;">Instagram • TikTok</span>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("---")
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

# ── MAIN CONTENT ──
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

st.markdown("""
<div style="text-align: center; margin: 1rem 0;">
    <button onclick="if(navigator.share){navigator.share({title:'Biliwaka MarketSpace',text:'Check out this amazing Ugandan marketplace!',url:window.location.href})}else{prompt('Copy this link:',window.location.href)}" 
            style="background: linear-gradient(135deg, #25D366, #128C7E); color: white; border: none; padding: 10px 25px; border-radius: 30px; font-weight: 700; cursor: pointer; box-shadow: 0 4px 15px rgba(37,211,102,0.3);">📤 Share Biliwaka</button>
</div>
""", unsafe_allow_html=True)

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
        <div style="background:linear-gradient(135deg, {color}15, {color}08);border:1px solid {color}30;border-radius:10px;padding:12px 16px;">
            <span style="font-size:1.3rem;">{icon}</span>
            <span style="color:#e5e7eb;font-weight:600;margin-left:8px;font-size:0.9rem;">{item}</span>
        </div>
        ''', unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)
st.markdown('<p style="font-size:1.1rem;font-weight:700;color:#e5e7eb;margin-bottom:0.8rem;">⭐ Featured Listings</p>', unsafe_allow_html=True)

db_items = []
with get_connection() as conn:
    featured = conn.execute("SELECT a.*, u.full_name FROM ads a JOIN users u ON u.id = a.user_id WHERE a.is_active = 1 AND a.is_featured = 1 ORDER BY a.clicks DESC LIMIT 4").fetchall()
    for row in featured:
        imgs = [m.strip() for m in row['media'].split(',') if m.strip()] if row['media'] else []
        valid = [img for img in imgs if img.startswith('http') and 'watch?v=' not in img]
        db_items.append((row['title'], f"UGX {row['price']:,.0f}", row['full_name'], valid[0] if valid else "", row['category'], row['discount']))

if not db_items:
    db_items = [
        ("HP Laptop 8GB RAM", "UGX 750,000", "Sejuku, Wakiso", "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80", "Electronics", 0),
        ("Modern 3 Bedroom House", "UGX 1,200,000 / Month", "Katale, Wakiso", "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=900&q=80", "Property", 0),
        ("Toyota Premio 2016", "UGX 38,000,000", "Nalumunye, Wakiso", "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?auto=format&fit=crop&w=900&q=80", "Vehicles", 0),
        ("Solar Panel 250W", "UGX 350,000", "Katale, Wakiso", "https://images.unsplash.com/photo-1509391366360-2e959784a276?auto=format&fit=crop&w=900&q=80", "Electronics", 0),
    ]

cards = st.columns(2)
for i in range(0, len(db_items), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(db_items):
            title, price, location, image_url, category, discount = db_items[i + j]
            with cols[j]:
                with st.container(border=True):
                    if image_url:
                        st.image(image_url, use_container_width=True)
                    else:
                        st.markdown("🖼️ *No image available*")
                    discount_tag = f"  ~~-{discount}%~~" if discount and discount > 0 else ""
                    st.markdown(f"<span style='background:#f59e0b20;color:#f59e0b;padding:2px 8px;border-radius:6px;font-size:0.7rem;font-weight:700;'>⭐ FEATURED</span> <span style='color:#6b7280;font-size:0.75rem;'>📁 {category}</span>{discount_tag}", unsafe_allow_html=True)
                    st.markdown(f"**{title}**")
                    st.markdown(f"<span style='color:#fbbf24;font-weight:800;font-size:1.15rem;'>{price}</span>", unsafe_allow_html=True)
                    st.caption(f"📍 {location}")
        else:
            with cols[j]:
                st.empty()

st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

info_left, info_right = st.columns(2)

with info_left:
    st.markdown('<p style="font-size:1.1rem;font-weight:700;color:#e5e7eb;margin-bottom:0.8rem;">❤️ Why Biliwaka?</p>', unsafe_allow_html=True)
    st.markdown('''
    <div style="background:linear-gradient(135deg,#3b82f615,#6366f110);border:1px solid #3b82f630;border-radius:12px;padding:16px;">
        <div style="color:#9ca3af;font-size:0.88rem;line-height:2.2;">
            ✅ 100% free to list<br>
            ✅ Connect directly with buyers<br>
            ✅ Trusted local vendors<br>
            ✅ WhatsApp integration<br>
            ✅ Wide coverage across Uganda
        </div>
    </div>
    ''', unsafe_allow_html=True)

with info_right:
    st.markdown('<p style="font-size:1.1rem;font-weight:700;color:#e5e7eb;margin-bottom:0.8rem;">🚀 How It Works</p>', unsafe_allow_html=True)
    steps = [
        ("1", "👤", "Create Account"),
        ("2", "📸", "Post Your Ad"),
        ("3", "💬", "Get Customers"),
        ("4", "📈", "Grow Business"),
    ]
    step_cols = st.columns(4)
    for col, (num, icon, title) in zip(step_cols, steps):
        with col:
            st.markdown(f'''
            <div style="text-align:center;padding:10px 4px;">
                <div style="font-size:1.5rem;margin-bottom:6px;">{icon}</div>
                <div style="color:#6b7280;font-size:0.65rem;font-weight:800;letter-spacing:1px;margin-bottom:2px;">STEP {num}</div>
                <div style="color:#e5e7eb;font-weight:700;font-size:0.78rem;">{title}</div>
            </div>
            ''', unsafe_allow_html=True)

render_footer()
