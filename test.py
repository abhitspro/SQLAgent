
# import os
from langchain_community.chat_message_histories import RedisChatMessageHistory
import os
from dotenv import load_dotenv

# MUST be called before os.getenv()
load_dotenv()

# Verify environment variable is loading properly
redis_url = os.getenv("REDIS_URL")
if not redis_url:
    raise ValueError("REDIS_URL is not set or .env file was not loaded.")

# Fetch the session history directly from Upstash
history = RedisChatMessageHistory(
    session_id="upstash_test_user",
    url=os.getenv("REDIS_URL"),
    ttl=86400
)

print("--- Stored Messages in Upstash ---")
for msg in history.messages:
    print(f"{msg.type.upper()}: {msg.content}")