import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

from functools import reduce

st.set_page_config(page_title="Artist/Song Search",page_icon="🔍",layout="wide")
st.markdown("## ARTIST/SONG SEARCH")
# DATA_URL = r"D:\OneDrive\05_ PROJECTS\Spotify 2023 Popular Songs Web App\20230918 Spotify data web app\spotify-2023_clean.csv"
DATA_URL = Path(__file__).parents[1] / 'data/spotify-2023_clean.csv'

# @st.cache_data
def load_data():
    data = pd.read_csv(DATA_URL,encoding = 'latin1',dtype={'released_year': str})
    data["song-artist"] = data["track_name"] + " | " + data["artist(s)_name"]
    data['released_date'] = pd.to_datetime(dict(year=data.released_year, month=data.released_month, day=data.released_day))
    return data



#Load Data
raw_data = load_data()

# Get list of Unique Artists
list_artist = []
for artists in raw_data["artist(s)_name"]:
    artists_ = artists.split(",")
    list_artist.extend(artists_)
list_artist = [s.strip() for s in list_artist]
list_artist = reduce(lambda re, x: re+[x] if x not in re else re, list_artist, [])
list_artist.sort()

# Get list of Songs-Artist
list_songs = []
list_songs = raw_data["song-artist"].tolist()
list_songs = [s.strip() for s in list_songs]
list_songs = reduce(lambda re, x: re+[x] if x not in re else re, list_songs, [])

list_songs.sort()


# Create Tabs for Artist Search and Song Search
artistSearch_tab, songNameSearch_tab = st.tabs(["Artist", "Song Name"])

