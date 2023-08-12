from pytube import YouTube, Playlist, Channel, exceptions
from pytube.cli import on_progress
from youtubedownloader import downloadoptions
from youtubeuploader import upload_to_youtube, playlists_of_channel
import os


def update_playlist(playlist_url, saved_playlist_url):
    playlist = Playlist(playlist_url)
    saved_playlist = Playlist(saved_playlist_url)
    for index, video in enumerate(playlist.videos):
        video = YouTube(video.watch_url, use_oauth=True, allow_oauth_cache=True)
        saved = False
        try:
            print(video.title, end='')
        except exceptions.VideoUnavailable:
            print(f"Video number {index}: {video.watch_url} is unavailable, check if it\'s in a saved playlist")
            continue
        for saved_video in saved_playlist.videos:
            saved_video = YouTube(saved_video.watch_url, use_oauth=True, allow_oauth_cache=True)
            if video.title == saved_video.title and video.length == saved_video.length:
                saved = True
                break
        if not saved:
            print(f" is missing")
            print(f"Saving...")
            downloadoptions(video.watch_url, os.getcwd(), 'best video')
            filename = video.streams.first().default_filename[:video.streams.first().default_filename.index('.')] + '.mp4'
            upload_to_youtube(f'{os.getcwd()}\\{filename}', saved_playlist.title)
            os.remove(f'{os.getcwd()}\\{filename}')
        else:
            print(f" is present")


if __name__ == "__main__":
    # pytube version 12.0.0 required (pip install --force-reinstall pytube==12.0.0)
    channel = "https://www.youtube.com/@channel"
    playlists_url = playlists_of_channel(channel)
    saved_channel = "https://www.youtube.com/@channelsave"
    saved_playlists_url = playlists_of_channel(saved_channel)
    for playlist_url in playlists_url:
        playlist = Playlist(playlist_url)
        for saved_playlist_url in saved_playlists_url:
            saved_playlist = Playlist(saved_playlist_url)
            if playlist.title == saved_playlist.title:
                update_playlist(playlist_url, saved_playlist_url)
