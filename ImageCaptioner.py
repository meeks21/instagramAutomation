import openai
import base64
from PIL import Image
from config import api_key, imgbb_api_key 
import io
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class ImageCaptioner:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def compress_image(self, input_path, output_path, quality=85):
        try:
            with Image.open(input_path) as img:
                img.save(output_path, "JPEG", quality=quality)
            logger.info(f"Image compressed and saved to {output_path}")
        except Exception as e:
            logger.error(f"Error compressing image: {e}")

    def upload_image(self, image_path):
        try:
            with open(image_path, "rb") as image_file:
                response = requests.post(
                    "https://api.imgbb.com/1/upload",
                    data={"key": imgbb_api_key},
                    files={"image": image_file}
                )
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response content: {response.content}")

            response_json = response.json()
            return response_json["data"]["url"]
        except requests.exceptions.JSONDecodeError as e:
            logger.error("JSON decode error: Could not parse response as JSON")
            logger.error(f"Response content: {response.content}")
            raise e
        except Exception as e:
            logger.error(f"Error uploading image: {e}")
            raise e

    def get_image_caption(self, image_path):
        try:
            # Compress the image
            compressed_image_path = "compressed_image.jpg"
            self.compress_image(image_path, compressed_image_path)

            # Upload the compressed image
            image_url = self.upload_image(compressed_image_path)

            # Create a prompt for ChatGPT
            prompt = f"Create an Instagram caption for the following image: {image_url}"

            # Call the OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )

            # Extract and return the caption
            caption = response.choices[0].message['content'].strip()
            logger.info("Caption generated successfully")
            return caption
        except Exception as e:
            logger.error(f"Error generating caption: {e}")
            raise e

# Example usage
if __name__ == "__main__":
    image_path = "/home/meeks/groovePlant/logos/sage5.jpeg"
    captioner = ImageCaptioner(api_key)
    try:
        caption = captioner.get_image_caption(image_path)
        print("Generated Caption:", caption)
    except Exception as e:
        logger.error(f"Failed to generate caption: {e}")