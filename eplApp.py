import streamlit as st
import pandas as pd
import numpy as np

st.title('English Premier League Standings')

@st.cache
def load_data():
    data = pd.read_csv("eplFullStandings.csv")
    return data

def load_games():
    data = pd.read_csv("eplMatchweek.csv")
    return data

df = load_data()
df_2 = load_games()
# subset_df = df.loc[lambda d: d['Team'].isin(teams)]
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

# Display a static table

if st.sidebar.checkbox("Show EPL Table"):
    st.table(df)

if st.sidebar.checkbox("Show Upcoming Match Schedule"):
    st.table(df_2)

st.markdown('Table updates every Tuesday at 5AM EST')