import streamlit as st
from pathlib import Path

from database import get_connection, init_db
from utils import apply_theme, init_session_defaults, render_footer, render_theme_toggle, render_topbar, render_carousel

st.set_page_config(page_title="Biliwaka MarketSpace", page_icon="🛒", layout="wide")
init_session_defaults()
init_db()
render_theme_toggle()
apply_theme()
render_topbar()

layout = st.columns([1.1, 3.5, 1.3], gap="large")
left_sidebar, center, right_sidebar = layout

with left_sidebar:
    st.markdown('<div class="block"><b>Menu</b><br>Home<br>Listings<br>Categories<br>Featured ads<br>Top vendors<br>🚀 Advertising<br>💳 Payment<br>How it works</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="block"><b>Become a Vendor</b><br>Post products and services for free.<br><br><small>4 free ads every 7 days</small></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="block"><b>Follow Us</b><br>WhatsApp  •  Facebook  •  Instagram  •  TikTok</div>', unsafe_allow_html=True)

with center:
    # Carousel images - starting with local banner as default
    carousel_images = []
    
    # Add local banner as first image if it exists
    banner_path = Path("/home/zion/banner.png")
    if banner_path.exists():
        carousel_images.append(str(banner_path))
    
    # Add sample carousel images - you can replace these with your actual images
    carousel_images.extend([
        "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=1200&q=80",  # Business meeting
        "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=1200&q=80",  # Shopping
        "https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=1200&q=80",  # Technology
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80",  # Market
    ])
    
    render_carousel(carousel_images, auto_slide=True, interval=4000)

    st.markdown("<div style='margin-top:-0.1rem;'></div>", unsafe_allow_html=True)
    st.subheader("Browse by category")
    categories = [
        ("💻", "Electronics"),
        ("👗", "Fashion"),
        ("🛋️", "Home & Office"),
        ("🚗", "Vehicles"),
        ("🏠", "Property"),
        ("📱", "Phones"),
        ("💄", "Beauty"),
        ("🌱", "Agriculture"),
        ("🛠️", "Services"),
    ]
    # Use fixed-width rows so category labels stay readable.
    cat_cols = st.columns(3)
    for idx, (icon, item) in enumerate(categories):
        with cat_cols[idx % 3]:
            st.markdown(
                f'<div class="category-chip"><span class="category-label">{icon} {item}</span></div>',
                unsafe_allow_html=True,
            )

    st.subheader("Featured listings")
    cards = st.columns(2)
    demo_items = [
        (
            "HP Laptop 8GB RAM",
            "UGX 750,000",
            "Sejuku, Wakiso",
            "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80",
        ),
        (
            "Modern 3 Bedroom House",
            "UGX 1,200,000 / Month",
            "Katale, Wakiso",
            "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=900&q=80",
        ),
        (
            "Toyota Premio 2016",
            "UGX 38,000,000",
            "Nalumunye, Wakiso",
            "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=900&q=80",
        ),
        (
            "Solar Panel 250W",
            "UGX 350,000",
            "Katale, Wakiso",
            "https://images.unsplash.com/photo-1509391366360-2e959784a276?auto=format&fit=crop&w=900&q=80",
        ),
    ]
    for i, (title, price, location, image_url) in enumerate(demo_items):
        with cards[i % 2]:
            st.markdown('<div class="listing-image">', unsafe_allow_html=True)
            st.image(image_url, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="listing-card">
                    <div style="font-size:0.8rem;opacity:0.7;">FEATURED</div>
                    <div style="font-weight:700;margin-top:0.2rem;">{title}</div>
                    <div class="listing-price">{price}</div>
                    <div style="font-size:0.86rem;opacity:0.8;">{location}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.subheader("How this app works")
    flow = st.columns(4)
    steps = [
        "Create a account and set your profile",
        "Post your ad with photos",
        "Get customers and direct calls",
        "Grow your business with featured ads",
    ]
    for col, step in zip(flow, steps):
        with col:
            st.markdown(f'<div class="block">{step}</div>', unsafe_allow_html=True)

with right_sidebar:
    st.success("Post your ad for free")
    st.write("- 4 free ads every 7 days")
    st.write("- Featured ads available")
    st.write("- Vendor dashboard support")

    st.info("Why choose Biliwaka?")
    st.write("- 100% free to list")
    st.write("- Connect directly with buyers")
    st.write("- Trusted local vendors")
    st.write("- Secure and easy to use")

    with get_connection() as conn:
        total_users = conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()["n"]
        total_ads = conn.execute("SELECT COUNT(*) AS n FROM ads").fetchone()["n"]
        total_clicks = conn.execute("SELECT COALESCE(SUM(clicks), 0) AS n FROM ads").fetchone()["n"]
    st.markdown(
        f"<div class='block'><b>Platform statistics</b><br>Total vendors: {total_users}<br>Active listings: {total_ads}<br>Total views: {total_clicks}</div>",
        unsafe_allow_html=True,
    )

render_footer()
