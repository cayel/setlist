import streamlit as st
from setlist_api import get_attended_events
import pandas as pd
import time
from database import save_all_events

st.title('Administration')

with st.expander('Refresh the database',icon=':material/refresh:'):
    st.write('This will refresh the database with the latest data from the Setlist.fm API.')
    data = get_attended_events(1)
    nb_events = data['total']
    st.write(f'You have attended {nb_events} events.')
    last_updated = data['setlist'][0]['eventDate']
    st.write(f'Last updated: {last_updated}')
    items_per_page = data['itemsPerPage']
    nb_pages = nb_events // items_per_page + 1
    if st.button('Refresh', icon=':material/refresh:'):
        df = pd.DataFrame()
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)
        for page in range(1, nb_pages+1):
            data = get_attended_events(page)
            if 'setlist' in data:
                df_new = pd.json_normalize(data['setlist'])
                df = pd.concat([df, df_new], ignore_index=True)
                my_bar.progress(page / (nb_pages +1), text=progress_text)
                time.sleep(0.5)
            else:
                break
        
        save_all_events(df)
        st.write('Data saved in your database.')
        my_bar.empty()