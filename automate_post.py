from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from config import username, password, api_key
from ImageCaptioner import ImageCaptioner
import logging

logger = logging.getLogger()
cl = Client()

def login_user(username, password):
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    # Attempt to load the session
    try:
        session = cl.load_settings("session.json")
        if session:
            cl.set_settings(session)
            cl.login(username, password)

            # Check if session is valid
            try:
                cl.get_timeline_feed()
                logger.info("Logged in using session.")
                return cl  # Successfully logged in
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password.")
    except FileNotFoundError:
        logger.info("No session file found, proceeding to login with username and password.")

    # If session login failed or doesn't exist, login with username and password
    try:
        logger.info(f"Attempting to login via username and password: {username}")
        cl.login(username, password)
        cl.dump_settings("session.json")  # Save session after successful login
        logger.info("Logged in using username and password.")
        return cl  # Successfully logged in
    except Exception as e:
        logger.error(f"Couldn't login user: {e}")
        raise Exception("Couldn't login user with either password or session.")

# Example usage
if __name__ == "__main__":
    USERNAME = username
    PASSWORD = password
    client = login_user(USERNAME, PASSWORD)

    # Initialize the captioner
    captioner = ImageCaptioner(api_key)

    # Upload a photo
    caption = captioner.get_image_caption('/home/meeks/groovePlant/logos/sage5.jpeg')
    cl.photo_upload('/home/meeks/groovePlant/logos/sage5.jpeg', caption=caption)
