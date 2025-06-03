from bansuk_bot.clients.union import unionClient
# from bansuk_bot.clients.youtube import youtubeClient
from bansuk_bot.schemas import BodyBible, BodyBibleContent
import click
import requests
import json


@click.command(help="CLI for sending message to slack.")
# @click.option("--google_api_key", "-k", type=click.STRING, required=True)
# @click.option("--channel_id", "-c", type=click.STRING, required=True)
@click.option("--webhook_url", "-w", type=click.STRING, required=True)
def main(webhook_url: str) -> None:
    # youtube_client = youtubeClient(google_api_key)
    # youtube_url = youtube_client.get_today_video_from_channel(channel_id)
    union_client = unionClient()
    body_bible = union_client.fetch_body_bible()
    body_bible_content = union_client.fetch_body_bible_content()
    message = create_message(body_bible, body_bible_content)
    send_message(webhook_url, message)


def create_message(
    body_bible: BodyBible, body_bible_content: BodyBibleContent
) -> dict:
    """
    Create a Slack Block Kit formatted message for the Bible content.
    Returns a complete Slack webhook payload with blocks.
    """
    
    # Helper function to truncate text safely
    def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
    
    # Helper function to split long text into chunks
    def split_text(text: str, max_length: int = 2800) -> list:
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        while text:
            if len(text) <= max_length:
                chunks.append(text)
                break
            
            # Find a good break point (prefer sentence or line breaks)
            chunk = text[:max_length]
            break_point = chunk.rfind('\n')
            if break_point == -1:
                break_point = chunk.rfind('. ')
            if break_point == -1:
                break_point = max_length
            
            chunks.append(text[:break_point].strip())
            text = text[break_point:].strip()
        
        return chunks
    
    # Create header text (max 150 characters for plain_text header)
    header_text = f"{body_bible.date}({body_bible.week_day})\n{body_bible.title}"
    header_text = truncate_text(header_text, 150)
    
    # Format bible text with verse numbers
    bible_text = ""
    for verse in body_bible.bible_text:
        verse_num = list(verse.keys())[0]
        verse_content = list(verse.values())[0]
        bible_text += f"*{verse_num}.* {verse_content}\n\n"
    
    # Create the main blocks array
    blocks = [
        # Header with date and title
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": header_text,
                "emoji": True  # Fixed: changed from True to true (JSON boolean)
            }
        },
        
        # Bible reference
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{body_bible.bible_name} {body_bible.bible_range}*"
            }
        }
    ]
    
    # Split bible text into chunks if too long
    bible_chunks = split_text(bible_text.strip())
    for chunk in bible_chunks:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": chunk
            }
        })
    
    
    # Add divider
    blocks.append({
        "type": "divider"
    })
    
    # Content title
    content_title = truncate_text(body_bible_content.content_title, 2800)
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*💭 {content_title}*"
        }
    })
    
    # Add content sections
    for content_item in body_bible_content.content_data:
        section_title = list(content_item.keys())[0]
        section_content = list(content_item.values())[0]
        
        # Clean up HTML br tags
        clean_content = section_content.replace('<br>', '\n')
        
        # Create full section text
        full_text = f"*📌 {section_title}*\n\n{clean_content}"
        
        # Split into chunks if too long
        content_chunks = split_text(full_text)
        for chunk in content_chunks:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": chunk
                }
            })
    
    # Ensure we don't exceed 50 blocks limit
    if len(blocks) > 50:
        blocks = blocks[:49]  # Keep 49 blocks
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*... 내용이 길어 일부가 생략되었습니다.*"
            }
        })
    
    # Return complete Slack webhook payload
    return {
        "text": f"{body_bible.date}({body_bible.week_day})\n{body_bible.title}",  # Fallback text with line break
        "blocks": blocks
    }



def send_message(webhook_url: str, message: dict) -> None:
    """
    Send a Block Kit formatted message to Slack webhook.
    The message should already be in the correct format from create_message.
    """
    # Validate JSON structure
    try:
        json_str = json.dumps(message)
        print(f"✅ JSON validation passed. Size: {len(json_str)} characters")
        print(f"📊 Number of blocks: {len(message.get('blocks', []))}")
    except Exception as e:
        print(f"❌ JSON validation failed: {e}")
        return
    
    # The message is already in the correct Slack webhook format
    result = requests.post(url=webhook_url, json=message)
    print(f"Status Code: {result.status_code}")
    print(f"Response: {result.text}")

    if result.status_code != 200:
        print(f"❌ Error sending message: {result.text}")
        print("\n🔧 Try using test message:")
        print("python scripts/send_message.py -w YOUR_WEBHOOK_URL --test")
    else:
        print("✅ Message sent successfully!")




main()