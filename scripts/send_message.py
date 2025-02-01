from bansuk_bot.clients.union import unionClient
# from bansuk_bot.clients.youtube import youtubeClient
from bansuk_bot.schemas import BodyBible, BodyBibleContent
import click
import requests


@click.command(help="CLI for sending message to slack.")
# @click.option("--google_api_key", "-k", type=click.STRING, required=True)
# @click.option("--channel_id", "-c", type=click.STRING, required=True)
@click.option("--webhook_url", "-w", type=click.STRING, required=True)
def main(webhook_url:str) -> None:
    # youtube_client = youtubeClient(google_api_key)
    # youtube_url = youtube_client.get_today_video_from_channel(channel_id)
    union_client = unionClient()
    body_bible = union_client.fetch_body_bible()
    body_bible_content = union_client.fetch_body_bible_content()
    message = create_message(body_bible, body_bible_content)
    send_message(webhook_url,message)


def create_message(
    body_bible: BodyBible, body_bible_content: BodyBibleContent
) -> dict[str, str]:
    bible_text = f"{body_bible.bible_name} {body_bible.bible_range}\n\n"
    for line in body_bible.bible_text:
        bible_text = bible_text + f"{list(line.keys())[0]}. {list(line.values())[0]}\n\n"
    
    content_text = f"\" {body_bible_content.content_title} \"\n\n"
    for line in body_bible_content.content_data:
        content_text= content_text + f"*📌 {list(line.keys())[0]}*\n\n{list(line.values())[0]}\n"
    content_text = content_text.replace('<br>', '\n')

    
    return {
        "date": f"{body_bible.date}({body_bible.week_day})",
        "title": body_bible.title,
        "bible": bible_text,
        "content": content_text,
        # "url": youtube_url,
    }


def send_message(webhook_url: str, message: dict[str, str]) -> None:
    data = {
        "text": message["date"]+ "\n" + message["title"],
        "attachments":[
            {
                "fields":[{
                    "title": "*본문*",
                    "value": message["bible"],
                    "short": False
                }]
            },
            {
                "fields":[{
                    "title": "*해설*",
                    "value": message["content"],
                    "short": False,
                }]
            },
        ],
    }
    result = requests.post(url=webhook_url, json=data)
    print(result.text)




main()