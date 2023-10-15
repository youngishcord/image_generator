from PIL import Image, ImageDraw
from random import randint

def create_images():
    for i in range(10):
        width, height = 64, 64
        x1, x2 = (randint(0, 44), randint(0, 44))
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)

        draw.rectangle([(x1, x2), (x1+20, x2+20)], fill="black", outline="black")
        
        image.save(f"./images/image_{i}.png")


create_images()