# import os
# import sys
# import requests

# ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
# INSTAGRAM_ACCOUNT_ID = os.environ.get("INSTAGRAM_ACCOUNT_ID")

# if not ACCESS_TOKEN or not INSTAGRAM_ACCOUNT_ID:
#     print("❌ ERROR: Missing required GitHub Secrets!")
#     print(f"-> INSTAGRAM_ACCESS_TOKEN: {'Found' if ACCESS_TOKEN else 'MISSING'}")
#     print(f"-> INSTAGRAM_ACCOUNT_ID: {'Found' if INSTAGRAM_ACCOUNT_ID else 'MISSING'}")
#     sys.exit(1)

# def get_latest_media():
#     # FIXED: Changed www.facebook.com to graph.facebook.com
#     url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media?access_token={ACCESS_TOKEN}"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json().get('data', [])
#         return data[0] if data else None  # Safely returns the single most recent post
#     except Exception as e:
#         print(f"❌ Failed to fetch media: {e}")
#         return None

# def send_dm(user_id, message_text):
#     # FIXED: Changed www.facebook.com to graph.facebook.com
#     url = f"https://facebook.com/{ACCESS_TOKEN}"
#     payload = {
#         "recipient": {"id": user_id},
#         "message": {"text": message_text}
#     }
#     requests.post(url, json=payload)

# def reply_to_public_comment(comment_id):
#     # FIXED: Changed www.facebook.com to graph.facebook.com
#     url = f"https://graph.facebook.com/v18.0/{comment_id}/replies"
#     payload = {
#         'message': "Thanks for hanging out! Check your DMs, I just sent you a message! 📥",
#         'access_token': ACCESS_TOKEN
#     }
#     requests.post(url, data=payload)

# def process_all_comments(media_id):
#     # FIXED: Changed www.facebook.com to graph.facebook.com
#     url = f"https://graph.facebook.com/v18.0/{media_id}/comments?fields=id,text,from&access_token={ACCESS_TOKEN}"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         comments = response.json().get('data', [])
#         print(f"💬 Found {len(comments)} total comments to evaluate.")
        
#         for comment in comments:
#             comment_id = comment.get('id')
#             commenter = comment.get('from')
            
#             if commenter:
#                 instagram_user_id = commenter.get('id')
#                 username = commenter.get('username', 'there')
                
#                 # Prevent the bot from talking to itself
#                 if instagram_user_id == INSTAGRAM_ACCOUNT_ID:
#                     continue
                
#                 print(f"🚀 Processing comment from @{username}...")
                
#                 # 1. Post public comment reply
#                 reply_to_public_comment(comment_id)
                
#                 # 2. Fire the private engagement DM
#                 dm_text = f"Hey {username}! Thanks for dropping a comment on my recent post. Let's connect!"
#                 send_dm(instagram_user_id, dm_text)
                
#     except Exception as e:
#         print(f"❌ Error processing comments: {e}")

# if __name__ == "__main__":
#     print("🚀 Starting Instagram Blanket Engagement Bot...")
#     latest_post = get_latest_media()
#     if latest_post:
#         print(f"📸 Target Post Found ID: {latest_post['id']}")
#         process_all_comments(latest_post['id'])
#     else:
#         print("🤷 No recent posts found or API error occurred.")
















import os
import sys
import requests

ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_ACCOUNT_ID = os.environ.get("INSTAGRAM_ACCOUNT_ID")

if not ACCESS_TOKEN or not INSTAGRAM_ACCOUNT_ID:
    print("❌ ERROR: Missing required GitHub Secrets!")
    sys.exit(1)

