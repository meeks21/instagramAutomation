import praw
import urllib.request
import os
import subredditCollection
from datetime import datetime
from config import clientId, clientSecret

# Initialize PRAW with your credentials
reddit = praw.Reddit(
    client_id=clientId,
    client_secret=clientSecret,
    user_agent="memeScrapper"
)

# Subreddites to pull memes from
subreddit_values = subredditCollection.values
subreddits_str = ",".join(subreddit_values)


# Search for popular meme posts in a subreddit (e.g., r/memes)
subreddits = reddit.subreddit(subreddits_str)
for submission in subreddits.hot(limit=200):
    if submission.url.endswith((".jpg", ".png", ".gif")):
        # Create a folder with the current date as the title
        folder_name = datetime.now().strftime("%Y-%m-%d")
        folder_path = f"/home/meeks/groovePlant/memes/{folder_name}"
        
        # Check if the folder already exists
        if os.path.exists(folder_path):
            print(f"Folder {folder_path} already exists. Saving images to this folder.")
        else:
            os.makedirs(folder_path, exist_ok=True)
            print(f"Created new folder {folder_path}.")

        # Download the image to the new or existing folder
        url = submission.url
        local_filename = os.path.join(folder_path, f"{submission.id}.{submission.url.split('.')[-1]}")
        urllib.request.urlretrieve(url, local_filename)
        print(f"Saved {local_filename}")

print("Meme images saved successfully!")
