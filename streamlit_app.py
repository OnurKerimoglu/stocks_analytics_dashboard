import streamlit as st

from config.config import load_configs

env = st.secrets["global"]["env"]
CONFIG = load_configs(env)

dashboard = st.Page(
    "dashboard_page.py", title="Dashboard", icon=":material/dashboard:", default=True
)
admin = st.Page(
    "admin_page.py", title="Admin", icon=":material/admin_panel_settings:")


pg = st.navigation(
    # {
    #     "Dashboard": [dashboard],
    #     "Admin": [admin]
    # },
    [
        dashboard,
        admin
    ],
    # position="hidden"
    expanded = False
)

pg.run()