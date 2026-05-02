from __future__ import annotations

import streamlit as st
from pathlib import Path


def init_session_defaults() -> None:
    if "cart" not in st.session_state:
        st.session_state.cart = []
    if "user" not in st.session_state:
        st.session_state.user = None
    if "role" not in st.session_state:
        st.session_state.role = "guest"
    # Force dark mode to always be True
    st.session_state.dark_mode = True


def apply_theme() -> None:
    """Applies the permanent dark mode theme."""
    bg = "#0f172a"
    surface = "#111827"
    text = "#e5e7eb"
    muted = "#94a3b8"
    border = "#1f2937"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: {bg};
            color: {text};
        }}
        .stApp p, .stApp span, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp li {{
            color: {text};
        }}
        .stApp a {{
            color: #93c5fd;
        }}
        
        /* Hide the default menu items and footer, but KEEP the hamburger button */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        [data-testid="stSidebarCollapseButton"] {{color: #e5e7eb !important;}}

        .stTextInput input, .stTextArea textarea, .stNumberInput input {{
            color: {text} !important;
        }}
        div[data-testid="stMetricValue"] {{
            color: {text};
        }}
        .block {{
            background: {surface};
            border: 1px solid {border};
            border-radius: 14px;
            padding: 1rem;
            margin-bottom: 0.8rem;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
        }}
        .hero-wrap {{
            background: linear-gradient(90deg, #111827 0%, #f59e0b 100%);
            border-radius: 14px;
            padding: 1.2rem 1.3rem;
            color: white;
            margin-bottom: 0.9rem;
        }}
        .category-chip {{
            background: {surface};
            border: 1px solid {border};
            border-radius: 12px;
            padding: 0.7rem 0.8rem;
            text-align: center;
            font-size: 0.9rem;
            color: {text};
            min-height: 64px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 0.55rem;
        }}
        .category-label {{
            line-height: 1.2;
            font-weight: 600;
        }}
        .listing-image img {{
            border-radius: 10px;
            height: 170px;
            object-fit: cover;
        }}
        .listing-card {{
            background: {surface};
            border: 1px solid {border};
            border-radius: 12px;
            padding: 0.75rem;
            min-height: 140px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
            margin-bottom: 0.8rem;
        }}
        .featured {{
            border: 3px solid #C8A96A !important;
        }}
        .listing-price {{
            color: #f59e0b;
            font-weight: 700;
            margin: 0.2rem 0;
        }}
        .footer {{
            color: {muted};
            text-align: center;
            margin-top: 1rem;
            font-size: 0.85rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_topbar() -> None:
    st.markdown(
        """
        <div class="block">
            <div style="display:flex;justify-content:center;align-items:center;flex-wrap:wrap;">
                <div style="text-align: center;">
                    <h2 style="margin:0;">Biliwaka MarketSpace</h2>
                    <div style="opacity:0.85;">Search products, services, and vendors</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.markdown('<div class="footer">© 2026 Biliwaka MarketSpace</div>', unsafe_allow_html=True)


def guard_logged_in() -> bool:
    init_session_defaults()
    if "user" not in st.session_state or st.session_state.user is None:
        st.warning("Please log in first.")
        st.stop()
    return True


def guard_admin() -> bool:
    init_session_defaults()
    guard_logged_in()
    if st.session_state.get("role") != "admin":
        st.error("Admin access only.")
        st.stop()
    return True


def get_local_image(image_path: str, fallback_url: str = None):
    """
    Safely handles local images. 
    If running locally, it uses the local file.
    If on Streamlit Cloud (or file is missing), it uses a fallback URL.
    """
    path = Path(image_path)
    if path.exists():
        return str(path)
    
    # If fallback is provided, use it. Otherwise return a blank 1x1 pixel.
    return fallback_url if fallback_url else "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="


def render_carousel(media_list: list, auto_slide: bool = True, interval: int = 3000) -> None:
    if not media_list:
        return
    
    # Initialize state
    if 'carousel_index' not in st.session_state:
        st.session_state.carousel_index = 0
    if 'carousel_tick' not in st.session_state:
        st.session_state.carousel_tick = 0

    # Auto-slide logic using a tick counter
    if auto_slide:
        st.session_state.carousel_tick += 1
        # Approximate 1 tick = ~100ms. 50 ticks = 5 seconds.
        ticks_needed = max(10, interval // 100) 
        if st.session_state.carousel_tick >= ticks_needed:
            st.session_state.carousel_index = (st.session_state.carousel_index + 1) % len(media_list)
            st.session_state.carousel_tick = 0
    
    current_index = st.session_state.carousel_index % len(media_list)
    current_media = media_list[current_index]
    
    st.markdown("""
    <style>
    .carousel-image img, .carousel-image video {
        width: 100%; height: 350px; object-fit: cover; border-radius: 14px; display: block;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([0.5, 9, 0.5])
    with col1:
        if st.button("◀", key="prev_btn"):
            st.session_state.carousel_index = (current_index - 1) % len(media_list)
            st.rerun()
    with col2:
        if isinstance(current_media, str) and current_media.endswith('.mp4'):
            st.video(current_media)
        else:
            st.image(current_media, use_container_width=True)
    with col3:
        if st.button("▶", key="next_btn"):
            st.session_state.carousel_index = (current_index + 1) % len(media_list)
            st.rerun()


def hide_admin_sidebar_if_not_admin():
    """Completely removes the Admin link from the page source for non-admins."""
    is_admin = st.session_state.get("role") == "admin"
    if not is_admin:
        st.markdown("""
        <style>
            [data-testid="stSidebarNav"] li:has(a[href*="Admin"]) {
                display: none !important;
            }
        </style>
        """, unsafe_allow_html=True)


# Alias so both names work — your Admin.py was importing "hide_admin_if_not_admin"
def hide_admin_if_not_admin():
    """Alias for hide_admin_sidebar_if_not_admin — stops non-admins from seeing the Admin page."""
    hide_admin_sidebar_if_not_admin()