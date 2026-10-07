import os
import sys
import requests

ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_ACCOUNT_ID = os.environ.get("INSTAGRAM_ACCOUNT_ID")

if not ACCESS_TOKEN or not INSTAGRAM_ACCOUNT_ID:
    print("❌ ERROR: Missing required GitHub Secrets!")
    print(f"-> INSTAGRAM_ACCESS_TOKEN: {'Found' if ACCESS_TOKEN else 'MISSING'}")
    print(f"-> INSTAGRAM_ACCOUNT_ID: {'Found' if INSTAGRAM_ACCOUNT_ID else 'MISSING'}")
    sys.exit(1)

def get_latest_media():
    # FIXED: Changed www.facebook.com to graph.facebook.com
    url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media?access_token={ACCESS_TOKEN}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get('data', [])
        return data[0] if data else None  # Safely returns the single most recent post
    except Exception as e:
        print(f"❌ Failed to fetch media: {e}")
        return None

def send_dm(user_id, message_text):
    # FIXED: Changed www.facebook.com to graph.facebook.com
    url = f"https://facebook.com/{ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": user_id},
        "message": {"text": message_text}
    }
    requests.post(url, json=payload)

def reply_to_public_comment(comment_id):
    # FIXED: Changed www.facebook.com to graph.facebook.com
    url = f"https://graph.facebook.com/v18.0/{comment_id}/replies"
    payload = {
        'message': "Thanks for hanging out! Check your DMs, I just sent you a message! 📥",
        'access_token': ACCESS_TOKEN
    }
    requests.post(url, data=payload)

def process_all_comments(media_id):
    # FIXED: Changed www.facebook.com to graph.facebook.com
    url = f"https://graph.facebook.com/v18.0/{media_id}/comments?fields=id,text,from&access_token={ACCESS_TOKEN}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        comments = response.json().get('data', [])
        print(f"💬 Found {len(comments)} total comments to evaluate.")
        
        for comment in comments:
            comment_id = comment.get('id')
            commenter = comment.get('from')
            
            if commenter:
                instagram_user_id = commenter.get('id')
                username = commenter.get('username', 'there')
                
                # Prevent the bot from talking to itself
                if instagram_user_id == INSTAGRAM_ACCOUNT_ID:
                    continue
                
                print(f"🚀 Processing comment from @{username}...")
                
                # 1. Post public comment reply
                reply_to_public_comment(comment_id)
                
                # 2. Fire the private engagement DM
                dm_text = f"Hey {username}! Thanks for dropping a comment on my recent post. Let's connect!"
                send_dm(instagram_user_id, dm_text)
                
    except Exception as e:
        print(f"❌ Error processing comments: {e}")

if __name__ == "__main__":
    print("🚀 Starting Instagram Blanket Engagement Bot...")
    latest_post = get_latest_media()
    if latest_post:
        print(f"📸 Target Post Found ID: {latest_post['id']}")
        process_all_comments(latest_post['id'])
    else:
        print("🤷 No recent posts found or API error occurred.")
