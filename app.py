import streamlit as st
from pytube import YouTube, Playlist
from pytube.cli import on_progress
import instaloader
import os

# Helper functions for YouTube
def download_youtube_video(url, resolution):
    yt = YouTube(url, on_progress_callback=on_progress)
    stream = yt.streams.filter(res=resolution, file_extension='mp4').first()
    if stream:
        stream.download(output_path='downloads')
        return stream.default_filename
    else:
        return None

def download_youtube_audio(url):
    yt = YouTube(url, on_progress_callback=on_progress)
    stream = yt.streams.filter(only_audio=True).first()
    if stream:
        stream.download(output_path='downloads')
        return stream.default_filename
    else:
        return None

def download_youtube_playlist(url, resolution):
    pl = Playlist(url)
    filenames = []
    for video in pl.videos:
        stream = video.streams.filter(res=resolution, file_extension='mp4').first()
        if stream:
            stream.download(output_path='downloads')
            filenames.append(stream.default_filename)
    return filenames

# Helper functions for Instagram
def download_instagram_post(url):
    L = instaloader.Instaloader()
    post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
    L.download_post(post, target='downloads')
    return post.shortcode

def download_instagram_video(url):
    L = instaloader.Instaloader()
    post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
    if post.is_video:
        L.download_post(post, target='downloads')
        return post.shortcode
    else:
        return None

# Streamlit app
st.title("Video Downloader")

st.header("YouTube Downloader")
youtube_url = st.text_input("Enter YouTube URL")
if youtube_url:
    option = st.selectbox("Choose download option", ["Video", "Audio", "Playlist"])
    if option == "Video":
        resolution = st.selectbox("Choose resolution", ["360p", "480p", "720p", "1080p"])
        if st.button("Download Video"):
            filename = download_youtube_video(youtube_url, resolution)
            if filename:
                st.success(f"Video downloaded: {filename}")
            else:
                st.error("Failed to download video.")
    elif option == "Audio":
        if st.button("Download Audio"):
            filename = download_youtube_audio(youtube_url)
            if filename:
                st.success(f"Audio downloaded: {filename}")
            else:
                st.error("Failed to download audio.")
    elif option == "Playlist":
        resolution = st.selectbox("Choose resolution", ["360p", "480p", "720p", "1080p"])
        if st.button("Download Playlist"):
            filenames = download_youtube_playlist(youtube_url, resolution)
            if filenames:
                st.success(f"Playlist downloaded: {len(filenames)} videos")
            else:
                st.error("Failed to download playlist.")

st.header("Instagram Downloader")
instagram_url = st.text_input("Enter Instagram Post URL")
if instagram_url:
    option = st.selectbox("Choose download option", ["Post", "Video"])
    if option == "Post":
        if st.button("Download Post"):
            shortcode = download_instagram_post(instagram_url)
            if shortcode:
                st.success(f"Post downloaded: {shortcode}")
            else:
                st.error("Failed to download post.")
    elif option == "Video":
        if st.button("Download Video"):
            shortcode = download_instagram_video(instagram_url)
            if shortcode:
                st.success(f"Video downloaded: {shortcode}")
            else:
                st.error("Failed to download video.")

# Ensure the downloads directory exists
if not os.path.exists('downloads'):
    os.makedirs('downloads')
