import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path


st.set_page_config(page_title="DATA",page_icon="📊",layout="wide")

DATE_COLUMN = 'date/time'
# DATA_URL = r"D:\OneDrive\05_ PROJECTS\Spotify 2023 Popular Songs Web App\20230918 Spotify data web app\spotify-2023_clean.csv"
DATA_URL = Path(__file__).parents[1] / 'data/spotify-2023_clean.csv'

audio_features_def = {
    'field':["Acousticness","Danceability","Energy","Instrumentalness","Liveness","Speechiness","Tempo","Valence"],
    'Definition':[                  
        "A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.",
        "Describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.",
        "Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy.",
        "Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal.” The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.",
        "Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.",
        "Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.",
        "The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.",
        "A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry)."
    ]
}


# @st.cache_data
def load_data():
    data = pd.read_csv(DATA_URL,encoding = "ISO-8859-1")

    return data

data = load_data()

st.markdown("## DATASET")

with st.expander("LOOK AT DATA"):
    st.markdown("2023 SPOTIFY POPULAR SONGS")
    st.dataframe(data,height = 700,use_container_width =True, hide_index = True)

st.divider()
st.markdown("## ABOUT THE DATA")
st.markdown("### Audio Features")

st.table(pd.DataFrame.from_dict(audio_features_def))