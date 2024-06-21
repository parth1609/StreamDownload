import streamlit as st
from pytube import YouTube, Playlist
from pytube.cli import on_progress
import instaloader
import os

# Ensure the downloads directory exists
DOWNLOAD_DIR = 'downloads'
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Helper functions for YouTube
def download_youtube_video(url, resolution):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        st.write(f"Available streams: {yt.streams.filter(progressive=True)}")
        stream = yt.streams.filter(progressive=True, res=resolution, file_extension='mp4').first()
        if stream:
            stream.download(output_path=DOWNLOAD_DIR)
            return stream.default_filename
        else:
            st.write(f"No progressive stream found for resolution {resolution}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def download_youtube_audio(url):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        stream = yt.streams.filter(only_audio=True).first()
        if stream:
            stream.download(output_path=DOWNLOAD_DIR)
            return stream.default_filename
        else:
            st.write("No audio stream found")
            return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def download_youtube_playlist(url, resolution):
    try:
        pl = Playlist(url)
        st.write(f"Playlist videos: {pl.video_urls}")
        filenames = []
        for video in pl.videos:
            stream = video.streams.filter(progressive=True, res=resolution, file_extension='mp4').first()
            if stream:
                stream.download(output_path=DOWNLOAD_DIR)
                filenames.append(stream.default_filename)
        return filenames
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []

# Helper functions for Instagram
def download_instagram_post(url):
    try:
        L = instaloader.Instaloader()
        post_shortcode = url.split("/")[-2]
        st.write(f"Instagram post shortcode: {post_shortcode}")
        post = instaloader.Post.from_shortcode(L.context, post_shortcode)
        L.download_post(post, target=DOWNLOAD_DIR)
        return post.shortcode
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def download_instagram_video(url):
    try:
        L = instaloader.Instaloader()
        post_shortcode = url.split("/")[-2]
        st.write(f"Instagram video shortcode: {post_shortcode}")
        post = instaloader.Post.from_shortcode(L.context, post_shortcode)
        if post.is_video:
            L.download_post(post, target=DOWNLOAD_DIR)
            return post.shortcode
        else:
            st.write("The post is not a video")
            return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit app
st.title("Video Downloader")

st.header("YouTube Video")
youtube_url = st.text_input("Enter YouTube URL")
if youtube_url:
    st.write(f"Received YouTube URL: {youtube_url}")
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

st.header("Instagram Reel")
instagram_url = st.text_input("Enter Instagram Post URL")
if instagram_url:
    st.write(f"Received Instagram URL: {instagram_url}")
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
