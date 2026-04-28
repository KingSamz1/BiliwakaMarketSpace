import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime

# ----------------------
# CONFIG
# ----------------------
st.set_page_config(page_title="Biliwaka MarketSpace", page_icon="🏪", layout="wide")

# ----------------------
# INIT STATE
# ----------------------
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Business Name": [
            "Elijah Shoe World",
            "Sarahs Touch Salon",
            "Kampala Tech Hub",
            "Mama Oyo Kitchen",
            "Pearl Motors Uganda",
            "Golden Real Estate",
            "Afro Glow Skincare",
            "Digital Solutions Ltd"
        ],
        "Category": [
            "Fashion", "Beauty", "Electronics", "Food",
            "Car Dealership 🚗", "Real Estate 🏠", "Beauty", "Services"
        ],
        "Product": [
            "Men Leather Shoes",
            "Wigs & Braids",
            "Laptops & Accessories",
            "Local Ugandan Dishes",
            "Toyota Harrier 2019",
            "3 Bedroom House in Mukono",
            "Organic Face Creams",
            "Website Design & Hosting"
        ],
        "Price (UGX)": [
            120000, "300,000 - 1,500,000", "1,500,000 - 8,000,000",
            "15,000 - 35,000", "85,000,000", "180,000,000",
            "45,000 - 120,000", "500,000 - 5,000,000"
        ],
        "Contact": [
            "0752694452", "0775998783", "0700123456",
            "0789123456", "0771234567", "0759876543",
            "0703456789", "0778765432"
        ],
        "Location": [
            "Kampala", "Nalumunye", "Kampala", "Nakawa",
            "Ntinda", "Mukono", "Entebbe", "Kampala"
        ],
        "Description": [
            "Premium handmade leather shoes for men. Durable and stylish for all occasions.",
            "Professional wigs, braids, and hair treatment services. Walk in beautiful.",
            "New and refurbished laptops, printers, and IT accessories at best prices.",
            "Authentic Ugandan food — Luwombo, Pilao, Posho & Beans, Matooke.",
            "Imported Toyota Harrier in excellent condition. Full service history.",
            "Spacious 3 bedroom house with compound, parking, and water tank.",
            "100% organic skincare products made from local Ugandan ingredients.",
            "Professional website design, hosting, and digital marketing services."
        ],
        "Rating": [4.5, 4.8, 4.2, 4.9, 4.0, 4.3, 4.7, 4.6],
        "Views": [234, 567, 189, 891, 123, 345, 678, 456],
        "Featured": [False, True, False, True, False, False, True, False],
        "Created At": [
            "2025-01-15", "2025-01-20", "2025-02-01", "2025-01-10",
            "2025-02-10", "2025-02-15", "2025-01-25", "2025-02-05"
        ],
        "Status": [
            "Active", "Active", "Active", "Active",
            "Active", "Active", "Active", "Active"
        ]
    })

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

if "page" not in st.session_state:
    st.session_state.page = "home"

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

if "toasts" not in st.session_state:
    st.session_state.toasts = []

if "search_history" not in st.session_state:
    st.session_state.search_history = []

if "favorites" not in st.session_state:
    st.session_state.favorites = set()

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ----------------------
# TOAST SYSTEM
# ----------------------
def show_toast(message, toast_type="success"):
    toast_id = f"toast_{int(time.time()*1000)}"
    colors = {
        "success": "#25D366",
        "error": "#ff4b4b",
        "info": "#ffd700",
        "warning": "#ff9800"
    }
    icons = {
        "success": "✅",
        "error": "❌",
        "info": "💡",
        "warning": "⚠️"
    }
    color = colors.get(toast_type, "#25D366")
    icon = icons.get(toast_type, "✅")
    st.session_state.toasts.append({
        "id": toast_id,
        "message": message,
        "color": color,
        "icon": icon,
        "time": time.time()
    })

def render_toasts():
    current = time.time()
    st.session_state.toasts = [t for t in st.session_state.toasts if current - t["time"] < 3]
    for toast in st.session_state.toasts:
        st.markdown(f"""
        <div id="{toast['id']}" style="
            position:fixed;top:20px;right:20px;z-index:9999;
            background:{toast['color']};color:#fff;
            padding:14px 24px;border-radius:12px;
            font-weight:600;font-size:0.95rem;
            box-shadow:0 8px 30px rgba(0,0,0,0.4);
            animation:slideIn 0.4s ease,fadeOut 0.4s ease 2.6s;
        ">
            {toast['icon']} {toast['message']}
        </div>
        """, unsafe_allow_html=True)

# ----------------------
# CATEGORY ICONS & COLORS
# ----------------------
CATEGORY_ICONS = {
    "Fashion": "👟",
    "Beauty": "💅",
    "Electronics": "💻",
    "Services": "🛠️",
    "Food": "🍲",
    "Car Dealership 🚗": "🚗",
    "Real Estate 🏠": "🏠"
}

CATEGORY_COLORS = {
    "Fashion": "#e74c3c",
    "Beauty": "#e91e90",
    "Electronics": "#3498db",
    "Services": "#9b59b6",
    "Food": "#f39c12",
    "Car Dealership 🚗": "#2ecc71",
    "Real Estate 🏠": "#1abc9c"
}

# ----------------------
# STYLING
# ----------------------
bg_gradient = "linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

