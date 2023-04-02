from googleapiclient.discovery import build

class youtubeClient:
    def __init__(self, google_api_key: str) -> None:
        self.google_api_key = google_api_key
    
    def get_today_vidio(self, playlist_id) -> str:
        playlists = self._get_playlist_info(playlist_id)
        lastest_video = playlists['items'][0]
        video_id = lastest_video['snippet']['resourceId']['videoId']
        # published_at = last_video['snippet']['publishedAt']
        return f'https://youtu.be/{video_id}'

    def _get_playlist_info(self, playlist_id: str) -> dict:
        youtube = build('youtube', 'v3', developerKey=self.google_api_key)
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
        )
        response = request.execute()
        return response
    
    
