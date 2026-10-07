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

def verify_and_get_true_instagram_id():
    """
    Validates if the provided ID is correct. If it throws a 400 error,
    it automatically crawls Meta to discover the true Instagram Business Account ID.
    """
    # Test the provided ID first
    test_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media?access_token={ACCESS_TOKEN}"
    test_res = requests.get(test_url)
    if test_res.status_code == 200:
        return INSTAGRAM_ACCOUNT_ID
        
    print("⚠️ Provided ID failed validation. Attempting automatic structural lookup...")
    
    # Discovery Step A: Fetch linked account fields using me/accounts
    lookup_url = f"https://facebook.com/{ACCESS_TOKEN}"
    try:
        res = requests.get(lookup_url).json()
        pages = res.get('data', [])
        for page in pages:
            ig_account = page.get('instagram_business_account')
            if ig_account and ig_account.get('id'):
                true_id = ig_account.get('id')
                print(f"🎯 Successfully auto-discovered true Instagram ID: {true_id}")
                return true_id
    except Exception:
        pass

    # Discovery Step B: Try reading target profile context directly using fallback variables
    direct_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}?fields=instagram_business_account&access_token={ACCESS_TOKEN}"
    try:
        res = requests.get(direct_url).json()
        true_id = res.get('instagram_business_account', {}).get('id')
        if true_id:
            print(f"🎯 Successfully discovered Instagram ID via Direct Node Check: {true_id}")
            return true_id
    except Exception:
        pass

    return INSTAGRAM_ACCOUNT_ID

# Run verification hook before launching main pipeline loop
TRUE_INSTAGRAM_ID = verify_and_get_true_instagram_id()

def get_latest_media():
    url = f"https://graph.facebook.com/v18.0/{TRUE_INSTAGRAM_ID}/media?access_token={ACCESS_TOKEN}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get('data', [])
        return data[0] if data else None  # Target array index matching your previous setup
    except Exception as e:
        print(f"❌ Failed to fetch media: {e}")
        return None

def send_dm(user_id, message_text):
    url = f"https://facebook.com/{ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": user_id},
        "message": {"text": message_text}
    }
    requests.post(url, json=payload)

def reply_to_public_comment(comment_id, message_text):
    url = f"https://graph.facebook.com/v18.0/{comment_id}/replies"
    payload = {
        'message': message_text,
        'access_token': ACCESS_TOKEN
    }
    requests.post(url, data=payload)

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
                
                # Prevent self-loop triggers
                if instagram_user_id == TRUE_INSTAGRAM_ID:
                    continue
                
                print(f"🚀 Processing comment from @{username}...")
                
                # Dynamic Ollama text generation integration
                custom_ai_reply = generate_local_ai_reply(username, comment_text)
                print(f"✨ AI Reply Created: {custom_ai_reply}")
                
                # 1. Post the custom AI message directly on the comment thread
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

