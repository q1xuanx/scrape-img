import requests
from bs4 import BeautifulSoup
import validators
import shutil
import os
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

def save_image():
    r = requests.get(os.getenv('url_scape'))
    save_dir = r"C:/Users/ADMIN/Desktop/dogs"
    os.makedirs(save_dir, exist_ok=True)
    if r.status_code == 200: 
        s = BeautifulSoup(r.content, 'html.parser')
        s.find('picture', class_='absolute top-0 bottom-0 left-0 w-full')
        images = s.find_all('source')
        for index, image in tqdm(enumerate(images), total=len(images), ascii=True, desc="Fetch Image"): 
            url_image = image.get('srcset')
            if not validators.url(url_image):
                continue
            check_valid_image_url = requests.get(url_image, stream=True)
            if check_valid_image_url.status_code != 200: 
                continue
            file_name = f"image_{index}.webp"
            file_name = os.path.join(save_dir, file_name)
            with open(file_name, "wb") as f:
                shutil.copyfileobj(check_valid_image_url.raw, f)

        print(f"Scape success and save image to: {save_dir}")

if __name__ == '__main__':
    save_image()