@keyframes slideIn {{
    from {{ transform: translateX(100%); opacity: 0; }}
    to {{ transform: translateX(0); opacity: 1; }}
}}
@keyframes fadeOut {{
    from {{ opacity: 1; }}
    to {{ opacity: 0; }}
}}
@keyframes fadeInUp {{
    from {{ transform: translateY(30px); opacity: 0; }}
    to {{ transform: translateY(0); opacity: 1; }}
}}
@keyframes pulse {{
    0%, 100% {{ transform: scale(1); }}
    50% {{ transform: scale(1.05); }}
}}
@keyframes shimmer {{
    0% {{ background-position: -200% center; }}
    100% {{ background-position: 200% center; }}
}}
@keyframes float {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-8px); }}
}}

[data-testid="stApp"] {{
    background: {bg_gradient};
    color: #f4f4f4;
    font-family: 'Inter', sans-serif;
}}

[data-testid="stSidebar"] {{
    background: #111122 !important;
    border-right: 1px solid #2a2a4a !important;
}}

[data-testid="stSidebar"] * {{
    color: #c4c4e4 !important;
}}

h1, h2, h3, h4, h5, h6, p, span, label {{
    color: #e4e4f4 !important;
    font-family: 'Inter', sans-serif;
}}

.main-title {{
    text-align: center;
    background: linear-gradient(90deg, #ffd700, #ff8c00, #ffd700);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3rem;
    font-weight: 900;
    letter-spacing: -1px;
    animation: shimmer 3s linear infinite;
    text-shadow: none;
}}

.sub-title {{
    text-align: center;
    color: #8888aa !important;
    margin-bottom: 8px;
    font-size: 1.05rem;
    font-weight: 400;
}}

.biz-card {{
    background: linear-gradient(145deg, #1a1a2e, #16162a);
    padding: 22px;
    border-radius: 18px;
    margin-bottom: 16px;
    border: 1px solid #2a2a4a;
    transition: all 0.3s ease;
    animation: fadeInUp 0.5s ease;
    position: relative;
    overflow: hidden;
}}
.biz-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    border-radius: 18px 0 0 18px;
}}
.biz-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
    border-color: #3a3a5a;
}}