# Artist Search Tab
with artistSearch_tab:

    with st.expander("🔍 SEARCH ARTIST"):
        # Add text box for searching artist
        searchBar_artist = st.selectbox("Artist Name",list_artist,label_visibility="hidden",)

    # Artist Name as Header
    st.markdown("# <u>" + searchBar_artist + "</u>",unsafe_allow_html=True)

    # Create List of songs considered as popular in 2023 by selected artist
    songs_OfSearchedArtist = raw_data[raw_data['artist(s)_name'].str.contains(searchBar_artist)]

    # songs_OfSearchedArtist = songs_OfSearchedArtist.filter(['track_name', 'artist(s)_name', 'released_year','streams', "danceability_%","valence_%", "energy_%", "acousticness_%",	"instrumentalness_%","liveness_%",	"speechiness_%"],axis=1)
    songs_OfSearchedArtist["streams"] = songs_OfSearchedArtist["streams"].apply(int)
    songs_OfSearchedArtist = songs_OfSearchedArtist.sort_values('streams', ascending = False)
    songs_OfSearchedArtist.reset_index(drop=True)

    statistics_container = st.container()
    with statistics_container:
        if searchBar_artist != "":
            # Display # of songs considered popular in 2023
            col1, col2, spacer_art1, col3,col4 = st.columns([1,1,0.3,1.2,1.2])
            col1_con = col1.container()

            with col1_con:

                col1_con.markdown("## " + format(songs_OfSearchedArtist["streams"].sum(), ","))
                col1_con.caption("Total Streams from his/her Popular songs in 2023")

                col1_con.markdown("## " + str(len(songs_OfSearchedArtist)))
                col1_con.caption("Num. of Popular songs in 2023")
            
            with col2:
                st.markdown("#### Average Audio Features")
                artist_audio_features = {
                    'feature': ["Danceability","Valence","Energy", "Instrumentalness","Acousticness","Liveliness","Speechiness"],
                    'value': [
                        songs_OfSearchedArtist["danceability_%"].mean(), 
                        songs_OfSearchedArtist["valence_%"].mean(), 
                        songs_OfSearchedArtist["energy_%"].mean(), 
                        songs_OfSearchedArtist["acousticness_%"].mean(), 
                        songs_OfSearchedArtist["acousticness_%"].mean(), 
                        songs_OfSearchedArtist["liveness_%"].mean(),
                        songs_OfSearchedArtist["speechiness_%"].mean()
                    ]
                }

                df_artfeat_platform = pd.DataFrame(artist_audio_features)
                df_artfeat_platform.fillna(0)    
                df_artfeat_platform["value"] = df_artfeat_platform["value"].apply(int)
                df_artfeat_platform.sort_values(by=['value'],ascending = True)

                col2.altair_chart(alt.Chart(df_artfeat_platform).mark_bar().encode(
                    y=alt.Y('feature', sort='-y'),
                    x='value',
                ).properties(height = 250),
                use_container_width=True)

            with col3:
                st.markdown("### <u> MUSIC PLATFORMS </u>",unsafe_allow_html=True)

                spotify_container = st.container()
                apple_container = st.container()
                
                with apple_container:
                    st.markdown("### __:red[Apple Music]__")
                    apple_container_col1, apple_container_col2  = apple_container.columns([1,1])
                    

                    with apple_container_col1:
                        st.metric("Num of Playlists included",songs_OfSearchedArtist["in_apple_playlists"].sum())

                    with apple_container_col2:
                        st.metric("Rank in Chart",round(songs_OfSearchedArtist["in_apple_charts"].mean()) if songs_OfSearchedArtist["in_apple_charts"].mean() > 0 else "-")

                with spotify_container:
                    st.markdown("### _:green[Spotify]_")
                    spotify_container_col1, spotify_container_col2 = spotify_container.columns([1,1])
                    
                    with spotify_container_col1:
                        st.metric("Num of Playlists included",str(songs_OfSearchedArtist["in_spotify_playlists"].sum()))

                    with spotify_container_col2:
                        st.metric("Rank in Chart",round(songs_OfSearchedArtist["in_spotify_charts"].mean()) if songs_OfSearchedArtist["in_spotify_charts"].mean() > 0 else "-")

                with col4:
                    st.markdown("<br> <br>",unsafe_allow_html=True)
                    deezer_container = st.container()

                    with deezer_container:
                        st.markdown("### _:rainbow[Deezer]_")
                        deezer_container_col1, deezer_container_col2 = deezer_container.columns([1,1])
                        

                        with deezer_container_col1:
                            st.metric("Num of Playlists included",songs_OfSearchedArtist["in_deezer_playlists"].sum())

                        with deezer_container_col2:
                            st.metric("Rank in Chart",round(songs_OfSearchedArtist["in_deezer_charts"].mean()) if songs_OfSearchedArtist["in_deezer_charts"].mean() > 0 else "-")
                    
                
    # Display list of songs
    if searchBar_artist != "":        

        # df to display
        toDisplay_songs_OfSearchedArtist = songs_OfSearchedArtist.filter(['track_name', 'artist(s)_name', 'released_year','streams'],axis=1)

        # Calculate Max # of Streams per song
        maxSongStreams = toDisplay_songs_OfSearchedArtist["streams"].max()

        # a divider
        st.divider()


        st.markdown("#### Songs by *" + searchBar_artist + "* that were popular in 2023")

        # Display data of popular songs by selected artist
        st.dataframe(
            toDisplay_songs_OfSearchedArtist.set_index(toDisplay_songs_OfSearchedArtist.columns[0]),
            column_config= {
                "track_name": "Song Name",
                "artist(s)_name": "Artist/s",
                "streams": st.column_config.ProgressColumn(
                    "Streams",
                    help="Number of streams for said song",
                    width="large",
                    format="%d",
                    max_value= maxSongStreams
                ),
                
            }
        )


    

    pass

