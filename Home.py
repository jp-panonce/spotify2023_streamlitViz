import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(page_title="Spotify Popular Songs in 2023",page_icon="🌍",layout="wide")

st.markdown("# 🏠 HOME")

# =========== FAQ
st.markdown("## FAQs")
with st.expander("What is this web app about?"):
   st.markdown('''
   This web app was created as a practice exercise for using 'Streamlit' in Data Visualization projects.
   ''')

with st.expander("What dataset is used?"):
   st.markdown('''
   The dataset used for this web-app contains spotify data of songs that were identified as popular in 2023. To explore the data, go to "Data" menu in the sidebar menu.
   ''')

# =========== 