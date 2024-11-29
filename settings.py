import streamlit as st
from users.users_db import get_user_name, is_table_users_exists, insert_user, create_table_users
from setlist_api import get_user_info

st.title('Settings')

if not is_table_users_exists():
    create_table_users()

user_name = get_user_name()

if user_name:
    user_info = get_user_info(user_name)
    st.write(user_info['url'])

user_name = st.text_input('Enter your user name:', user_name)
if st.button('Submit'):
    insert_user(user_name)
    st.write(f'User {user_name} has been added.')