# Song Name Search Tab
with songNameSearch_tab:
    with st.expander("Find a Song"):
        searchBar_song_artist = st.selectbox("Song",list_songs,label_visibility="hidden")

    # Song Name
    song_name,song_artist = searchBar_song_artist.split('|')
    # hd_songName = st.header(song_name, anchor=None, help=None, divider=False)
    st.markdown("# <u>" + song_name + "</u>",unsafe_allow_html=True)
    
    # st.caption(song_artist)


    # Get Data of selected song-artist
    song_artist_data = raw_data[raw_data["song-artist"] == searchBar_song_artist]

    
    # ===== Platform Info
    col1, col2, col3, col4 = st.columns([3,0.3, 2, 2])

    with col1:
        col1_1, col1_2 = st.columns([3,4])
        with col1_1:
            st.markdown("__Artist/s__ <br> __Released__ <br>",unsafe_allow_html=True)
        with col1_2:
            st.markdown(song_artist + " <br> " + (', '.join((song_artist_data["released_date"].astype(str)))),unsafe_allow_html=True)
        
        st.metric("### Spotify Streams","  " + format(song_artist_data["streams"].sum(),","))

        col1_audioFeature_cont = col1.container()

        with col1_audioFeature_cont:
            st.divider()
            st.markdown("### <u> AUDIO FEATURES </u>",unsafe_allow_html=True)
            st.caption("this section contains audio features of the selected song")
            col1_audioFeature_col1, col1_audioFeature_spacing, col1_audioFeature_col2  = st.columns([5,0.3,1])
            
            with col1_audioFeature_col1:
                
                # Bar Chart with Audio Features
                song_audio_features = {
                    'feature': ["Danceability","Valence","Energy", "Instrumentalness","Acousticness","Liveliness","Speechiness"],
                    'value': [
                        song_artist_data["danceability_%"].mean(), 
                        song_artist_data["valence_%"].mean(), 
                        song_artist_data["energy_%"].mean(), 
                        song_artist_data["acousticness_%"].mean(), 
                        song_artist_data["acousticness_%"].mean(), 
                        song_artist_data["liveness_%"].mean(),
                        song_artist_data["speechiness_%"].mean()
                    ]

                }
                df_audfeat_platform = pd.DataFrame(song_audio_features)
                df_audfeat_platform.fillna(0)    
                df_audfeat_platform["value"] = df_audfeat_platform["value"].apply(int)
                df_audfeat_platform.sort_values(by=['value'],ascending = True)

                st.altair_chart(alt.Chart(df_audfeat_platform).mark_bar().encode(
                    y=alt.Y('feature', sort='-y'),
                    x='value',
                ).properties(height = 300),
                use_container_width=True)
                
            
            with col1_audioFeature_col2:
                
                st.metric("mode","maj" if song_artist_data.iloc[0, song_artist_data.columns.get_loc('mode')]=="Major" else "min")
                st.metric("bpm",song_artist_data.iloc[0, song_artist_data.columns.get_loc('bpm')])
                st.metric("key",song_artist_data.iloc[0, song_artist_data.columns.get_loc('key')])


    with col3:
        
        st.markdown("### <u> MUSIC PLATFORMS </u>",unsafe_allow_html=True)

        spotify_container = st.container()
        apple_container = st.container()
        
        with apple_container:
            st.markdown("### __:red[Apple Music]__")
            apple_container_col1, apple_container_col2  = apple_container.columns([1,1])
            

            with apple_container_col1:
                st.metric("Num of Playlists included",song_artist_data["in_apple_playlists"].sum())

            with apple_container_col2:
                st.metric("Rank in Chart",str(round(song_artist_data["in_apple_charts"].mean())) if song_artist_data["in_apple_charts"].mean() > 0 else "-")

        with spotify_container:
            st.markdown("### _:green[Spotify]_")
            spotify_container_col1, spotify_container_col2 = spotify_container.columns([1,1])
            
            with spotify_container_col1:
                st.metric("Num of Playlists included",str(song_artist_data["in_spotify_playlists"].sum()))

            with spotify_container_col2:
                st.metric("Rank in Chart",round(song_artist_data["in_spotify_charts"].mean()) if song_artist_data["in_spotify_charts"].mean() > 0 else "-")


    with col4:
        st.markdown("<br> <br>",unsafe_allow_html=True)
        deezer_container = st.container()

        with deezer_container:
            st.markdown("### _:rainbow[Deezer]_")
            deezer_container_col1, deezer_container_col2 = deezer_container.columns([1,1])
            

            with deezer_container_col1:
                st.metric("Num of Playlists included",song_artist_data["in_deezer_playlists"].sum())

            with deezer_container_col2:
                st.metric("Rank in Chart",round(song_artist_data["in_deezer_charts"].mean()) if song_artist_data["in_deezer_charts"].mean() > 0 else "-")

    pass