def generate_local_ai_reply(username, comment_text):
    """
    Connects to the local Ollama instance running inside the 
    GitHub Action runner to query the Qwen model architecture.
    """
    print(f"🤖 Querying local Ollama server for @{username}...")
    ollama_url = "http://localhost:11434/api/generate"
    
    prompt = (
        f"You are a friendly, engaging Instagram creator. A viewer named @{username} "
        f"just left this comment on your post: '{comment_text}'. "
        f"Write a short, lively, and conversational reply to them. Use emojis naturally, "
        f"keep it under 2 sentences, and make it feel personal so they want to keep chatting. "
        f"Do not include quotes or meta-text. Just output the direct reply."
    )
    
    payload = {
        "model": "qwen2.5:1.5b",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(ollama_url, json=payload, timeout=30)
        if response.status_code == 200:
            ai_text = response.json().get("response", "").strip()
            if ai_text.startswith('"') and ai_text.endswith('"'):
                ai_text = ai_text[1:-1]
            return ai_text
    except Exception as e:
        print(f"⚠️ Local Ollama inference failed ({e}). Falling back to baseline response.")
        
    return "Thanks for hanging out! Check your DMs, I just sent you a message! 📥"

def get_latest_media():
    """
    Fetches the media feed directly. If the saved ID encounters an error, 
    the endpoint automatically pivots to a node query using 'me' mapping.
    """
    # Pipeline Endpoint A: Target specified structural mapping node
    url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media?access_token={ACCESS_TOKEN}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json().get('data', [])
            return data[0] if data else None
            
        print(f"⚠️ Endpoint A returned {response.status_code}. Pivoting to secondary network node discovery...")
    except Exception as e:
        print(f"⚠️ Endpoint A failed ({e}). Pivoting to secondary network node discovery...")

    # Pipeline Endpoint B: Hard fallback lookup using 'me' alias to prevent 400 Bad Requests
    fallback_url = f"https://graph.facebook.com/v18.0/me/media?access_token={ACCESS_TOKEN}"
    try:
        res = requests.get(fallback_url)
        res.raise_for_status()
        media_data = res.json().get('data', [])
        return media_data[0] if media_data else None
    except Exception as e:
        print(f"❌ Critical Error: All Meta endpoint discovery branches exhausted: {e}")
        return None

def send_dm(user_id, message_text):
    # FIXED: Correct Graph API v18.0 endpoint for sending Instagram DMs
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": str(user_id)},
        "message": {"text": message_text}
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"✅ DM sent successfully to {user_id}")
    except Exception as e:
        print(f"❌ Failed to send DM to {user_id}: {e}")

def reply_to_public_comment(comment_id, message_text):
    # FIXED: Added proper error handling to prevent silent failures
    url = f"https://graph.facebook.com/v18.0/{comment_id}/replies"
    payload = {
        'message': message_text,
        'access_token': ACCESS_TOKEN
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print(f"✅ Replied to comment {comment_id}")
    except Exception as e:
        print(f"❌ Failed to reply to comment {comment_id}: {e}")

def process_all_comments(media_id):
    url = f"https://graph.facebook.com/v18.0/{media_id}/comments?fields=id,text,from&access_token={ACCESS_TOKEN}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        comments = response.json().get('data', [])
        print(f"💬 Found {len(comments)} total comments to evaluate.")
        
        for comment in comments:
            comment_id = comment.get('id')
            comment_text = comment.get('text', '')
            commenter = comment.get('from')
            
            if commenter:
                instagram_user_id = commenter.get('id')
                username = commenter.get('username', 'there')
                
                # Prevent self-interaction loops (compare as strings to be type-safe)
                if str(instagram_user_id) == str(INSTAGRAM_ACCOUNT_ID):
                    continue
                
                print(f"🚀 Processing comment from @{username}...")
                
                # Fetch output directly via local Ollama background worker
                custom_ai_reply = generate_local_ai_reply(username, comment_text)
                print(f"✨ AI Reply Created: {custom_ai_reply}")
                
                # 1. Post public comment reply powered by local Qwen
                reply_to_public_comment(comment_id, custom_ai_reply)
                
                # 2. Fire the private engagement DM
                dm_text = f"Hey {username}! Thanks for dropping a comment on my recent post. Let's connect!"
                send_dm(instagram_user_id, dm_text)
                
    except Exception as e:
        print(f"❌ Error processing comments: {e}")

if __name__ == "__main__":
    print("🚀 Starting Instagram Blanket Engagement Bot (v18.0)...")
    latest_post = get_latest_media()
    if latest_post and 'id' in latest_post:
        print(f"📸 Target Post Found ID: {latest_post['id']}")
        process_all_comments(latest_post['id'])
    else:
        print("🤷 No recent posts found or API assignment failed.")
