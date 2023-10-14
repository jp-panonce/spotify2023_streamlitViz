import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

from functools import reduce
from PIL import Image
from pathlib import Path



# st.title("Search", anchor=None, help="Search your favorite song and see if it's popular this year (2023)")
st.set_page_config(page_title="Dashboard",page_icon="📊",layout="wide")
# DATA_URL = r"D:\OneDrive\05_ PROJECTS\Spotify 2023 Popular Songs Web App\20230918 Spotify data web app\spotify-2023_clean.csv"
DATA_URL = Path(__file__).parents[1] / 'data/spotify-2023_clean.csv'


# @st.cache_data
def load_data():
    data = pd.read_csv(DATA_URL,encoding = 'latin1', dtype={'key':str})
    data['released_date'] = pd.to_datetime(dict(year=data.released_year, month=data.released_month, day=data.released_day))
    
    #Clean Deezer Playlist 
    data['in_deezer_playlists'] = data['in_deezer_playlists'].str.replace(',','').astype(int)
    data["in_deezer_playlists"] = data["in_deezer_playlists"]
    return data

audio_features_def = {
    "Acousticness":"A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.",
    "Danceability" : " Describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.",
    "Energy":" Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy.",
    "Instrumentalness":" Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal.” The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.",
    "Liveness":" Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.",
    "Speechiness":" Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.",
    "Tempo":" The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.",
    "Valence":" A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry)."
}

# ========== Load Data
# Raw Data
raw_data = load_data()

# Get list of Unique Artists
list_artist = []
for artists in raw_data["artist(s)_name"]:
    artists_ = artists.split(",")
    list_artist.extend(artists_)
list_artist = [s.strip() for s in list_artist]
list_artist = reduce(lambda re, x: re+[x] if x not in re else re, list_artist, [])
list_artist.sort()

relYear_min = (raw_data.released_date.min()).to_pydatetime()
relYear_max = (raw_data.released_date.max()).to_pydatetime()


# ++++++++++++++++++++++++ UI ++++++++++++++++++++++++++++++++++++++++++
# Title
st.title("Popular Songs in 2023 | Spotify")

# ========== Input Controls
with st.expander("FILTERS"):

    # Multiselect box for Artist
    with st.container():

        filter_cont1_col1, filter_cont1_space1, filter_cont1_col2, ph1= st.columns([1,0.05,1,0.1])

        with filter_cont1_col1:
            mselect_artist = st.multiselect("Select Contributing Artist",list_artist,placeholder ="All Artists")
        with filter_cont1_col2:
            slider_relYear_start, slider_relYear_end = st.slider("Select Released Date",relYear_min,relYear_max,(relYear_min,relYear_max))
    
    with st.container():

        st.markdown("##### Audio Features")
        fc2_mar1, filter_cont2_col1, fc2_pc1, filter_cont2_col2, fc2_pc2, filter_cont2_col3, fc2_pc3, filter_cont2_col4, fc2_mar2 = st.columns([0.1,1,0.2,1,0.2,1,0.2,1,0.2])

        with filter_cont2_col1:
            # Slider for Music Key
            raw_data["key"] = raw_data["key"].apply(str)
            list_musicKey = raw_data.key.unique().tolist()
            # list_musicKey.remove('nan')
            list_musicKey.sort()
            multSelect_key = st.multiselect("Key",list_musicKey,list_musicKey,placeholder="All")
            include_noKey = st.checkbox("Include no keys?")

            # Slider for Acousticness
            acous_start, acous_end = st.slider("Acousticness (%)",0,100,(0,100))
            include_acous = st.checkbox("Consider Acousticness")
            
        with filter_cont2_col2:

            # Slider for Danceability
            danc_start, danc_end = st.slider("Danceability (%)",0,100,(0,100))
            include_danc = st.checkbox("Consider Danceability")

            # Slider for Speechiness
            spch_start, spch_end = st.slider("Speechiness (%)",0,100,(0,100))
            include_spch = st.checkbox("Consider Speechiness")

        with filter_cont2_col3:
            # Slider for Valence
            val_start, val_end = st.slider("Consider Valence",0,100,(0,100))
            include_val = st.checkbox("Consider Valence")

            # Slider for Liveliness
            liv_start, liv_end = st.slider("Liveliness (%)",0,100,(0,100))
            include_liv = st.checkbox("Consider Liveliness")

        with filter_cont2_col4:
            # Slider for Energy
            ener_start, ener_end = st.slider("Energy (%)",0,100,(0,100))
            include_ener = st.checkbox("Consider Energy")

            # Slider for Instrumentalness
            instr_start, instr_end = st.slider("Instrumentalness (%)",0,100,(0,100))
            include_instr = st.checkbox("Consider Instrumentalness")

# =========== FILTER DATA TO SHOW ACCORDING TO FILTERS SET BY USER
dataToShow = raw_data[
    (raw_data["released_date"] >= slider_relYear_start) & 
    (raw_data["released_date"] <= slider_relYear_end)
]
if mselect_artist:
    dataToShow = dataToShow[dataToShow['artist(s)_name'].str.contains('|'.join(mselect_artist))]

