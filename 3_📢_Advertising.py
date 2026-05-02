import streamlit as st

st.set_page_config(page_title="Advertising Packages - Biliwaka", page_icon="🚀", layout="wide")

from utils import apply_theme, init_session_defaults, render_footer, render_topbar, hide_admin_sidebar_if_not_admin

init_session_defaults()
apply_theme()
hide_admin_sidebar_if_not_admin()
render_topbar()

# Create the same layout as main app
layout = st.columns([1.1, 3.5, 1.3], gap="large")
left_sidebar, center, right_sidebar = layout

with left_sidebar:
    st.markdown('<div class="block"><b>Menu</b></div>', unsafe_allow_html=True)
    
    # FIXED: Added "pages/" before the filenames!
    if st.button("🏠 Home", use_container_width=True, key="adv_home"):
        st.switch_page("Home.py")
    if st.button("📦 Listings", use_container_width=True, key="adv_list"):
        st.switch_page("pages/1_🏪_MarketSpace.py")
    if st.button("💳 Payment", use_container_width=True, key="adv_pay"):
        st.switch_page("pages/4_💳_Pay.py")
        
    st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)
        
    st.markdown(
        '<div class="block"><b>Become a Vendor</b><br>Post products and services for free.<br><br><small>4 free ads every 7 days</small></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="block"><b>Follow Us</b><br>WhatsApp • Facebook • Instagram • TikTok</div>', unsafe_allow_html=True)

