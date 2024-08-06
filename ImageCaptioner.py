import openai
import base64
from PIL import Image
from config import api_key
import io

class ImageCaptioner:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def get_image_caption(self, image_path):
        # Open and encode the image
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')

        # Create a prompt for ChatGPT
        prompt = f"Describe the following image: {encoded_image}"

        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract and return the caption
        caption = response.choices[0].message['content'].strip()
        return caption

# Example usage
if __name__ == "__main__":
    api_key = api_key
    image_path = "/home/meeks/groovePlant/logos/sage5.jpeg"
    captioner = ImageCaptioner(api_key)
    caption = captioner.get_image_caption(image_path)
    print("Generated Caption:", caption)



