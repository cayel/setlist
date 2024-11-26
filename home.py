import streamlit as st
from database import get_user_name, load_all_events
from setlist_api import get_user_info
import pandas as pd

def get_count_events_for_year(df, year):
    # Filter events for the given year
    df_year = df[df['eventDate'].dt.year == year]
    return len(df_year)

st.title('Home')

user_name = get_user_name()

if user_name:
    user_info = get_user_info(user_name)
    st.write(user_info['url'])
    df = load_all_events()
    if df.empty:
        st.warning('No event found in the database.', icon=':material/warning:')
        st.write('You can refresh the database in the administration page.')
    else:
        st.write(f'You have attended {len(df)} events.')
        number_of_events = len(df)
        current_year = pd.Timestamp.now().year
        last_year = current_year - 1
        number_of_events_current_year = get_count_events_for_year(df, current_year)
        number_of_events_last_year = get_count_events_for_year(df, last_year)
        st.metric(label="Events this year", value=number_of_events_current_year, delta=number_of_events_current_year-number_of_events_last_year)
        st.header('Last 10 events')
        # Display the last 10 events : date, artist, venue
        df_last_10 = df[['eventDate', 'artist.name', 'venue.name']].head(10)
        # Display the date in a human readable format
        df_last_10['eventDate'] = df_last_10['eventDate'].dt.strftime('%d/%m/%Y')
        st.dataframe(df_last_10, use_container_width=True)
else:
    st.warning('No user name has been set yet. You can set it in the settings page.', icon=':material/warning:')