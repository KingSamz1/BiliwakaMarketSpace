import streamlit as st
import requests

from utils import apply_theme, init_session_defaults, render_footer, render_theme_toggle, render_topbar

st.set_page_config(page_title="Vendor Payment Checkout", page_icon="💳", layout="wide")
init_session_defaults()
render_theme_toggle()
apply_theme()
render_topbar()

# Create same layout as other pages
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
    st.title("💳 Vendor Payment Checkout")
    st.write("Pay advertising fees directly to merchant: **+256 775998783**")

    # -------------------
    # PACKAGE DISPLAY
    # -------------------
    st.markdown('<h2>📦 Available Packages</h2>', unsafe_allow_html=True)

    # Individual Ad Options
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
                <h4>🖼️ Banner Ad</h4>
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
                <h4>📣 Social Media Boost</h4>
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
    st.markdown('<h3>🔥 COMBO OFFERS (BEST VALUE)</h3>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="pricing-card featured">
            <div class="pricing-header">
                <h4>🌱 Starter Growth Pack</h4>
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
                <h4>👁️ Visibility Pack</h4>
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
                <h4>💎 Best Value Pack</h4>
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

    # -------------------
    # PAYMENT FORM
    # -------------------
    st.markdown('<h2>💳 Make Payment</h2>', unsafe_allow_html=True)

    # SELECT PROVIDER
    provider = st.radio(
        "Choose Mobile Money Provider",
        ["MTN Mobile Money", "Airtel Money"],
        horizontal=True
    )

    # Package prices mapping
    package_prices = {
        "Featured Ad - 25,000 UGX": 25000,
        "Banner Ad - 25,000 UGX": 25000,
        "Social Media Boost - 25,000 UGX": 25000,
        "Starter Growth Pack - 45,000 UGX": 45000,
        "Visibility Pack - 45,000 UGX": 45000,
        "Best Value Pack - 65,000 UGX": 65000
    }
    
    # Get initial amount from session state or default
    if 'selected_package' not in st.session_state:
        st.session_state.selected_package = "Featured Ad - 25,000 UGX"
        st.session_state.selected_amount = 25000
    
    col1, col2 = st.columns(2)
    
    with col1:
        # INPUTS
        phone = st.text_input("Your Phone Number (e.g. 2567XXXXXXX)", placeholder="2567XXXXXXXX")
        amount = st.number_input("Amount (UGX)", min_value=1000, value=st.session_state.selected_amount, step=1000)
        
    with col2:
        package = st.selectbox(
            "Select Package",
            list(package_prices.keys()),
            index=list(package_prices.keys()).index(st.session_state.selected_package)
        )
    
    # Update amount when package changes
    if package != st.session_state.selected_package:
        st.session_state.selected_package = package
        st.session_state.selected_amount = package_prices[package]
        st.rerun()

    # -------------------
    # BACKEND API
    # -------------------
    API_URL = "http://localhost:5000/checkout"

    # -------------------
    # PAY BUTTON
    # -------------------
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Pay Now", type="primary", use_container_width=True):

            if not phone:
                st.error("Please enter your phone number")
            elif len(phone) < 9:
                st.error("Please enter a valid phone number")
            else:
                payload = {
                    "provider": provider,
                    "phone": phone,
                    "amount": amount,
                    "package": package,
                    "merchant": "0775998783"
                }

                with st.spinner("Sending payment request..."):
                    try:
                        res = requests.post(API_URL, json=payload, timeout=30)

                        if res.status_code == 200:
                            data = res.json()
                            st.success("📲 Payment request sent!")
                            st.info("Check your phone and enter PIN to confirm payment.")
                            st.write("Reference ID:", data.get("reference_id", "N/A"))
                            
                            # Show payment details
                            st.markdown("---")
                            st.markdown("**Payment Details:**")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Provider:** {provider}")
                                st.write(f"**Phone:** {phone}")
                            with col2:
                                st.write(f"**Amount:** UGX {amount:,}")
                                st.write(f"**Package:** {package}")
                            
                            # Add instructions based on provider
                            st.markdown("---")
                            st.markdown("**Next Steps:**")
                            if provider == "MTN Mobile Money":
                                st.write("1. Check your phone for MTN MoMo prompt")
                                st.write("2. Enter your MTN MoMo PIN to confirm")
                                st.write("3. Wait for confirmation SMS")
                            else:
                                st.write("1. Check your phone for Airtel Money prompt") 
                                st.write("2. Enter your Airtel Money PIN to confirm")
                                st.write("3. Wait for confirmation SMS")
                                
                            # Add transaction status check
                            if 'transaction_id' in data:
                                st.markdown("---")
                                st.markdown("**Track Your Payment:**")
                                if st.button("Check Status", key="check_status"):
                                    try:
                                        status_res = requests.get(f"{API_URL}/status/{data['transaction_id']}")
                                        if status_res.status_code == 200:
                                            status_data = status_res.json()
                                            st.info(f"Status: {status_data.get('status', 'Unknown')}")
                                        else:
                                            st.error("Could not check status")
                                    except:
                                        st.error("Status check failed")

                        else:
                            st.error("Payment failed. Please try again.")
                            try:
                                error_data = res.json()
                                st.write("Error:", error_data.get('error', 'Unknown error'))
                            except:
                                st.write(f"Server returned status code: {res.status_code}")

                    except requests.exceptions.Timeout:
                        st.error("Payment request timed out. Please try again.")
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot connect to payment server. Please make sure the server is running on localhost:5000")
                        st.info("💡 **To start the payment server:**")
                        st.code("python payment_server.py")
                    except Exception as e:
                        st.error(f"Server error: {e}")

with right_sidebar:
    st.success("💳 Quick Payment")
    st.write("- Fast & secure")
    st.write("- Instant confirmation")
    st.write("- Multiple providers")
    st.write("- 24/7 support")

    st.info("📞 Need Help?")
    st.write("**WhatsApp:** +256 775998783")
    st.write("**Email:** biliwakaug@gmail.com")
    
    st.warning("⏰ Payment Hours")
    st.write("Payments processed instantly")
    st.write("Weekdays: 6AM - 10PM")
    st.write("Weekends: 8AM - 8PM")

# Add custom CSS for pricing cards
st.markdown("""
<style>
.pricing-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 1.5rem;
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
    margin-bottom: 1rem;
}

.pricing-header h4 {
    margin: 0 0 0.5rem 0;
    color: #333;
    font-size: 1.1rem;
}

.price {
    font-size: 1.5rem;
    font-weight: bold;
    color: #2E7D32;
}

.price span {
    font-size: 0.9rem;
    font-weight: normal;
    color: #666;
}

.pricing-content {
    text-align: center;
}

.pricing-content p {
    color: #666;
    margin-bottom: 0.8rem;
    font-size: 0.9rem;
}

.pricing-content ul {
    list-style: none;
    padding: 0;
    text-align: left;
    margin-bottom: 0;
}

.pricing-content li {
    padding: 0.3rem 0;
    border-bottom: 1px solid #eee;
    color: #666;
    font-size: 0.85rem;
}

.includes {
    background: #f8f9fa;
    padding: 0.8rem;
    border-radius: 8px;
    margin: 0.8rem 0;
    color: #333;
    font-size: 0.85rem;
}

/* Dark mode fixes */
[data-testid="stApp"] .pricing-card {
    background: #1f2937 !important;
    border-color: #374151 !important;
}

[data-testid="stApp"] .pricing-header h4 {
    color: #fbbf24 !important;
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
</style>
""", unsafe_allow_html=True)

render_footer()
