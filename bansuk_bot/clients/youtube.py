# https://developers.google.com/youtube/v3/guides/implementation/videos?hl=ko

import re

from googleapiclient.discovery import build
from datetime import datetime, timedelta
from youtube_transcript_api import YouTubeTranscriptApi


class youtubeClient:
    def __init__(self, google_api_key: str) -> None:
        self.google_api_key = google_api_key
    
    def get_union_video_url_from_channel(self, channel_id: str, date: datetime) -> str:
        videos = self._fetch_channel_videos(channel_id)['items']
        # 성서유니온 설명의 날짜 형식이 "2026. 6. 8. 월요일"(마침표) 또는
        # "2026. 6. 8 월요일"(공백)로 혼재한다. 날짜 뒤에 마침표/공백이 오는
        # 경우만 매칭해 "6. 1"이 "6. 15"에 잘못 매칭되는 것을 방지한다.
        date_pattern = re.escape(f"{date.year}. {date.month}. {date.day}") + r"[.\s]"
        for video in videos:
            if "매일성경" not in video['snippet']['title']:
                continue
            if not re.search(date_pattern, video['snippet']['description']):
                continue
            video_id = video['id']['videoId']
            return f'https://youtu.be/{video_id}'
        return ""

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
        
    def search_videos(self, query: str, max_results: int = 10) -> list:
        """검색어로 동영상을 검색하고 ID 목록을 반환합니다."""
        youtube = build('youtube', 'v3', developerKey=self.google_api_key)
        search_response = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=max_results,
            type='video',
            videoCaption='closedCaption'
        ).execute()
        
        return [item['id']['videoId'] for item in search_response.get('items', [])]

    def get_transcript(self, video_id: str) -> str:
        """동영상의 자막을 가져옵니다."""
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko','en'])
            return " ".join([t['text'] for t in transcript_list])
        except Exception as e:
            print(f"Error fetching transcript for video {video_id}: {e}")
            return None
        