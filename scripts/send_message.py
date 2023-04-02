from bansuk_bot.clients.union import unionClient
from bansuk_bot.clients.youtube import youtubeClient
from bansuk_bot.schemas import BodyBible, BodyBibleContent
import click, requests


@click.command(help="CLI for sending message to slack.")
@click.option("--google_api_key", "-k", type=click.STRING, required=True)
@click.option("--playlist_id", "-p", type=click.STRING, required=True)
def main(google_api_key: str, playlist_id:str) -> None:
    youtube_client = youtubeClient(google_api_key)
    union_client = unionClient()
    youtube_url = youtube_client.get_today_vidio(playlist_id)
    body_bible = union_client.fetch_body_bible()
    body_bible_content = union_client.fetch_body_bible_content()
    message = create_message(youtube_url, body_bible, body_bible_content)
    send_message(message)


def create_message(
    youtube_url: str, body_bible: BodyBible, body_bible_content: BodyBibleContent
) -> dict[str, str]:
    bible_text = f"{body_bible.bible_name} {body_bible.bible_range}\n\n"
    for line in body_bible.bible_text:
        bible_text = bible_text + f"{list(line.keys())[0]} {list(line.values())[0]}\n"
    
    content_text = f"\" {body_bible_content.content_title} \"\n\n"
    for line in body_bible_content.content_data:
        content_text= content_text + f"*{list(line.keys())[0]}*\n\n{list(line.values())[0]}\n\n"
    content_text = content_text.replace('<br>', '\n')

    
    return {
        "date": f"{body_bible.date} ({body_bible.week_day})",
        "title": body_bible.title,
        "bible": bible_text,
        "content": content_text,
        "url": youtube_url,
    }


def send_message(message: str) -> None:
    url = "https://hooks.slack.com/services/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"
    pre_text = message["date"]+ "\n" + message["title"]
    data = {
        "attachments":[
            {
                "fallback": pre_text,
                "pretext": pre_text,
                "fields":[{
                    "title": "*본문*",
                    "value": message["bible"],
                    "short": False
                }]
            },
            {
                "fallback": "해설",
                "fields":[{
                    "title": "*해설*",
                    "value": message["content"],
                    "short": False,
                }]
            },
        ],
        "text":message["url"]
    }
    requests.post(url=url, json=data)

    


main()