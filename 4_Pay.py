import streamlit as st

from utils import apply_theme, init_session_defaults, render_footer, render_topbar, hide_admin_sidebar_if_not_admin

st.set_page_config(page_title="Vendor Payment - Biliwaka", page_icon="💳", layout="wide")
init_session_defaults()
apply_theme()
hide_admin_sidebar_if_not_admin()
render_topbar()

# Create same layout as other pages
layout = st.columns([1.1, 3.5, 1.3], gap="large")
left_sidebar, center, right_sidebar = layout

with left_sidebar:
    st.markdown('<div class="block"><b>Menu</b></div>', unsafe_allow_html=True)
    
    # FIXED: Added "pages/" before the filename!
    if st.button("🏠 Home", use_container_width=True, key="pay_home"):
        st.switch_page("Home.py")
    if st.button("📦 Listings", use_container_width=True, key="pay_list"):
        st.switch_page("pages/1_🏪_MarketSpace.py")
    if st.button("🚀 Advertising", use_container_width=True, key="pay_adv"):
        st.switch_page("pages/3_📢_Advertising.py")
        
    st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)
        
    st.markdown(
        '<div class="block"><b>Become a Vendor</b><br>Post products and services for free.<br><br><small>4 free ads every 7 days</small></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="block"><b>Follow Us</b><br>WhatsApp • Facebook • Instagram • TikTok</div>', unsafe_allow_html=True)