# If those with no key is to be exlude, filter them out
if not(include_noKey):
    dataToShow = dataToShow[dataToShow['key'] != "nan"]
    pass

# Filter keys
if bool(multSelect_key):
    dataToShow = dataToShow[dataToShow['key'].isin(multSelect_key)]

# Filter acousticness
if include_acous:
    dataToShow = raw_data[
        (raw_data["acousticness_%"] >= acous_start) & 
        (raw_data["acousticness_%"] <= acous_end)
    ]

if include_danc:
    dataToShow = raw_data[
        (raw_data["danceability_%"] >= danc_start) & 
        (raw_data["danceability_%"] <= danc_end)
    ]

if include_spch:
    dataToShow = raw_data[
        (raw_data["speechiness_%"] >= spch_start) & 
        (raw_data["speechiness_%"] <= spch_end)
    ]

if include_val:
    dataToShow = raw_data[
        (raw_data["valence_%"] >= val_start) & 
        (raw_data["valence_%"] <= val_end)
    ]

if include_liv:
    dataToShow = raw_data[
        (raw_data["liveness_%"] >= liv_start) & 
        (raw_data["liveness_%"] <= liv_end)
    ]

if include_ener:
    dataToShow = raw_data[
        (raw_data["energy_%"] >= ener_start) & 
        (raw_data["energy_%"] <= ener_end)
    ]

if include_instr:
    dataToShow = raw_data[
        (raw_data["instrumentalness_%"] >= instr_start) & 
        (raw_data["instrumentalness_%"] <= instr_end)
    ]


# ============= Metrics
# st.divider()
metrics_container = st.container()
with metrics_container:
    metrics_container_col1,metrics_container_col2, metrics_container_col3 = st.columns(3)
    
    metrics_container_col1.metric("Number of Songs","🎶" + str(len(dataToShow.index)))
    metrics_container_col2.metric("Contributing Artists","👨‍🎤" + str(len(list(set((",".join(dataToShow['artist(s)_name'])).split(","))))))
    metrics_container_col3.metric("Total Streams","⏯" + format(dataToShow['streams'].sum(),","))

# ============= Charts

