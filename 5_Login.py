import streamlit as st
import json

st.set_page_config(page_title="Login - Biliwaka", page_icon="🔐", layout="wide")

from auth import login_user, hash_password
from database import init_db, get_connection
from utils import apply_theme, render_footer, render_topbar, hide_admin_sidebar_if_not_admin, init_session_defaults

init_session_defaults()
init_db()
apply_theme()
hide_admin_sidebar_if_not_admin()
render_topbar()

# --- BULLETPROOF SESSION PERSISTENCE ---
def save_session():
    """Saves session to browser local storage so it survives refreshes."""
    if st.session_state.get("user"):
        user_data = json.dumps({
            "id": st.session_state.user["id"],
            "first_name": st.session_state.user["first_name"],
            "full_name": st.session_state.user["full_name"],
            "email": st.session_state.user["email"],
            "role": st.session_state.user["role"],
            "is_subscription": st.session_state.user.get("is_subscription", 0),
            "phone": st.session_state.user.get("phone", "")
        })
        st.markdown(f"""
        <script>
            try {{
                localStorage.setItem('biliwaka_session', '{user_data}');
            }} catch(e) {{}}
        </script>
        """, unsafe_allow_html=True)

# Check local storage on load
st.markdown("""
<script>
    try {
        const saved = localStorage.getItem('biliwaka_session');
        if (saved) {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                key: 'loaded_session',
                value: saved
            }, '*');
        }
    } catch(e) {}
</script>
""", unsafe_allow_html=True)
loaded = st.text_input("loaded_session", label_visibility="collapsed")
if loaded and not st.session_state.get("user"):
    try:
        u = json.loads(loaded)
        st.session_state.user = u
        st.session_state.role = u["role"]
    except: pass

# CSS Tabs
st.markdown("""<style>
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background: transparent; }
    .stTabs [data-baseweb="tab"] { border-radius: 8px; padding: 10px 20px; background-color: #111827; color: #e5e7eb; border: 1px solid #1f2937; }
    .stTabs [aria-selected="true"] { background-color: #f59e0b !important; color: black !important; font-weight: bold; border: 1px solid #f59e0b !important; }
</style>""", unsafe_allow_html=True)

st.title("Login")

if st.session_state.get("user"):
    st.success(f"Currently logged in as: **{st.session_state.user['full_name']}** ({st.session_state.role})")
    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.role = "guest"
        st.markdown('<script>try{localStorage.removeItem("biliwaka_session");}catch(e){}</script>', unsafe_allow_html=True)
        st.success("Logged out.")
        st.rerun()
else:
    tab_email, tab_phone = st.tabs(["Login with Email", "Login with Phone Number"])

    with tab_email:
        with st.form("login_form_email"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

        if submitted:
            user = login_user(email, password)
            if user:
                st.session_state.role = user["role"]
                st.session_state.user = user
                save_session()
                # Force Streamlit to remember via URL Parameters
                st.query_params["id"] = str(user["id"])
                st.query_params["role"] = user["role"]

                st.switch_page("Home.py")
            else:
                st.error("Invalid email or password.")

    with tab_phone:
        st.info("Enter the phone number you used to register.")
        with st.form("login_form_phone"):
            phone = st.text_input("Phone Number (e.g. 077XXXXXXX)", max_chars=12)
            password = st.text_input("Password", type="password", key="phone_pass")
            submitted = st.form_submit_button("Login")

        if submitted:
            with get_connection() as conn:
                row = conn.execute("SELECT id, first_name, full_name, email, role, is_subscription, password_hash, phone FROM users WHERE phone = ?", (phone.strip(),)).fetchone()

            if row and row["password_hash"] == hash_password(password):
                user = {"id": row["id"], "first_name": row["first_name"], "full_name": row["full_name"], "email": row["email"], "role": row["role"], "is_subscription": bool(row["is_subscription"]), "phone": row["phone"]}
                st.session_state.role = user["role"]
                st.session_state.user = user
                save_session()
                st.query_params["id"] = str(user["id"])
                st.query_params["role"] = user["role"]
                
                st.switch_page("Home.py")
            else:
                st.error("Invalid phone number or password.")

render_footer()