with center:
    st.title("💳 Complete Your Payment")
    st.caption("Secure, reliable manual mobile money payment")

    # -------------------
    # PACKAGE DISPLAY
    # -------------------
    st.markdown('<h2>📦 Available Packages</h2>', unsafe_allow_html=True)

    st.markdown('<h3>⭐ Individual Ad Options</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="pricing-card">
            <div class="pricing-header">
                <h4>⭐ Featured Ad</h4>
                <div class="price">25,000 UGX<span>/week</span></div>
            </div>
            <div class="pricing-content">
                <p>Top visibility placement</p>
                <ul><li>✓ Premium placement</li><li>✓ Highlighted listing</li></ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="pricing-card">
            <div class="pricing-header">
                <h4>🖼️ Banner Ad</h4>
                <div class="price">25,000 UGX<span>/week</span></div>
            </div>
            <div class="pricing-content">
                <p>High-impact display</p>
                <ul><li>✓ Banner placement</li><li>✓ High visibility</li></ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="pricing-card">
            <div class="pricing-header">
                <h4>📣 Social Media Boost</h4>
                <div class="price">25,000 UGX<span>/week</span></div>
            </div>
            <div class="pricing-content">
                <p>Social promotion</p>
                <ul><li>✓ Social media ads</li><li>✓ Extended reach</li></ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<h3>🔥 COMBO OFFERS (BEST VALUE)</h3>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="pricing-card featured">
            <div class="pricing-header">
                <h4>🌱 Starter Pack</h4>
                <div class="price">45,000 UGX<span>/week</span></div>
            </div>
            <div class="pricing-content">
                <div class="includes"><strong>✔ Featured Ad</strong><br><strong>✔ Social Boost</strong></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="pricing-card featured">
            <div class="pricing-header">
                <h4>👁️ Visibility Pack</h4>
                <div class="price">45,000 UGX<span>/week</span></div>
            </div>
            <div class="pricing-content">
                <div class="includes"><strong>✔ Featured Ad</strong><br><strong>✔ Banner Ad</strong></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="pricing-card featured best-value">
            <div class="pricing-header">
                <h4>💎 Best Value</h4>
                <div class="price">65,000 UGX<span>/week</span></div>
            </div>
            <div class="pricing-content">
                <div class="includes"><strong>✔ Featured Ad</strong><br><strong>✔ Banner Ad</strong><br><strong>✔ Social Boost</strong></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # -------------------
    # MANUAL PAYMENT FLOW (IMPROVED)
    # -------------------
    st.markdown('<h2>📲 How to Pay</h2>', unsafe_allow_html=True)

    # 1. Select Package
    package_prices = {
        "Featured Ad - 25,000 UGX": 25000,
        "Banner Ad - 25,000 UGX": 25000,
        "Social Media Boost - 25,000 UGX": 25000,
        "Starter Pack - 45,000 UGX": 45000,
        "Visibility Pack - 45,000 UGX": 45000,
        "Best Value - 65,000 UGX": 65000
    }
    
    if 'selected_package' not in st.session_state:
        st.session_state.selected_package = "Featured Ad - 25,000 UGX"
        st.session_state.selected_amount = 25000
    
    package = st.selectbox(
        "1. Select Package",
        list(package_prices.keys()),
        index=list(package_prices.keys()).index(st.session_state.selected_package)
    )
    
    if package != st.session_state.selected_package:
        st.session_state.selected_package = package
        st.session_state.selected_amount = package_prices[package]
        st.rerun()

    amount = st.session_state.selected_amount

    # 2. Display Payment Instructions
    st.markdown("""
    <div class="payment-instructions">
        <h4 style="margin-top:0;">Send exactly <span style="color:#25D366; font-size:1.5rem;">UGX {:,}</span> to:</h4>
        <div class="number-box">
            <span class="number-label">MTN / AIRTEL MONEY</span>
            <span class="number-code">0775998783</span>
            <span class="number-name">Scovia Kyazike</span>
        </div>
    </div>
    """.format(amount), unsafe_allow_html=True)

    # 3. Action Buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("📋 Copy Number", use_container_width=True):
            st.code("0775998783")
            st.success("Number copied to clipboard!")
            
    with col2:
        # Opens the native phone dialer/MM menu safely
        st.markdown("""
        <a href="tel:*165%23" target="_blank" style="text-decoration: none;">
            <button class="mtn-btn" style="width: 100%; padding: 12px; background: linear-gradient(135deg, #FFC107, #FF9800); color: #000; border: none; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 1rem;">
                📱 Open MTN Menu
            </button>
        </a>
        """, unsafe_allow_html=True)
        
    with col3:
        if st.button("✅ I Have Paid", type="primary", use_container_width=True):
            st.session_state.payment_submitted = True
            st.rerun()

    # 4. Success State
    if st.session_state.get("payment_submitted"):
        st.markdown("---")
        st.markdown("""
        <div class="success-box">
            <h3>✅ Payment Submitted!</h3>
            <p>Thank you for choosing Biliwaka Advertising.</p>
            <p><strong>What happens next?</strong></p>
            <ol>
                <li>Our team will verify your payment (usually takes 5-30 minutes).</li>
                <li>You will get a confirmation message on WhatsApp/Email.</li>
                <li>Your package will be activated instantly after verification!</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Make Another Payment", use_container_width=True):
            st.session_state.payment_submitted = False
            st.rerun()

with right_sidebar:
    st.success("💳 Quick Payment")
    st.write("- Fast & secure")
    st.write("- Works on all phones")
    st.write("- No app needed")

    st.info("📞 Need Help?")
    st.write("**WhatsApp:** +256 775998783")
    st.write("**Email:** biliwakaug@gmail.com")
    
    st.warning("⏰ Payment Hours")
    st.write("Verified instantly during:")
    st.write("Weekdays: 6AM - 10PM")
    st.write("Weekends: 8AM - 8PM")

# Custom CSS for pricing cards and payment UI
st.markdown("""
<style>
.pricing-card {
    background: #111827;
    border-radius: 12px;
    padding: 1.5rem;
    border: 1px solid #1f2937;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    margin-bottom: 1rem;
    transition: transform 0.3s ease;
}
.pricing-card:hover { transform: translateY(-5px); border-color: #f59e0b; }
.pricing-card.featured { border: 2px solid #25D366; }
.pricing-card.best-value { border: 2px solid #f59e0b; position: relative; }
.pricing-card.best-value::before {
    content: "BEST VALUE"; position: absolute; top: -10px; right: 20px;
    background: #f59e0b; color: #000; padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;
}
.pricing-header { text-align: center; margin-bottom: 1rem; }
.pricing-header h4 { margin: 0 0 0.5rem 0; color: #fbbf24; font-size: 1.1rem; }
.price { font-size: 1.5rem; font-weight: bold; color: #25D366; }
.price span { font-size: 0.9rem; font-weight: normal; color: #94a3b8; }
.pricing-content { text-align: center; }
.pricing-content p { color: #94a3b8; margin-bottom: 0.8rem; font-size: 0.9rem; }
.pricing-content ul { list-style: none; padding: 0; text-align: left; margin-bottom: 0; }
.pricing-content li { padding: 0.3rem 0; border-bottom: 1px solid #1f2937; color: #d1d5db; font-size: 0.85rem; }
.includes { background: #1f2937; padding: 0.8rem; border-radius: 8px; margin: 0.8rem 0; color: #e5e7eb; font-size: 0.85rem; }

/* Payment UI Styles */
.payment-instructions {
    background: #1f2937; padding: 2rem; border-radius: 14px; text-align: center; margin-bottom: 2rem; border: 1px solid #374151;
}
.payment-instructions h4 { color: #e5e7eb; }
.number-box {
    margin-top: 1.5rem; background: #111827; padding: 1.5rem; border-radius: 12px; border: 2px dashed #f59e0b;
}
.number-label { display: block; font-size: 0.85rem; color: #94a3b8; margin-bottom: 0.5rem; }
.number-code { display: block; font-size: 2.5rem; font-weight: 900; color: #fbbf24; letter-spacing: 2px; }
.number-name { display: block; font-size: 1rem; color: #d1d5db; margin-top: 0.5rem; }

.success-box {
    background: linear-gradient(135deg, #1a2e1a 0%, #111827 100%); padding: 2rem; border-radius: 14px;
    border: 1px solid #25D366; color: #e5e7eb;
}
.success-box h3 { color: #25D366; margin-top: 0; }
.success-box ol { padding-left: 20px; line-height: 1.8; }
</style>
""", unsafe_allow_html=True)

render_footer()
