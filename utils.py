from __future__ import annotations

import streamlit as st


def init_session_defaults() -> None:
    if "cart" not in st.session_state:
        st.session_state.cart = []
    if "user" not in st.session_state:
        st.session_state.user = None
    if "role" not in st.session_state:
        st.session_state.role = "guest"
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True


def render_theme_toggle() -> None:
    init_session_defaults()
    st.sidebar.toggle("Dark mode", key="dark_mode")


def apply_theme() -> None:
    init_session_defaults()
    dark_mode = st.session_state.dark_mode

    bg = "#0f172a" if dark_mode else "#F7F3EE"
    surface = "#111827" if dark_mode else "#ffffff"
    text = "#e5e7eb" if dark_mode else "#3A2A26"
    muted = "#94a3b8" if dark_mode else "#6a5b56"
    border = "#1f2937" if dark_mode else "#e7ddd3"

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
            color: {"#93c5fd" if dark_mode else "#1d4ed8"};
        }}
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
            <div style="display:flex;justify-content:space-between;gap:0.8rem;align-items:center;flex-wrap:wrap;">
                <div>
                    <h2 style="margin:0;">Biliwaka MarketSpace</h2>
                    <div style="opacity:0.85;">Search products, services, and vendors</div>
                </div>
                <div style="font-size:0.9rem;opacity:0.8;">Local marketplace for buyers and sellers</div>
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


def render_carousel(images: list, auto_slide: bool = True, interval: int = 3000) -> None:
    """Render an image carousel with auto-slide functionality.
    
    Args:
        images: List of image URLs or paths
        auto_slide: Whether to automatically slide through images
        interval: Auto-slide interval in milliseconds
    """
    if not images:
        return
    
    # Initialize carousel state
    if 'carousel_index' not in st.session_state:
        st.session_state.carousel_index = 0
    
    # Auto-slide functionality
    if auto_slide:
        if 'last_slide_time' not in st.session_state:
            st.session_state.last_slide_time = 0
        
        # Simple auto-slide using session state
        current_time = st.session_state.get('current_time', 0)
        if current_time - st.session_state.last_slide_time > interval:
            st.session_state.carousel_index = (st.session_state.carousel_index + 1) % len(images)
            st.session_state.last_slide_time = current_time
    
    # Get current image
    current_index = st.session_state.carousel_index % len(images)
    current_image = images[current_index]
    
    # Render carousel container
    st.markdown("""
    <style>
    .carousel-container {
        position: relative;
        width: 100%;
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        margin-bottom: 1rem;
    }
    .carousel-image {
        width: 100%;
        height: 400px;
        object-fit: cover;
        display: block;
    }
    .carousel-controls {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        width: 100%;
        display: flex;
        justify-content: space-between;
        padding: 0 1rem;
        pointer-events: none;
    }
    .carousel-btn {
        background: rgba(0, 0, 0, 0.6);
        color: white;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        font-size: 18px;
        cursor: pointer;
        pointer-events: all;
        transition: background 0.3s;
    }
    .carousel-btn:hover {
        background: rgba(0, 0, 0, 0.8);
    }
    .carousel-indicators {
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        gap: 8px;
    }
    .indicator {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.5);
        cursor: pointer;
        transition: background 0.3s;
    }
    .indicator.active {
        background: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Manual navigation buttons
    col1, col2, col3 = st.columns([1, 8, 1])
    
    with col1:
        if st.button("◀", key="prev_btn", help="Previous image"):
            st.session_state.carousel_index = (current_index - 1) % len(images)
            st.rerun()
    
    with col2:
        # Display current image
        if isinstance(current_image, str) and current_image.startswith(('http://', 'https://')):
            st.image(current_image, use_container_width=True)
        else:
            st.image(current_image, use_container_width=True)
    
    with col3:
        if st.button("▶", key="next_btn", help="Next image"):
            st.session_state.carousel_index = (current_index + 1) % len(images)
            st.rerun()
    
    # Image indicators
    indicator_cols = st.columns(len(images))
    for i, col in enumerate(indicator_cols):
        with col:
            if st.button("●" if i == current_index else "○", key=f"indicator_{i}", help=f"Go to image {i+1}"):
                st.session_state.carousel_index = i
                st.rerun()
