import streamlit as st
import pandas as pd
from events.events_db import load_attended_events

st.title('Statistics')

df = load_attended_events('IchabodCrane')

if df.empty:
    st.warning('No event found in the database.', icon=':material/warning:')
    st.write('You can refresh the database in the administration page.')
else:
    st.write(f'You have attended {len(df)} events.')

    # Concerts per year
    df['eventDate'] = pd.to_datetime(df['eventDate'])
    df['year'] = df['eventDate'].dt.year
    concerts_per_year = df['year'].value_counts().sort_index()
    # Display chart
    st.subheader('Concerts per year')
    st.bar_chart(concerts_per_year)

    # Concerts per month
    df['month'] = df['eventDate'].dt.month
    concerts_per_month = df['month'].value_counts().sort_index()
    # Display chart
    st.subheader('Concerts per month')
    st.bar_chart(concerts_per_month, use_container_width=True)

    # Calculate the number of events per venue
    venues = df['venues.name'].value_counts()
    # Add a line other for all the venue with less than 5 events
    venues['Other'] = venues[venues < 5].sum()
    venues = venues[venues >= 5]
    # Display chart
    st.subheader('Number of events per venue')
    st.dataframe(venues, use_container_width=True)

