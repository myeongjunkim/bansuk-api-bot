# https://developers.google.com/youtube/v3/guides/implementation/videos?hl=ko

from googleapiclient.discovery import build
from datetime import datetime, timedelta


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
        return ""

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
        if '아.까.배' in title or '아까배' in title:
            return True
        return False
    
    def _is_today_video(self, video: dict) -> bool:
        published_at = video['snippet']['publishedAt']
        time_delta = datetime.now() - self._convert_date(published_at)
        if time_delta < timedelta(days=1):
            return True
        print(video['snippet']['title'])
        return False
        

    def _convert_date(self, date_str: str) -> datetime:
        utc_dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        return utc_dt + timedelta(hours=9)
        