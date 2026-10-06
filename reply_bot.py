import os
import requests

# Load secrets from environment variables
ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_ACCOUNT_ID = os.environ.get("INSTAGRAM_ACCOUNT_ID")

def get_latest_media():
    url = f"https://facebook.com{INSTAGRAM_ACCOUNT_ID}/media?access_token={ACCESS_TOKEN}"
    response = requests.get(url).json()
    return response.get('data', [])

def check_and_reply_to_comments(media_id):
    # Fetch comments for a specific post
    url = f"https://facebook.com{media_id}/comments?access_token={ACCESS_TOKEN}"
    comments = requests.get(url).json().get('data', [])
    
    for comment in comments:
        comment_id = comment.get('id')
        text = comment.get('text', '')
        
        # Simple keyword check (Example: Trigger if they ask for a link or info)
        if "info" in text.lower() or "link" in text.lower():
            reply_url = f"https://facebook.com{comment_id}/replies"
            payload = {
                'message': "Thanks for asking! Check your DMs for the details.",
                'access_token': ACCESS_TOKEN
            }
            # Post the reply comment
            requests.post(reply_url, data=payload)
            
            # Note: To send a direct message (DM) instead of a comment reply, 
            # you would use the Messenger API for Instagram components.

if __name__ == "__main__":
    media_list = get_latest_media()
    if media_list:
        # Check the most recent post
        latest_post_id = media_list[0]['id']
        check_and_reply_to_comments(latest_post_id)