with center:
    st.markdown('<h1 class="page-title">🚀 ADVERTISING PACKAGES & PRICING</h1>', unsafe_allow_html=True)

    # Individual Ad Options
    st.markdown('<h2>📌 Individual Ad Options</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
    <div class="pricing-card">
        <div class="pricing-header">
            <h3>⭐ Featured Ad</h3>
            <div class="price">25,000 UGX<span>/week</span></div>
        </div>
        <div class="pricing-content">
            <p>Top visibility placement for maximum exposure</p>
            <ul>
                <li>✓ Premium placement</li>
                <li>✓ Highlighted listing</li>
                <li>✓ Priority visibility</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
    <div class="pricing-card">
        <div class="pricing-header">
            <h3>🖼️ Banner Ad</h3>
            <div class="price">25,000 UGX<span>/week</span></div>
        </div>
        <div class="pricing-content">
            <p>High-impact display across key sections</p>
            <ul>
                <li>✓ Banner placement</li>
                <li>✓ High visibility</li>
                <li>✓ Brand exposure</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
    <div class="pricing-card">
        <div class="pricing-header">
            <h3>📣 Social Media Boost</h3>
            <div class="price">25,000 UGX<span>/week</span></div>
        </div>
        <div class="pricing-content">
            <p>Reach more customers through social promotion</p>
            <ul>
                <li>✓ Social media promotion</li>
                <li>✓ Extended reach</li>
                <li>✓ Cross-platform exposure</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Combo Offers
    st.markdown('<h2>🔥 COMBO OFFERS (BEST VALUE)</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
    <div class="pricing-card featured">
        <div class="pricing-header">
            <h3>🌱 Starter Growth Pack</h3>
            <div class="price">45,000 UGX<span>/week</span></div>
        </div>
        <div class="pricing-content">
            <div class="includes">
                <strong>✔ Featured Ad</strong><br>
                <strong>✔ Social Media Boost</strong>
            </div>
            <p><em>Perfect for growing visibility fast</em></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
    <div class="pricing-card featured">
        <div class="pricing-header">
            <h3>👁️ Visibility Pack</h3>
            <div class="price">45,000 UGX<span>/week</span></div>
        </div>
        <div class="pricing-content">
            <div class="includes">
                <strong>✔ Featured Ad</strong><br>
                <strong>✔ Banner Ad</strong>
            </div>
            <p><em>Ideal for strong on-site exposure</em></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
    <div class="pricing-card featured best-value">
        <div class="pricing-header">
            <h3>💎 Best Value Pack</h3>
            <div class="price">65,000 UGX<span>/week</span></div>
        </div>
        <div class="pricing-content">
            <div class="includes">
                <strong>✔ Featured Ad</strong><br>
                <strong>✔ Banner Ad</strong><br>
                <strong>✔ Social Media Boost</strong>
            </div>
            <p><em>Maximum reach across all platforms</em></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Growth Benefits
    st.markdown('<h2>📈 Grow Your Business Faster</h2>', unsafe_allow_html=True)
    st.markdown("""
<div class="growth-section">
    <p>Get more clicks, more calls, and more customers with targeted advertising that works.</p>
</div>
""", unsafe_allow_html=True)

    # Call to Action
    st.markdown("""
<div class="cta-section">
    <h3>📲 Contact us today to get started!</h3>
    <p>Ready to boost your business? Get in touch with our team to activate your advertising package.</p>
    <div class="contact-methods">
        <strong>WhatsApp:</strong> +256 775998783<br>
        <strong>Email:</strong> biliwakaug@gmail.com<br>
        <strong>Phone:</strong> +256 775998783
    </div>
</div>
""", unsafe_allow_html=True)

with right_sidebar:
    st.success("🚀 Boost Your Business")
    st.write("- Get more visibility")
    st.write("- Reach more customers")
    st.write("- Increase sales")
    st.write("- Track results")

    st.info("📞 Quick Contact")
    st.write("**WhatsApp:** +256 775998783")
    st.write("**Email:** biliwakaug@gmail.com")

    st.warning("💡 Pro Tip")
    st.write("Combo packages offer the best value for maximum exposure across all platforms.")

# Custom CSS for pricing cards (Adjusted to perfectly match your dark blue theme)
st.markdown("""
<style>
.pricing-card {
    background: #111827;
    border-radius: 12px;
    padding: 2rem;
    border: 1px solid #1f2937;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    margin-bottom: 1rem;
    transition: transform 0.3s ease;
}

.pricing-card:hover {
    transform: translateY(-5px);
    border-color: #f59e0b;
}

.pricing-card.featured {
    border: 2px solid #25D366;
}

.pricing-card.best-value {
    border: 2px solid #f59e0b;
    position: relative;
}

.pricing-card.best-value::before {
    content: "BEST VALUE";
    position: absolute;
    top: -10px;
    right: 20px;
    background: #f59e0b;
    color: #000;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: bold;
}

.pricing-header {
    text-align: center;
    margin-bottom: 1.5rem;
}

.pricing-header h3 {
    margin: 0 0 0.5rem 0;
    color: #fbbf24;
}

.price {
    font-size: 2rem;
    font-weight: bold;
    color: #25D366;
}

.price span {
    font-size: 1rem;
    font-weight: normal;
    color: #94a3b8;
}

.pricing-content {
    text-align: center;
}

.pricing-content p {
    color: #94a3b8;
    margin-bottom: 1rem;
}

.pricing-content ul {
    list-style: none;
    padding: 0;
    text-align: left;
}

.pricing-content li {
    padding: 0.5rem 0;
    border-bottom: 1px solid #1f2937;
    color: #d1d5db;
}

.includes {
    background: #1f2937;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
    color: #e5e7eb;
}

.growth-section {
    background: linear-gradient(135deg, #1e3a5f 0%, #111827 100%);
    color: #e5e7eb;
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    margin: 2rem 0;
    border: 1px solid #1f2937;
}

.cta-section {
    background: #111827;
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    margin: 2rem 0;
    border: 1px solid #1f2937;
}

.contact-methods {
    margin-top: 1rem;
    line-height: 1.8;
    color: #d1d5db;
}

.cta-section h3 {
    color: #fbbf24 !important;
}

.cta-section p {
    color: #94a3b8 !important;
}
</style>
""", unsafe_allow_html=True)

render_footer()