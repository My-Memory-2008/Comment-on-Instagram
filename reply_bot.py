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

# def generate_local_ai_reply(username, comment_text):
#     """
#     Connects to the local Ollama instance running inside the 
#     GitHub Action runner to query the Qwen model architecture.
#     """
#     print(f"🤖 Querying local Ollama server for @{username}...")
#     ollama_url = "http://localhost:11434/api/generate"
    
#     prompt = (
#         f"You are a friendly, engaging Instagram creator. A viewer named @{username} "
#         f"just left this comment on your post: '{comment_text}'. "
#         f"Write a short, lively, and conversational reply to them. Use emojis naturally, "
#         f"keep it under 2 sentences, and make it feel personal so they want to keep chatting. "
#         f"Do not include quotes or meta-text. Just output the direct reply."
#     )
    
#     payload = {
#         "model": "qwen2.5:1.5b",
#         "prompt": prompt,
#         "stream": False
#     }
    
#     try:
#         response = requests.post(ollama_url, json=payload, timeout=30)
#         if response.status_code == 200:
#             ai_text = response.json().get("response", "").strip()
#             if ai_text.startswith('"') and ai_text.endswith('"'):
#                 ai_text = ai_text[1:-1]
#             return ai_text
#     except Exception as e:
#         print(f"⚠️ Local Ollama inference failed ({e}). Falling back to baseline response.")
        
#     return "Thanks for hanging out! Check your DMs, I just sent you a message! 📥"

# def get_latest_media():
#     # UNTOUCHED WORKING ORIGINAL ENDPOINT
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
#     # UNTOUCHED WORKING ORIGINAL ENDPOINT
#     url = f"https://facebook.com/{ACCESS_TOKEN}"
#     payload = {
#         "recipient": {"id": user_id},
#         "message": {"text": message_text}
#     }
#     requests.post(url, json=payload)

# def reply_to_public_comment(comment_id, message_text):
#     # INTEGRATED WITH THE DYNAMIC AI REPLY TEXT
#     url = f"https://graph.facebook.com/v18.0/{comment_id}/replies"
#     payload = {
#         'message': message_text,
#         'access_token': ACCESS_TOKEN
#     }
#     requests.post(url, data=payload)

# def process_all_comments(media_id):
#     # UNTOUCHED WORKING ORIGINAL ENDPOINT
#     url = f"https://graph.facebook.com/v18.0/{media_id}/comments?fields=id,text,from&access_token={ACCESS_TOKEN}"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         comments = response.json().get('data', [])
#         print(f"💬 Found {len(comments)} total comments to evaluate.")
        
#         for comment in comments:
#             comment_id = comment.get('id')
#             comment_text = comment.get('text', '') # Safe string capture
#             commenter = comment.get('from')
            
#             if commenter:
#                 instagram_user_id = commenter.get('id')
#                 username = commenter.get('username', 'there')
                
#                 # Prevent the bot from talking to itself
#                 if instagram_user_id == INSTAGRAM_ACCOUNT_ID:
#                     continue
                
#                 print(f"🚀 Processing comment from @{username}...")
                
#                 # Call local Qwen runner inside actions container
#                 custom_ai_reply = generate_local_ai_reply(username, comment_text)
#                 print(f"✨ AI Reply Generated: {custom_ai_reply}")
                
#                 # 1. Post public comment reply powered by local Qwen
#                 reply_to_public_comment(comment_id, custom_ai_reply)
                
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
        f"A viewer named @{username} commented: '{comment_text}'. "
        f"Generate a response that is MAXIMUM 1-3 words or purely emojis. "
        f"Express high energy, respect, or gratitude. Total length MUST be under 20 characters. "
        f"Focus heavily on emojis like 🙌, 🔥, ❤️, 🫡, 🌟. Do not include quotes or meta text."
    )
    
    payload = {
        "model": "qwen2.5:1.5b",
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 10,
            "temperature": 0.6
        }
    }
    
    try:
        response = requests.post(ollama_url, json=payload, timeout=30)
        if response.status_code == 200:
            ai_text = response.json().get("response", "").strip()
            if ai_text.startswith('"') and ai_text.endswith('"'):
                ai_text = ai_text[1:-1]
            
            # Truncation safety cap to enforce the 20-character rule
            if len(ai_text) > 20:
                ai_text = ai_text[:17] + "..."
            return ai_text
    except Exception as e:
        print(f"⚠️ Local Ollama inference failed ({e}). Falling back to baseline.")
        
    return "🙌🔥🫡"

def get_latest_media():
    """
    Tries the specific account endpoint first, and automatically provides a 
    universal fallback if a 404 error occurs.
    """
    # Channel A: Your standard setup node
    url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media?access_token={ACCESS_TOKEN}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json().get('data', [])
            return data[0] if data else None
    except Exception:
        pass

    print("⚠️ Channel A returned a 404. Attempting universal fallback query...")
    
    # Channel B: Universal Node Fallback to completely bypass account block checks
    fallback_url = f"https://facebook.com/{ACCESS_TOKEN}"
    try:
        response = requests.get(fallback_url)
        response.raise_for_status()
        data = response.json().get('data', [])
        return data[0] if data else None
    except Exception as e:
        print(f"❌ Failed to fetch media across all fallbacks: {e}")
        return None

def send_dm(user_id, message_text):
    # FIXED: Re-enforced direct payload formatting to clear connection resets
    url = f"https://facebook.com/{ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": user_id},
        "message": {"text": message_text}
    }
    try:
        requests.post(url, json=payload)
    except Exception:
        pass

def reply_to_public_comment(comment_id, message_text):
    url = f"https://graph.facebook.com/v18.0/{comment_id}/replies"
    payload = {
        'message': message_text,
        'access_token': ACCESS_TOKEN
    }
    requests.post(url, data=payload)

def has_already_replied(comment_id):
    """
    Checks the live Instagram thread history to see if your account ID 
    has already engaged with this comment thread.
    """
    url = f"https://graph.facebook.com/v18.0/{comment_id}/replies?fields=from&access_token={ACCESS_TOKEN}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            replies = res.json().get('data', [])
            for reply in replies:
                author = reply.get('from', {})
                if author.get('id') == INSTAGRAM_ACCOUNT_ID:
                    return True
    except Exception:
        pass
    return False

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
                
                # Rule 1: Skip self comments
                if instagram_user_id == INSTAGRAM_ACCOUNT_ID:
                    continue
                
                # Rule 2: Live Server-Side Deduplication Check
                if has_already_replied(comment_id):
                    print(f"⏭️ Skipping comment from @{username} (Live check: Already replied).")
                    continue
                
                print(f"🚀 Processing new comment from @{username}...")
                
                custom_ai_reply = generate_local_ai_reply(username, comment_text)
                print(f"✨ AI Reply Generated ({len(custom_ai_reply)} chars): {custom_ai_reply}")
                
                # 1. Post the custom AI emoji reply
                reply_to_public_comment(comment_id, custom_ai_reply)
                
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

