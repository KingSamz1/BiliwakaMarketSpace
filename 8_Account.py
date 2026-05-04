import streamlit as st

st.set_page_config(page_title="My Account - Biliwaka", page_icon="👤", layout="wide")

from database import get_connection, init_db
from utils import apply_theme, init_session_defaults, render_footer, render_topbar, guard_logged_in
from auth import hash_password

init_session_defaults()
init_db()
apply_theme()
guard_logged_in()
render_topbar()

user = st.session_state.user

st.title("My Account Settings")

with st.form("update_profile"):
    st.subheader("Personal Information")
    col1, col2 = st.columns(2)
    
    with col1:
        new_name = st.text_input("Full Name", value=user['full_name'])
        new_phone = st.text_input("Phone Number", value=user.get('phone', ''))
    
    with col2:
        new_email = st.text_input("Email", value=user['email'])
        new_pass = st.text_input("New Password (leave blank to keep current)", type="password")

    if st.form_submit_button("💾 Save Changes"):
        with get_connection() as conn:
            if new_pass:
                pass_hash = hash_password(new_pass)
                conn.execute("UPDATE users SET full_name=?, phone=?, email=?, password_hash=? WHERE id=?", 
                             (new_name, new_phone, new_email, pass_hash, user['id']))
            else:
                conn.execute("UPDATE users SET full_name=?, phone=?, email=? WHERE id=?", 
                             (new_name, new_phone, new_email, user['id']))
            
            # Update session state so the topbar updates immediately
            st.session_state.user['full_name'] = new_name
            st.session_state.user['email'] = new_email
            st.session_state.user['phone'] = new_phone
            
        st.success("Profile updated successfully!")
        st.rerun()

st.markdown("---")
st.subheader("Subscription Status")
is_sub = user.get('is_subscription', False)
if is_sub:
    st.success("🌟 You are a Pro Vendor!")
else:
    st.info("Free Account. Upgrade to Pro to unlock unlimited listings and premium features.")
    if st.button("Upgrade to Pro", use_container_width=True):
        st.switch_page("pages/4_💳_Pay.py")

render_footer()