if not(dataToShow.empty):
    st.divider()
    st.markdown("### 🎉 WHICH SONGS ARE POPULAR?")
    st.caption("this section contains visualizations of the top popular songs")
    songsDash_container = st.container()
    with songsDash_container:

        songsDash_container_col1, songsDash_container_col2 = st.columns([1,1])

        with songsDash_container_col1:

            # Popuular Tracks (by Streams) (Spotify)
            st.markdown("#### ▶ by Streams (Spotify)")
            top_spotify_streams = dataToShow[['track_name', 'artist(s)_name', 'streams']].sort_values(by='streams', ascending=False).head(10)
            st.altair_chart(alt.Chart(top_spotify_streams).mark_bar().encode(
                    y=alt.Y('track_name', sort='-x'),
                    x='streams',
                ).properties(height=700),
                use_container_width=True
            )
        
        with songsDash_container_col2:
            # Popular Tracks (by Addition to Playlists)

            # Spotify Playlists Addition
            st.markdown("#### ⏯ by Playlist Additions")
            st.markdown("__:green[Spotify]__")
            top_spotify_streams = dataToShow[['track_name', 'artist(s)_name', 'in_spotify_playlists']].sort_values(by='in_spotify_playlists', ascending=False).head(5)
            st.altair_chart(alt.Chart(top_spotify_streams).mark_bar().encode(
                    y=alt.Y('track_name', sort='-x'),
                    x='in_spotify_playlists',
                ).properties(height=200),
                use_container_width=True
            )

            # Apple Playlists Addition
            st.markdown("__:red[Apple Music]__")
            top_spotify_streams = dataToShow[['track_name', 'artist(s)_name', 'in_apple_playlists']].sort_values(by='in_apple_playlists', ascending=False).head(5)
            st.altair_chart(alt.Chart(top_spotify_streams).mark_bar().encode(
                    y=alt.Y('track_name', sort='-x'),
                    x='in_apple_playlists',
                ).properties(height=200),
                use_container_width=True
            )

            # Deezer Playlists Addition
            st.markdown("__:rainbow[Deezer]__")
            top_spotify_streams = dataToShow[['track_name', 'artist(s)_name', 'in_deezer_playlists']].sort_values(by='in_deezer_playlists', ascending=False).head(5)
            st.altair_chart(alt.Chart(top_spotify_streams).mark_bar().encode(
                    y=alt.Y('track_name', sort='-x'),
                    x='in_deezer_playlists',
                ).properties(height=200),
                use_container_width=True
            )
        
    st.divider()
    st.markdown("### 👩‍🎤 WHO ARE THE ARTISTS BEHIND THESE POPULAR SONGS?")
    st.caption("this section shows the ranking of artists according to their popular songs")
    with st.container():

        art_container_col1,art_container_col2,art_container_col3 = st.columns([1,0.1,1])

        with art_container_col1:
            
            # Popular Artists by # of Songs (Top 10 artists with most songs popular in 2023)
            st.markdown("#### #️⃣ by Count of Popular songs")
            exploded_df = dataToShow.explode('artist(s)_name')
            artist_counts = exploded_df['artist(s)_name'].value_counts().reset_index()
            artist_counts.columns = ['artist_name', 'track_count']

            top_artists = artist_counts.head(10)
            st.altair_chart(alt.Chart(top_artists).mark_bar().encode(
                    y=alt.Y('artist_name', sort='-x'),
                    x='track_count',
                ).properties(height=500),
                use_container_width=True
            )

        with art_container_col3:
            # Popular Artists by Streams (Top 10 artists with most songs popular in 2023)
            st.markdown("#### #️⃣ by Num. of Total streams")
            exploded_df = dataToShow.explode('artist(s)_name')
            artist_stream_counts = exploded_df.groupby('artist(s)_name')['streams'].sum().reset_index()
            artist_stream_counts.columns = ['artist_name', 'streaming_count']
            top_artists_streams = artist_stream_counts.sort_values(by='streaming_count', ascending=False).head(10)
            st.altair_chart(alt.Chart(top_artists_streams).mark_bar().encode(
                    y=alt.Y('artist_name', sort='-x'),
                    x='streaming_count',
                ).properties(height=500),
                use_container_width=True
            )

        
    st.divider()
    st.markdown("### 👴 HOW OLD ARE THESE SONGS?")
    
    with st.container():
        st.caption("this section shows how even the old songs still persist and become popular this year")
        st.markdown("#### 📅 by year")
        release_year_counts = dataToShow['released_year'].value_counts().sort_index()
        release_year_counts = pd.DataFrame({'year':release_year_counts.index, 'count':release_year_counts.values})
        release_year_counts['year'] = release_year_counts['year'].apply(str)

        with st.container():
            old_songs_col1, ph2, old_songs_col2 = st.columns([2,0.2,1])

            
            with old_songs_col2:

                released_year_to_show_data = st.selectbox("Select Released Year to view Songs",sorted(dataToShow['released_year'].unique()))
                list_of_songs_on_selected_year = dataToShow[dataToShow['released_year'] == released_year_to_show_data]
                list_of_songs_on_selected_year = list_of_songs_on_selected_year[['track_name','artist(s)_name','released_date']]
                list_of_songs_on_selected_year['released_date'] = list_of_songs_on_selected_year['released_date'].dt.strftime('%Y-%b-%d')

                st.dataframe(list_of_songs_on_selected_year,use_container_width=True,hide_index = True,height=200)
            
            with old_songs_col1:
                # st.bar_chart(release_year_counts)
                st.altair_chart(alt.Chart(release_year_counts).mark_bar().encode(
                    x='year',
                    y='count',
                    color=alt.condition(
                        alt.datum.year == str(released_year_to_show_data),  # If the rating is 80 it returns True,
                        alt.value('red'),
                        alt.value('steelblue')
                    )
                ),use_container_width=True)

        st.markdown("#### 📅 by decade")
        dataToShow['released_decade'] = ((dataToShow['released_year']//10)).astype(str) + "0s"
        release_decade_counts = dataToShow['released_decade'].value_counts().sort_index()
        st.bar_chart(release_decade_counts)

    st.divider()
    st.markdown("### 😲 WHAT COULD'VE MADE THEM POPULAR?")
    st.caption("this section shows some possible factors that contribute to the songs being popular")
    with st.container():
        
        pop_analysis_col1, pop_analysis_col2 = st.columns(2)

        with pop_analysis_col1:
            # Percentage of Collaborated Songs vs Solo
            st.markdown("#### 😶solo vs collaboration 🤼‍♂️")
            colabVsSolo = pd.DataFrame({"category": ["Collaboration","Solo"], "count":[len(dataToShow[dataToShow['artist_count'] <= 1]), len(dataToShow[dataToShow['artist_count'] > 1])]})
            st.altair_chart(alt.Chart(colabVsSolo).mark_arc().encode(
                theta="count",
                color="category"
            ))

            st.markdown("#### Music Key")
            key_counts = dataToShow['key'].value_counts().sort_index()
            st.bar_chart(key_counts)


        # By Key
        with pop_analysis_col2:
            # ------ AUDIO FEATURES vs Streams
            st.markdown("#### 🎙Streams vs Audio Features")
            columns_to_plot = ['bpm', 'danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%']

            fig, axes = plt.subplots(4, 2, figsize=(20, 30))
            axes = axes.flatten()
            for i, column in enumerate(columns_to_plot):
                plt.sca(axes[i])
                plt.bar(dataToShow[column], dataToShow['streams'], color='blue')
                plt.xlabel(column, fontsize=12)
                plt.ylabel('Streams', fontsize=12)
                plt.title(f'Streams vs. {column}', fontsize=14)
                plt.grid(axis='y')
            plt.tight_layout()
            st.pyplot(plt)



    
else:
    st.info('No songs fit the criteria set by your filters.', icon="😑")


st.divider()
st.markdown("### SHOW APPLICABLE DATA")
st.caption("The table below shows the dataset after filters by user has been applied")
st.dataframe(dataToShow)