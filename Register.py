import streamlit as st

from auth import register_user
from database import init_db
from utils import apply_theme, render_footer, render_theme_toggle, render_topbar

init_db()
render_theme_toggle()
apply_theme()
render_topbar()

st.title("Register")

with st.form("register_form", clear_on_submit=True):
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Account Type", ["buyer", "vendor"])
    submitted = st.form_submit_button("Create Account")

if submitted:
    ok, message = register_user(full_name, email, password, role)
    if ok:
        st.success(message)
    else:
        st.error(message)

render_footer()
