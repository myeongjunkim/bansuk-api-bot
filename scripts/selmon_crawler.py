from bansuk_bot.clients.youtube import youtubeClient
import json

def main():
    # 유튜브 API 키 (개인 API 키를 입력합니다.)
    api_key = "AIzaSyD3gBX0F2kE5wBkLMa7MI40bbl8TDfcOXo"
    youtube_client = youtubeClient(api_key)
    
    # '설교' 키워드를 기반으로 영상을 검색
    query = "설교"
    
    # 최대 20개의 영상 ID를 가져옵니다.
    video_ids = youtube_client.search_videos(query, max_results=20)
    sermons = []
    
    for vid in video_ids:
        transcript = youtube_client.get_transcript(vid)
        if transcript:
            sermons.append({
                "video_id": vid,
                "transcript": transcript
            })
    
    # 데이터셋 파일로 저장 (JSON 형식)
    with open("sermons.json", "w", encoding="utf-8") as f:
        json.dump(sermons, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()

    