from googleapiclient.discovery import build

class youtubeClient:
    def __init__(self, google_api_key: str, playlist_id: str) -> None:
        self.google_api_key = google_api_key
        self.playlist_id = playlist_id
    
    def get_today_vidio(self) -> str:
        playlists = self._get_playlist_info()
        lastest_video = playlists['items'][0]
        video_id = lastest_video['snippet']['resourceId']['videoId']
        # published_at = last_video['snippet']['publishedAt']
        return f'https://youtu.be/{video_id}'

    def _get_playlist_info(self) -> dict:
        youtube = build('youtube', 'v3', developerKey=self.google_api_key)
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=self.playlist_id,
        )
        response = request.execute()
        return response
    
    

