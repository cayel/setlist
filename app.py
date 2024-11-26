import streamlit as st

st.set_page_config(page_title="Setlist", page_icon=":studio_microphone:")

home_page = st.Page("home.py", title="Home", icon=":material/home:")
search_page = st.Page("search.py", title="Search", icon=":material/search:")    
statistics_page = st.Page("stats.py", title="Statistics", icon=":material/insert_chart_outlined:")
settings_page = st.Page("settings.py", title="Settings", icon=":material/settings_applications:")
admin_page = st.Page("admin.py", title="Administration", icon=":material/verified_user:")

pg = st.navigation([home_page, search_page, statistics_page, settings_page, admin_page])
pg.run()

