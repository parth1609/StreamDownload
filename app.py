import streamlit as st
from pytube import YouTube, Playlist
from pytube.cli import on_progress
import os

# Helper functions for YouTube
def download_youtube_video(url, resolution):
    yt = YouTube(url, on_progress_callback=on_progress)
    stream = yt.streams.filter(res=resolution, file_extension='mp4').first()
    if stream:
        stream.download(output_path='downloads')
        return os.path.join('downloads', stream.default_filename)
    else:
        return None

def download_youtube_audio(url):
    yt = YouTube(url, on_progress_callback=on_progress)
    stream = yt.streams.filter(only_audio=True).first()
    if stream:
        stream.download(output_path='downloads')
        return os.path.join('downloads', stream.default_filename)
    else:
        return None

def download_youtube_playlist(url, resolution):
    pl = Playlist(url)
    filenames = []
    for video in pl.videos:
        stream = video.streams.filter(res=resolution, file_extension='mp4').first()
        if stream:
            stream.download(output_path='downloads')
            filenames.append(os.path.join('downloads', stream.default_filename))
    return filenames

# Streamlit app
st.title("YouTube Downloader")

st.header("YouTube Downloader")
youtube_url = st.text_input("Enter YouTube URL")
if youtube_url:
    option = st.selectbox("Choose download option", ["Video", "Audio", "Playlist"])
    if option == "Video":
        resolution = st.selectbox("Choose resolution", ["360p", "480p", "720p", "1080p"])
        if st.button("Download Video"):
            filename = download_youtube_video(youtube_url, resolution)
            if filename:
                st.success(f"Video downloaded: {os.path.basename(filename)}")
                with open(filename, "rb") as file:
                    st.download_button(label="Download Video", data=file, file_name=os.path.basename(filename), mime="video/mp4")
            else:
                st.error("Failed to download video.")
    elif option == "Audio":
        if st.button("Download Audio"):
            filename = download_youtube_audio(youtube_url)
            if filename:
                st.success(f"Audio downloaded: {os.path.basename(filename)}")
                with open(filename, "rb") as file:
                    st.download_button(label="Download Audio", data=file, file_name=os.path.basename(filename), mime="audio/mp4")
            else:
                st.error("Failed to download audio.")
    elif option == "Playlist":
        resolution = st.selectbox("Choose resolution", ["360p", "480p", "720p", "1080p"])
        if st.button("Download Playlist"):
            filenames = download_youtube_playlist(youtube_url, resolution)
            if filenames:
                st.success(f"Playlist downloaded: {len(filenames)} videos")
                for filename in filenames:
                    with open(filename, "rb") as file:
                        st.download_button(label=f"Download {os.path.basename(filename)}", data=file, file_name=os.path.basename(filename), mime="video/mp4")
            else:
                st.error("Failed to download playlist.")

# Ensure the downloads directory exists
if not os.path.exists('downloads'):
    os.makedirs('downloads')
