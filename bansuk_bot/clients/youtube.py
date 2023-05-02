# https://developers.google.com/youtube/v3/guides/implementation/videos?hl=ko

from googleapiclient.discovery import build
import re
from datetime import datetime

class youtubeClient:
    def __init__(self, google_api_key: str) -> None:
        self.google_api_key = google_api_key
    
    def get_today_video_from_playlist(self, playlist_id: str) -> str:
        videos = self._fetch_playlist_videos(playlist_id)['items']
        lastest_video = videos[0]
        video_id = lastest_video['snippet']['resourceId']['videoId']
        return f'https://youtu.be/{video_id}'
    
    def get_today_video_from_channel(self, channel_id: str) -> str:
        videos = self._fetch_channel_videos(channel_id)['items']
        for video in videos:
            if not self._is_akkabae_video(video):
                continue
            if not self._is_today_video(video):
                continue
            video_id = video['id']['videoId']
            return f'https://youtu.be/{video_id}'
        return None

    def _fetch_playlist_videos(self, playlist_id: str) -> dict:
        youtube = build('youtube', 'v3', developerKey=self.google_api_key)
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
        )
        response = request.execute()
        return response
    
    
    def _fetch_channel_videos(self, channel_id:str) -> dict:
        youtube = build('youtube', 'v3', developerKey=self.google_api_key)
        videos = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            maxResults=10,
            order='date',
        ).execute()

        return videos
    
    def _is_akkabae_video(self, video: dict) -> bool:
        title = video['snippet']['title']
        if '아.까.배' in title:
            return True
        return False
    
    def _is_today_video(self, video: dict) -> bool:
        description = video['snippet']['description']
        date_info = re.search(r'\d{4}년 \d+월 \d+일', description)
        if not date_info:
            return False
        date_info = date_info.group()
        date_obj = datetime.strptime(date_info, '%Y년 %m월 %d일')
        if date_obj.date() == datetime.today().date():
            return True
        return False
        
