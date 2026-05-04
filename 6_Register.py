import streamlit as st

st.set_page_config(page_title="Register - Biliwaka", page_icon="📝", layout="wide")

from auth import register_user
from database import init_db, get_connection
from utils import apply_theme, render_footer, render_topbar, hide_admin_sidebar_if_not_admin, init_session_defaults

init_session_defaults()
init_db()
apply_theme()
hide_admin_sidebar_if_not_admin()
render_topbar()

# HARD BLOCK: If logged in, absolutely nothing below this renders. No greyed out forms.
if st.session_state.get("user"):
    st.error("You must **Log Out** before creating a new account.")
    if st.button("Go to Login to Logout", use_container_width=True):
        st.switch_page("pages/5_🔐_Login.py")
    st.stop()

st.title("Create Account")

st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background: transparent; }
    .stTabs [data-baseweb="tab"] { border-radius: 8px; padding: 10px 20px; background-color: #111827; color: #e5e7eb; border: 1px solid #1f2937; }
    .stTabs [aria-selected="true"] { background-color: #f59e0b !important; color: black !important; font-weight: bold; border: 1px solid #f59e0b !important; }
</style>
""", unsafe_allow_html=True)

tab_email, tab_phone = st.tabs(["Register with Email", "Register with Phone Number"])

# -----------------------------
# EMAIL REGISTER TAB
# -----------------------------
with tab_email:
    with st.form("register_form_email", clear_on_submit=True):
        full_name = st.text_input("Full Name", key="reg_name_email")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass_email")
        role = st.selectbox("Account Type", ["buyer", "vendor"], key="reg_role_email")
        submitted = st.form_submit_button("Create Account")

    if submitted:
        ok, message = register_user(full_name, email, password, role=role)
        if ok:
            st.success(message)
            st.info("You can now log in from the Login page.")
        else:
            st.error(message)

# -----------------------------
# PHONE REGISTER TAB
# -----------------------------
with tab_phone:
    with st.form("register_form_phone", clear_on_submit=True):
        full_name = st.text_input("Full Name", key="reg_name_phone")
        phone = st.text_input("Phone Number (e.g. 077XXXXXXX)", max_chars=12, key="reg_phone")
        password = st.text_input("Password", type="password", key="reg_pass_phone")
        role = st.selectbox("Account Type", ["buyer", "vendor"], key="reg_role_phone")
        submitted = st.form_submit_button("Create Account")

    if submitted:
        if not full_name or not phone or not password:
            st.error("All fields are required.")
        else:
            with get_connection() as conn:
                existing_phone = conn.execute("SELECT id FROM users WHERE phone = ?", (phone.strip(),)).fetchone()
            if existing_phone:
                st.error("This phone number is already registered.")
            else:
                ok, message = register_user(full_name, email="", phone=phone, password=password, role=role)
                if ok:
                    st.success(message)
                    st.info("You can now log in using your Phone Number.")
                else:
                    st.error(message)

render_footer()
