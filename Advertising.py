import streamlit as st
from utils import apply_theme, init_session_defaults, render_footer, render_theme_toggle, render_topbar

st.set_page_config(page_title="Advertising Packages - Biliwaka", page_icon="🚀", layout="wide")
init_session_defaults()
render_theme_toggle()
apply_theme()
render_topbar()

# Create the same layout as main app
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

# Add custom CSS for pricing cards
st.markdown("""
<style>
.pricing-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
    transition: transform 0.3s ease;
}

.pricing-card:hover {
    transform: translateY(-5px);
}

.pricing-card.featured {
    border: 2px solid #4CAF50;
}

.pricing-card.best-value {
    border: 2px solid #FFD700;
    position: relative;
}

.pricing-card.best-value::before {
    content: "BEST VALUE";
    position: absolute;
    top: -10px;
    right: 20px;
    background: #FFD700;
    color: #333;
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
    color: #333;
}

.price {
    font-size: 2rem;
    font-weight: bold;
    color: #2E7D32;
}

.price span {
    font-size: 1rem;
    font-weight: normal;
    color: #666;
}

.pricing-content {
    text-align: center;
}

.pricing-content p {
    color: #666;
    margin-bottom: 1rem;
}

.pricing-content ul {
    list-style: none;
    padding: 0;
    text-align: left;
}

.pricing-content li {
    padding: 0.5rem 0;
    border-bottom: 1px solid #eee;
    color: #666;
}

.includes {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
    color: #333;
}

.growth-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    margin: 2rem 0;
}

.cta-section {
    background: #f8f9fa;
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    margin: 2rem 0;
}

.contact-methods {
    margin-top: 1rem;
    line-height: 1.8;
    color: #333;
}

/* Dark mode fixes */
[data-testid="stApp"] .pricing-card {
    background: #1f2937 !important;
    border-color: #374151 !important;
}

[data-testid="stApp"] .pricing-header h3 {
    color: #fbbf24 !important; /* Bright amber/yellow for high visibility */
}

[data-testid="stApp"] .pricing-content p {
    color: #d1d5db !important;
}

[data-testid="stApp"] .pricing-content li {
    color: #d1d5db !important;
    border-color: #374151 !important;
}

[data-testid="stApp"] .includes {
    background: #374151 !important;
    color: #e5e7eb !important;
}

[data-testid="stApp"] .cta-section {
    background: #1f2937 !important;
}

[data-testid="stApp"] .contact-methods {
    color: #e5e7eb !important;
}

[data-testid="stApp"] .cta-section h3,
[data-testid="stApp"] .cta-section p {
    color: #e5e7eb !important;
}
</style>
""", unsafe_allow_html=True)

render_footer()
