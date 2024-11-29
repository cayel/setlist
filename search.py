import streamlit as st
import pandas as pd
from events.events_db import load_attended_events

st.title('Search')

df = load_attended_events('IchabodCrane')

if df.empty:
    st.warning('No event found in the database.', icon=':material/warning:')
    st.write('You can refresh the database in the administration page.')
else:
    # Add a select slider to select the date range
    current_year = pd.Timestamp.now().year
    date_range = st.slider('Select the date range:', 1980, current_year, (1980, current_year))
    # Add a multiselect to select the artists
    artists = df['artists.name'].unique()
    selected_artists = st.multiselect('Select the artists:', artists)
    # Add a multiselect to select the venues
    venues = df['venues.name'].unique()
    selected_venues = st.multiselect('Select the venues:', venues)

    # Display the events in the selected date range
    df['eventDate'] = pd.to_datetime(df['eventDate'])
    df_selected = df[(df['eventDate'].dt.year >= date_range[0]) & (df['eventDate'].dt.year <= date_range[1])]
    if selected_artists:
        df_selected = df_selected[df_selected['artists.name'].isin(selected_artists)]
    if selected_venues:
        df_selected = df_selected[df_selected['venues.name'].isin(selected_venues)]
    st.write(f'You have attended {len(df_selected)} events in the selection.')
    df['eventDate'] = pd.to_datetime(df['eventDate'])
    df_selected['eventDate'] = df_selected['eventDate'].dt.strftime('%d/%m/%Y')
    # reset the index starting from 1
    df_selected.reset_index(drop=True, inplace=True)

    st.dataframe(df_selected[['eventDate', 'artists.name', 'venues.name']], use_container_width=True, width=800)
