import streamlit as st

from auth import login_user
from database import init_db
from utils import apply_theme, render_footer, render_theme_toggle, render_topbar

init_db()
render_theme_toggle()
apply_theme()
render_topbar()

st.title("Login")

with st.form("login_form", clear_on_submit=False):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

if submitted:
    user = login_user(email, password)
    if user:
        st.session_state.user = user
        st.session_state.role = user["role"]
        st.success(f"Welcome back, {user['full_name']}!")
    else:
        st.error("Invalid email or password.")

if st.session_state.get("user"):
    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.role = "guest"
        st.success("Logged out.")

render_footer()