.biz-card.featured {{
    border-color: #ffd700;
    background: linear-gradient(145deg, #1f1f0a, #1a1a2e);
}}
.biz-card.featured::before {{
    background: linear-gradient(180deg, #ffd700, #ff8c00);
}}

.price-tag {{
    color: #ffd700 !important;
    font-weight: 800;
    font-size: 1.3rem;
}}

.meta-text {{
    color: #7777aa !important;
    font-size: 0.88rem;
}}

.desc-text {{
    color: #9999bb !important;
    font-size: 0.92rem;
    line-height: 1.5;
    margin: 8px 0;
}}

.wa-btn {{
    padding: 10px 20px;
    background: linear-gradient(135deg, #25D366, #128C7E);
    color: white !important;
    border-radius: 10px;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.2s ease;
    border: none;
    cursor: pointer;
}}
.wa-btn:hover {{
    transform: scale(1.05);
    box-shadow: 0 4px 20px rgba(37,211,102,0.4);
}}

.call-btn {{
    padding: 10px 20px;
    background: linear-gradient(135deg, #4285f4, #1a73e8);
    color: white !important;
    border-radius: 10px;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.2s ease;
    cursor: pointer;
}}
.call-btn:hover {{
    transform: scale(1.05);
    box-shadow: 0 4px 20px rgba(66,133,244,0.4);
}}

.fav-btn {{
    padding: 10px 14px;
    background: linear-gradient(135deg, #e74c3c, #c0392b);
    color: white !important;
    border-radius: 10px;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.2s ease;
    cursor: pointer;
}}
.fav-btn:hover {{
    transform: scale(1.05);
}}
.fav-btn.active {{
    background: linear-gradient(135deg, #ff6b6b, #ee5a24);
}}

.delete-btn {{
    padding: 10px 14px;
    background: linear-gradient(135deg, #ff4757, #ff3344);
    color: white !important;
    border-radius: 10px;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.2s ease;
    cursor: pointer;
}}

.edit-btn {{
    padding: 10px 14px;
    background: linear-gradient(135deg, #f39c12, #e67e22);
    color: white !important;
    border-radius: 10px;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.2s ease;
    cursor: pointer;
}}

.stat-card {{
    background: linear-gradient(145deg, #1a1a2e, #16162a);
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #2a2a4a;
    text-align: center;
    transition: all 0.3s ease;
}}
.stat-card:hover {{
    transform: translateY(-3px);
    border-color: #3a3a5a;
}}
.stat-number {{
    font-size: 2.2rem;
    font-weight: 900;
    color: #ffd700 !important;
    line-height: 1.2;
}}
.stat-label {{
    color: #7777aa !important;
    font-size: 0.85rem;
    font-weight: 500;
    margin-top: 4px;
}}

.category-pill {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 18px;
    border-radius: 25px;
    font-size: 0.88rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 1px solid #2a2a4a;
    background: #1a1a2e;
    color: #c4c4e4 !important;
}}
.category-pill:hover {{
    transform: scale(1.05);
}}
.category-pill.active {{
    border-color: #ffd700;
    background: linear-gradient(135deg, #2a2a0a, #1a1a2e);
    color: #ffd700 !important;
}}

.rating-stars {{
    color: #ffd700 !important;
    font-size: 0.95rem;
    letter-spacing: 2px;
}}

.featured-badge {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 12px;
    border-radius: 20px;
    background: linear-gradient(135deg, #ffd700, #ff8c00);
    color: #000 !important;
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.status-badge {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}}
.status-badge.active {{
    background: rgba(37,211,102,0.15);
    color: #25D366 !important;
}}
.status-badge.paused {{
    background: rgba(255,152,0,0.15);
    color: #ff9800 !important;
}}

.nav-link {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 18px;
    border-radius: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    color: #9999bb !important;
    text-decoration: none;
    margin-bottom: 4px;
}}
.nav-link:hover {{
    background: #1a1a3a;
    color: #ffd700 !important;
}}
.nav-link.active {{
    background: linear-gradient(135deg, #2a2a0a, #1a1a2e);
    color: #ffd700 !important;
    border: 1px solid #3a3a0a;
}}

.section-title {{
    font-size: 1.4rem;
    font-weight: 800;
    color: #e4e4f4 !important;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}}

.empty-state {{
    text-align: center;
    padding: 60px 20px;
    color: #6666aa !important;
}}
.empty-state-icon {{
    font-size: 4rem;
    margin-bottom: 16px;
    animation: float 3s ease-in-out infinite;
}}

.search-container {{
    position: relative;
}}
.search-container input {{
    background: #1a1a2e !important;
    border: 1px solid #2a2a4a !important;
    border-radius: 12px !important;
    padding: 14px 20px 14px 50px !important;
    color: #f4f4f4 !important;
    font-size: 1rem !important;
    transition: all 0.3s ease;
}}
.search-container input:focus {{
    border-color: #ffd700 !important;
    box-shadow: 0 0 20px rgba(255,215,0,0.1) !important;
}}

.divider {{
    height: 1px;
    background: linear-gradient(90deg, transparent, #2a2a4a, transparent);
    margin: 24px 0;
}}

.footer {{
    text-align: center;
    padding: 30px;
    color: #5555aa !important;
    font-size: 0.85rem;
}}
.footer a {{
    color: #ffd700 !important;
    text-decoration: none;
}}

.sort-select {{
    background: #1a1a2e !important;
    border: 1px solid #2a2a4a !important;
    border-radius: 10px !important;
    color: #f4f4f4 !important;
    padding: 8px 14px !important;
}}

/* Hide default Streamlit elements */
[data-testid="stSidebarCollapseButton"] {{
    color: #ffd700 !important;
}}
button[data-testid="stBaseButton-secondary"] {{
    background: linear-gradient(135deg, #ffd700, #ff8c00) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 12px 24px !important;
    transition: all 0.2s ease !important;
}}
button[data-testid="stBaseButton-secondary"]:hover {{
    transform: scale(1.03);
    box-shadow: 0 4px 20px rgba(255,215,0,0.3) !important;
}}
</style>
""", unsafe_allow_html=True)

# ----------------------
# HELPER FUNCTIONS
# ----------------------
def format_phone(phone):
    phone = str(phone).strip()
    if phone.startswith("0"):
        phone = "256" + phone[1:]
    elif not phone.startswith("256"):
        phone = "256" + phone
    return phone

def render_stars(rating):
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + ("½" if half else "") + "☆" * empty

def get_category_counts():
    if st.session_state.df.empty:
        return {}
    return st.session_state.df["Category"].value_counts().to_dict()

# ----------------------
# SIDEBAR NAV
# ----------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:20px 0 10px;">
        <div style="font-size:2.2rem;">🏪</div>
        <div style="font-weight:800;font-size:1.1rem;color:#ffd700 !important;">Biliwaka</div>
        <div style="font-size:0.75rem;color:#6666aa !important;">MarketSpace v2.0</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    nav_items = [
        ("🏠", "Home", "home"),
        ("➕", "Create Listing", "create"),
        ("⭐", "Favorites", "favorites"),
        ("📊", "Analytics", "analytics"),
        ("⚙️", "Admin Panel", "admin"),
    ]

    for icon, label, page in nav_items:
        is_active = st.session_state.page == page
        cls = "nav-link active" if is_active else "nav-link"
        st.markdown(f"""
        <div class="{cls}" onclick="document.querySelector('[data-testid=\"stSidebarNav\"]')">
            {icon} {label}
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"{icon} {label}", key=f"nav_{page}",
                      use_container_width=True,
                      on_click=lambda p=page: setattr(st.session_state, 'page', p)):
            pass

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Category filter in sidebar
    st.markdown("**📁 Categories**")
    counts = get_category_counts()
    all_cats = ["Fashion", "Beauty", "Electronics", "Services",
                "Food", "Car Dealership 🚗", "Real Estate 🏠"]

    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "All"

    cat_cols = st.columns(2)
    for i, cat in enumerate(["All"] + all_cats):
        with cat_cols[i % 2]:
            icon = CATEGORY_ICONS.get(cat, "📦")
            count = counts.get(cat, 0) if cat != "All" else len(st.session_state.df)
            is_active = st.session_state.selected_category == cat
            cls = "category-pill active" if is_active else "category-pill"
            color = CATEGORY_COLORS.get(cat, "#ffd700")
            border_c = color if is_active else "#2a2a4a"

            st.markdown(f"""
            <div class="{cls}" style="border-color:{border_c};width:100%;justify-content:center;"
                 onclick="window.parent.postMessage('{{\"category\":\"{cat}\"}}', '*')">
                {icon} {cat.split(' ')[0]} <span style="opacity:0.6;font-size:0.75rem;">({count})</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"{icon} {cat.split(' ')[0]} ({count})", key=f"cat_{cat}",
                          use_container_width=True,
                          on_click=lambda c=cat: setattr(st.session_state, 'selected_category', c)):
                pass

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Quick stats
    st.markdown("**⚡ Quick Stats**")
    total = len(st.session_state.df)
    active = len(st.session_state.df[st.session_state.df["Status"] == "Active"]) if not st.session_state.df.empty else 0
    featured = len(st.session_state.df[st.session_state.df["Featured"] == True]) if not st.session_state.df.empty else 0
    total_views = st.session_state.df["Views"].sum() if not st.session_state.df.empty else 0

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
        <div style="background:#1a1a2e;padding:12px;border-radius:10px;text-align:center;border:1px solid #2a2a4a;">
            <div style="font-size:1.4rem;font-weight:900;color:#ffd700;">{total}</div>
            <div style="font-size:0.7rem;color:#7777aa;">Listings</div>
        </div>
        <div style="background:#1a1a2e;padding:12px;border-radius:10px;text-align:center;border:1px solid #2a2a4a;">
            <div style="font-size:1.4rem;font-weight:900;color:#25D366;">{active}</div>
            <div style="font-size:0.7rem;color:#7777aa;">Active</div>
        </div>
        <div style="background:#1a1a2e;padding:12px;border-radius:10px;text-align:center;border:1px solid #2a2a4a;">
            <div style="font-size:1.4rem;font-weight:900;color:#ff8c00;">{featured}</div>
            <div style="font-size:0.7rem;color:#7777aa;">Featured</div>
        </div>
        <div style="background:#1a1a2e;padding:12px;border-radius:10px;text-align:center;border:1px solid #2a2a4a;">
            <div style="font-size:1.4rem;font-weight:900;color:#4285f4;">{total_views:,}</div>
            <div style="font-size:0.7rem;color:#7777aa;">Views</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------
# RENDER TOASTS
# ----------------------
render_toasts()

# ----------------------
# MAIN CONTENT
# ----------------------
df = st.session_state.df

# ======================
# HOME PAGE
# ======================
if st.session_state.page == "home":

    # Header
    st.markdown('<div class="main-title">🏪 Biliwaka MarketSpace</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Discover • Connect • Trade — Uganda\'s Premier Marketplace</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Search & Sort Row
    col_search, col_sort, col_loc = st.columns([3, 1.2, 1.2])

    with col_search:
        search = st.text_input("🔍", placeholder="Search products, businesses, locations...",
                               label_visibility="collapsed")
        if search and search not in st.session_state.search_history:
            st.session_state.search_history.append(search)
            if len(st.session_state.search_history) > 10:
                st.session_state.search_history.pop(0)

    with col_sort:
        sort_option = st.selectbox("Sort by", [
            "Newest First", "Oldest First", "Price: Low → High",
            "Price: High → Low", "Most Viewed", "Highest Rated", "Name A-Z"
        ], label_visibility="collapsed")

    with col_loc:
        locations = ["All"] + sorted(df["Location"].unique().tolist()) if not df.empty else ["All"]
        location_filter = st.selectbox("Location", locations, label_visibility="collapsed")

    st.markdown("")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Filter
    filtered_df = df.copy()

    if search:
        filtered_df = filtered_df[
            filtered_df["Business Name"].str.contains(search, case=False, na=False) |
            filtered_df["Product"].str.contains(search, case=False, na=False) |
            filtered_df["Location"].str.contains(search, case=False, na=False) |
            filtered_df["Description"].str.contains(search, case=False, na=False)
        ]

    if st.session_state.selected_category != "All":
        filtered_df = filtered_df[filtered_df["Category"] == st.session_state.selected_category]

    if location_filter != "All":
        filtered_df = filtered_df[filtered_df["Location"] == location_filter]

    # Only show active listings to visitors
    filtered_df = filtered_df[filtered_df["Status"] == "Active"]

    # Sort
    if sort_option == "Newest First":
        filtered_df = filtered_df.sort_values("Created At", ascending=False)
    elif sort_option == "Oldest First":
        filtered_df = filtered_df.sort_values("Created At", ascending=True)
    elif sort_option == "Most Viewed":
        filtered_df = filtered_df.sort_values("Views", ascending=False)
    elif sort_option == "Highest Rated":
        filtered_df = filtered_df.sort_values("Rating", ascending=False)
    elif sort_option == "Name A-Z":
        filtered_df = filtered_df.sort_values("Product", ascending=True)

    # Featured section
    featured_df = filtered_df[filtered_df["Featured"] == True]
    if not featured_df.empty:
        st.markdown('<div class="section-title">⭐ Featured Listings</div>', unsafe_allow_html=True)
        feat_cols = st.columns(min(3, len(featured_df)))
        for i, (_, row) in enumerate(featured_df.head(3).iterrows()):
            with feat_cols[i]:
                phone = format_phone(row["Contact"])
                wa_link = f"https://wa.me/{phone}?text=Hello%20I%20am%20interested%20in%20{row['Product']}"
                call_link = f"tel:{phone}"
                is_fav = row.name in st.session_state.favorites
                fav_cls = "fav-btn active" if is_fav else "fav-btn"
                cat_color = CATEGORY_COLORS.get(row["Category"], "#ffd700")

                st.markdown(f"""
                <div class="biz-card featured" style="border-top:3px solid {cat_color};">
                    <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:8px;">
                        <span class="featured-badge">⭐ FEATURED</span>
                        <span class="rating-stars">{render_stars(row['Rating'])}</span>
                    </div>
                    <h3 style="margin:4px 0;">{row['Product']}</h3>
                    <p class="meta-text">🏢 {row['Business Name']} | 📍 {row['Location']}</p>
                    <p class="desc-text">{row['Description'][:80]}...</p>
                    <p class="price-tag">💰 {row['Price (UGX)']}</p>
                    <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;">
                        <a class="wa-btn" href="{wa_link}" target="_blank">💬 Chat</a>
                        <a class="call-btn" href="{call_link}">📞 Call</a>
                    </div>
                    <p class="meta-text" style="margin-top:8px;">👁 {row['Views']:,} views</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # All listings
    st.markdown(f'<div class="section-title">📢 All Listings ({len(filtered_df)})</div>', unsafe_allow_html=True)

    if filtered_df.empty:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">🔍</div>
            <h3>No listings found</h3>
            <p style="color:#6666aa !important;">Try a different search or category filter.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for idx, row in filtered_df.iterrows():
            phone = format_phone(row["Contact"])
            wa_link = f"https://wa.me/{phone}?text=Hello%20I%20am%20interested%20in%20{row['Product']}"
            call_link = f"tel:{phone}"
            is_fav = idx in st.session_state.favorites
            fav_cls = "fav-btn active" if is_fav else "fav-btn"
            fav_text = "❤️ Saved" if is_fav else "🤍 Save"
            cat_icon = CATEGORY_ICONS.get(row["Category"], "📦")
            cat_color = CATEGORY_COLORS.get(row["Category"], "#ffd700")
            featured_html = '<span class="featured-badge" style="margin-left:8px;">⭐ FEATURED</span>' if row["Featured"] else ""

            st.markdown(f"""
            <div class="biz-card" style="border-left:4px solid {cat_color};">
                <div style="display:flex;justify-content:space-between;align-items:start;flex-wrap:wrap;gap:8px;">
                    <div>
                        <h3 style="margin:0;display:flex;align-items:center;gap:8px;">
                            {row['Product']} {featured_html}
                        </h3>
                        <p class="meta-text" style="margin:4px 0 0;">
                            {cat_icon} {row['Category']} | 🏢 {row['Business Name']} | 📍 {row['Location']}
                        </p>
                    </div>
                    <div style="text-align:right;">
                        <div class="rating-stars">{render_stars(row['Rating'])}</div>
                        <span class="meta-text">{row['Rating']}/5</span>
                    </div>
                </div>
                <p class="desc-text">{row['Description']}</p>
                <p class="price-tag" style="margin:8px 0;">💰 {row['Price (UGX)']}</p>
                <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;">
                    <a class="wa-btn" href="{wa_link}" target="_blank">💬 WhatsApp</a>
                    <a class="call-btn" href="{call_link}">📞 Call</a>
                    <button class="{fav_cls}" onclick="
                        fetch('/_stcore/save_favorite', {{
                            method:'POST',
                            body: JSON.stringify({{index: {idx}}})
                        }});
                    ">{fav_text}</button>
                </div>
                <div style="display:flex;justify-content:space-between;margin-top:10px;">
                    <p class="meta-text">👁 {row['Views']:,} views</p>
                    <p class="meta-text">📅 {row['Created At']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Favorite button handler
            col_fav, col_spacer = st.columns([0.15, 0.85])
            with col_fav:
                if st.button(fav_text, key=f"fav_{idx}", use_container_width=True):
                    if idx in st.session_state.favorites:
                        st.session_state.favorites.remove(idx)
                        show_toast("Removed from favorites", "info")
                    else:
                        st.session_state.favorites.add(idx)
                        show_toast("Added to favorites! ❤️", "success")
                    st.rerun()

# ======================
# CREATE / EDIT PAGE
# ======================
elif st.session_state.page == "create":

    is_editing = st.session_state.edit_index is not None
    page_title = "✏️ Edit Listing" if is_editing else "➕ Create Listing"
    st.markdown(f'<div class="section-title">{page_title}</div>', unsafe_allow_html=True)

    if is_editing:
        edit_row = df.iloc[st.session_state.edit_index]

    with st.form("create_listing"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Business Name *",
                                  value=edit_row["Business Name"] if is_editing else "")
            category = st.selectbox("Category *", [
                "Fashion", "Beauty", "Electronics", "Services",
                "Food", "Car Dealership 🚗", "Real Estate 🏠"
            ], index=[
                "Fashion", "Beauty", "Electronics", "Services",
                "Food", "Car Dealership 🚗", "Real Estate 🏠"
            ].index(edit_row["Category"]) if is_editing else 0)
            product = st.text_input("Product / Service *",
                                     value=edit_row["Product"] if is_editing else "")
            price = st.text_input("Price (UGX) *",
                                   value=str(edit_row["Price (UGX)"]) if is_editing else "")

        with col2:
            contact = st.text_input("WhatsApp Number * (e.g. 077xxxxxxx)",
                                     value=edit_row["Contact"] if is_editing else "")
            location = st.text_input("Location *",
                                      value=edit_row["Location"] if is_editing else "")
            description = st.text_area("Description *",
                                        value=edit_row["Description"] if is_editing else "",
                                        height=120)
            rating = st.slider("Rating", 0.0, 5.0, step=0.1,
                                value=float(edit_row["Rating"]) if is_editing else 4.0)

        featured = st.checkbox("⭐ Feature this listing (Premium)",
                                value=bool(edit_row["Featured"]) if is_editing else False)

        col_submit, col_cancel = st.columns([1, 1])

        with col_submit:
            submit = st.form_submit_button("✅ Publish Listing" if not is_editing else "💾 Save Changes")

        with col_cancel:
            if is_editing:
                cancel = st.form_submit_button("❌ Cancel Edit")
                if cancel:
                    st.session_state.edit_index = None
                    st.rerun()

        if submit:
            if not all([name, product, price, contact, location, description]):
                show_toast("Please fill in all required fields!", "error")
            else:
                phone = format_phone(contact)
                new_row = pd.DataFrame([{
                    "Business Name": name,
                    "Category": category,
                    "Product": product,
                    "Price (UGX)": price,
                    "Contact": phone,
                    "Location": location,
                    "Description": description,
                    "Rating": rating,
                    "Views": edit_row["Views"] if is_editing else 0,
                    "Featured": featured,
                    "Created At": edit_row["Created At"] if is_editing else datetime.now().strftime("%Y-%m-%d"),
                    "Status": "Active"
                }])

                if is_editing:
                    st.session_state.df.iloc[st.session_state.edit_index] = new_row.iloc[0]
                    st.session_state.edit_index = None
                    show_toast("Listing updated successfully! ✏️", "success")
                else:
                    st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
                    show_toast("Listing published successfully! 🎉", "success")

                st.rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Tips
    st.markdown("""
    <div style="background:#1a1a2e;padding:20px;border-radius:14px;border:1px solid #2a2a4a;">
        <h4 style="color:#ffd700 !important;margin:0 0 10px;">💡 Tips for a Great Listing</h4>
        <ul style="color:#9999bb !important;line-height:2;padding-left:20px;margin:0;">
            <li>Use a clear, specific product name (e.g., "Nike Air Max 90" not "Shoes")</li>
            <li>Write a detailed description — include size, color, condition, etc.</li>
            <li>Set a fair price — compare with similar listings on the platform</li>
            <li>Use your active WhatsApp number for faster connections</li>
            <li>Be specific with your location — include landmark if possible</li>
            <li>Featured listings get 3x more views and appear at the top!</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ======================
# FAVORITES PAGE
# ======================
elif st.session_state.page == "favorites":
    st.markdown('<div class="section-title">⭐ My Favorites</div>', unsafe_allow_html=True)

    if not st.session_state.favorites:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">🤍</div>
            <h3>No favorites yet</h3>
            <p style="color:#6666aa !important;">Click the heart icon on any listing to save it here.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        fav_df = df[df.index.isin(st.session_state.favorites)]
        if fav_df.empty:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">💔</div>
                <h3>Some favorites were removed</h3>
                <p style="color:#6666aa !important;">These listings may no longer be available.</p>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.favorites = set()
        else:
            for idx, row in fav_df.iterrows():
                phone = format_phone(row["Contact"])
                wa_link = f"https://wa.me/{phone}?text=Hello%20I%20am%20interested%20in%20{row['Product']}"
                cat_color = CATEGORY_COLORS.get(row["Category"], "#ffd700")

                st.markdown(f"""
                <div class="biz-card" style="border-left:4px solid {cat_color};">
                    <h3>{row['Product']}</h3>
                    <p class="meta-text">🏢 {row['Business Name']} | 📍 {row['Location']}</p>
                    <p class="price-tag">💰 {row['Price (UGX)']}</p>
                    <div style="display:flex;gap:8px;margin-top:12px;">
                        <a class="wa-btn" href="{wa_link}" target="_blank">💬 WhatsApp</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col_remove = st.columns([0.15, 0.85])
                with col_remove[0]:
                    if st.button("💔 Remove", key=f"remove_fav_{idx}", use_container_width=True):
                        st.session_state.favorites.discard(idx)
                        show_toast("Removed from favorites", "info")
                        st.rerun()

# ======================
# ANALYTICS PAGE
# ======================
elif st.session_state.page == "analytics":
    st.markdown('<div class="section-title">📊 Analytics Dashboard</div>', unsafe_allow_html=True)

    if df.empty:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📊</div>
            <h3>No data yet</h3>
            <p style="color:#6666aa !important;">Create some listings to see analytics.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Top stats
        total_listings = len(df)
        total_views = df["Views"].sum()
        avg_rating = df["Rating"].mean()
        total_featured = len(df[df["Featured"] == True])
        categories_used = df["Category"].nunique()
        locations_used = df["Location"].nunique()

        stat_cols = st.columns(6)
        stats = [
            ("📋", total_listings, "Listings", "#ffd700"),
            ("👁", f"{total_views:,}", "Total Views", "#4285f4"),
            ("⭐", f"{avg_rating:.1f}", "Avg Rating", "#ff8c00"),
            ("🌟", total_featured, "Featured", "#e91e90"),
            ("📁", categories_used, "Categories", "#25D366"),
            ("📍", locations_used, "Locations", "#9b59b6"),
        ]

        for i, (icon, value, label, color) in enumerate(stats):
            with stat_cols[i]:
                st.markdown(f"""
                <div class="stat-card">
                    <div style="font-size:1.5rem;margin-bottom:4px;">{icon}</div>
                    <div class="stat-number" style="color:{color} !important;">{value}</div>
                    <div class="stat-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Category breakdown
        col_cat, col_top = st.columns(2)

        with col_cat:
            st.markdown("**📁 Category Breakdown**")
            counts = df["Category"].value_counts()
            for cat, count in counts.items():
                icon = CATEGORY_ICONS.get(cat, "📦")
                color = CATEGORY_COLORS.get(cat, "#ffd700")
                pct = (count / len(df)) * 100
                st.markdown(f"""
                <div style="margin-bottom:12px;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                        <span style="color:#c4c4e4 !important;font-size:0.9rem;">{icon} {cat}</span>
                        <span style="color:#7777aa !important;font-size:0.85rem;">{count} ({pct:.0f}%)</span>
                    </div>
                    <div style="background:#1a1a2e;border-radius:6px;height:8px;overflow:hidden;">
                        <div style="background:{color};width:{pct}%;height:100%;border-radius:6px;transition:width 0.5s ease;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with col_top:
            st.markdown("**🔥 Top Viewed Listings**")
            top_viewed = df.nlargest(5, "Views")
            for i, (_, row) in enumerate(top_viewed.iterrows()):
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;padding:10px;
                           background:#1a1a2e;border-radius:10px;margin-bottom:8px;
                           border:1px solid #2a2a4a;">
                    <div style="font-size:1.3rem;font-weight:900;color:#ffd700;width:28px;text-align:center;">
                        #{i+1}
                    </div>
                    <div style="flex:1;">
                        <div style="color:#e4e4f4 !important;font-weight:600;font-size:0.9rem;">{row['Product']}</div>
                        <div style="color:#7777aa !important;font-size:0.8rem;">{row['Business Name']}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="color:#4285f4 !important;font-weight:700;">{row['Views']:,}</div>
                        <div style="color:#5555aa !important;font-size:0.75rem;">views</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Location breakdown
        st.markdown("**📍 Location Breakdown**")
        loc_counts = df["Location"].value_counts()
        loc_cols = st.columns(min(4, len(loc_counts)))
        for i, (loc, count) in enumerate(loc_counts.items()):
            with loc_cols[i % 4]:
                st.markdown(f"""
                <div class="stat-card">
                    <div style="font-size:1.3rem;margin-bottom:4px;">📍</div>
                    <div class="stat-number">{count}</div>
                    <div class="stat-label">{loc}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Rating distribution
        st.markdown("**⭐ Rating Distribution**")
        rating_cols = st.columns(5)
        for i, r in enumerate([5, 4, 3, 2, 1]):
            count = len(df[(df["Rating"] >= r - 0.5) & (df["Rating"] < r + 0.5)]) if r < 5 else len(df[df["Rating"] >= 4.5])
            stars = "★" * r + "☆" * (5 - r)
            with rating_cols[i]:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="rating-stars" style="font-size:1.1rem;">{stars}</div>
                    <div class="stat-number" style="font-size:1.6rem;">{count}</div>
                    <div class="stat-label">{r} star{'s' if r > 1 else ''}</div>
                </div>
                """, unsafe_allow_html=True)

# ======================
# ADMIN PANEL
# ======================
elif st.session_state.page == "admin":

    # Admin login check
    if not st.session_state.admin_logged_in:
        st.markdown('<div class="section-title">⚙️ Admin Panel</div>', unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        with st.form("admin_login"):
            pwd = st.text_input("Admin Password", type="password")
            login_btn = st.form_submit_button("🔓 Login")

            if login_btn:
                if pwd == "biliwaka2025":
                    st.session_state.admin_logged_in = True
                    show_toast("Welcome, Admin! 🔓", "success")
                    st.rerun()
                else:
                    show_toast("Incorrect password!", "error")

        st.markdown("""
        <div style="background:#1a1a2e;padding:20px;border-radius:14px;border:1px solid #2a2a4a;margin-top:20px;">
            <p style="color:#7777aa !important;">🔒 Default password: <code style="color:#ffd700;">biliwaka2025</code></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="section-title">⚙️ Admin Panel</div>', unsafe_allow_html=True)

        if st.button("🔒 Logout", use_container_width=False):
            st.session_state.admin_logged_in = False
            show_toast("Logged out", "info")
            st.rerun()

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Admin tabs
        tab1, tab2, tab3 = st.tabs(["📋 Manage Listings", "⭐ Set Featured", "🔄 Bulk Actions"])

        with tab1:
            st.markdown(f"**Total: {len(df)} listings**")

            for idx, row in df.iterrows():
                status_cls = "status-badge active" if row["Status"] == "Active" else "status-badge paused"
                cat_color = CATEGORY_COLORS.get(row["Category"], "#ffd700")

                st.markdown(f"""
                <div class="biz-card" style="border-left:4px solid {cat_color};padding:16px;">
                    <div style="display:flex;justify-content:space-between;align-items:start;flex-wrap:wrap;gap:8px;">
                        <div>
                            <h4 style="margin:0;">{row['Product']}</h4>
                            <p class="meta-text">{row['Business Name']} | {row['Location']} | {row['Price (UGX)']}</p>
                        </div>
                        <span class="{status_cls}">● {row['Status']}</span>
                    </div>
                    <div style="display:flex;gap:6px;margin-top:10px;flex-wrap:wrap;">
                """, unsafe_allow_html=True)

                btn_cols = st.columns([1, 1, 1, 1, 1])
                with btn_cols[0]:
                    if st.button("✏️ Edit", key=f"admin_edit_{idx}", use_container_width=True):
                        st.session_state.edit_index = idx
                        st.session_state.page = "create"
                        st.rerun()
                with btn_cols[1]:
                    if st.button("🔄 Toggle", key=f"admin_toggle_{idx}", use_container_width=True):
                        new_status = "Paused" if row["Status"] == "Active" else "Active"
                        st.session_state.df.at[idx, "Status"] = new_status
                        show_toast(f"Listing {new_status.lower()}", "info")
                        st.rerun()
                with btn_cols[2]:
                    if st.button("👁 +100", key=f"admin_views_{idx}", use_container_width=True):
                        st.session_state.df.at[idx, "Views"] += 100
                        show_toast("+100 views added", "success")
                        st.rerun()
                with btn_cols[3]:
                    if st.button("⭐ Feature", key=f"admin_feat_{idx}", use_container_width=True):
                        st.session_state.df.at[idx, "Featured"] = not row["Featured"]
                        show_toast("Featured toggled!", "info")
                        st.rerun()
                with btn_cols[4]:
                    if st.button("🗑️ Delete", key=f"admin_del_{idx}", use_container_width=True):
                        st.session_state.df = st.session_state.df.drop(idx).reset_index(drop=True)
                        st.session_state.favorites.discard(idx)
                        show_toast("Listing deleted", "error")
                        st.rerun()

                st.markdown("</div></div>", unsafe_allow_html=True)

        with tab2:
            st.markdown("**Click to toggle featured status for each listing:**")
            if df.empty:
                st.info("No listings to feature.")
            else:
                for idx, row in df.iterrows():
                    is_feat = row["Featured"]
                    feat_label = "⭐ FEATURED" if is_feat else "☆ Not Featured"
                    feat_color = "#ffd700" if is_feat else "#5555aa"
                    st.markdown(f"""
                    <div style="display:flex;justify-content:space-between;align-items:center;
                               padding:12px 16px;background:#1a1a2e;border-radius:10px;
                               margin-bottom:6px;border:1px solid {'#ffd700' if is_feat else '#2a2a4a'};">
                        <div>
                            <span style="color:#e4e4f4 !important;font-weight:600;">{row['Product']}</span>
                            <span style="color:#7777aa !important;font-size:0.85rem;margin-left:8px;">— {row['Business Name']}</span>
                        </div>
                        <span style="color:{feat_color} !important;font-weight:700;font-size:0.85rem;">{feat_label}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Toggle" if not is_feat else "Unfeature",
                                  key=f"feat_toggle_{idx}", use_container_width=False):
                        st.session_state.df.at[idx, "Featured"] = not is_feat
                        show_toast("Featured status updated!", "info")
                        st.rerun()

        with tab3:
            st.markdown("**Bulk Actions**")

            col_b1, col_b2 = st.columns(2)

            with col_b1:
                if st.button("▶️ Activate All", use_container_width=True, type="primary"):
                    st.session_state.df["Status"] = "Active"
                    show_toast("All listings activated!", "success")
                    st.rerun()

                if st.button("⏸️ Pause All", use_container_width=True):
                    st.session_state.df["Status"] = "Paused"
                    show_toast("All listings paused", "warning")
                    st.rerun()

                if st.button("👁 Add 1000 views to all", use_container_width=True):
                    st.session_state.df["Views"] = st.session_state.df["Views"] + 1000
                    show_toast("+1000 views to all!", "success")
                    st.rerun()

            with col_b2:
                if st.button("⭐ Feature All", use_container_width=True):
                    st.session_state.df["Featured"] = True
                    show_toast("All listings featured!", "success")
                    st.rerun()

                if st.button("☆ Unfeature All", use_container_width=True):
                    st.session_state.df["Featured"] = False
                    show_toast("All unfeatured", "info")
                    st.rerun()

                if st.button("🗑️ Delete All Listings", use_container_width=True):
                    st.session_state.df = pd.DataFrame(columns=df.columns)
                    st.session_state.favorites = set()
                    show_toast("ALL LISTINGS DELETED!", "error")
                    st.rerun()

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            st.markdown("**📥 Export Data**")
            if st.button("Download as CSV", use_container_width=True):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Click to download",
                    data=csv,
                    file_name=f"biliwaka_marketplace_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

# ----------------------
# FOOTER
# ----------------------
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    <div style="font-size:1.5rem;margin-bottom:8px;">🏪</div>
    <div style="font-weight:700;color:#ffd700 !important;margin-bottom:4px;">Biliwaka MarketSpace</div>
    <div>Uganda's Premier Digital Marketplace</div>
    <div style="margin-top:12px;">
        <a href="#">About</a> • <a href="#">Terms</a> • <a href="#">Privacy</a> • <a href="#">Contact</a>
    </div>
    <div style="margin-top:8px;color:#4444aa !important;">© 2025 Biliwaka MarketSpace. All rights reserved.</div>
</div>
""", unsafe_allow_html=True)
