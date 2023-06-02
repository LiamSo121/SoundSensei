import openai
import requests
import cv2
import numpy as np
import yaml

class Dalle:
    def __init__(self):  
        self.apiKey = "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"
        self.data = None


    def generate_image(self,emotion):
        with open('config.yaml') as f:
                self.data = self.data = yaml.load(f, Loader=yaml.FullLoader)
        prompt = f"Create a mesmerizing image that depicts a serene beach scene and conveys a feeling of profound {emotion}. The image should capture the essence of a tranquil view, . Utilize colors, lighting, and composition to evoke a deep sense of {emotion} and convey the peaceful atmosphere. Let the image reflect the harmony and beauty of nature, merging it with the emotion you desire to portray. Be imaginative and innovative in illustrating this unique blend of natural elements and emotion."
        openai.api_key = self.apiKey

        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size= self.data['dalle-2']['size'],
            )
        except Exception as e:
            print(e)
        image_url = response["data"][0]["url"]
        # Send a GET request to retrieve the image
        response = requests.get(image_url, stream=True).raw

        image = np.asarray(bytearray(response.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # Show the image
        return image