from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import textwrap


def makeStory(text, outputPath):
    text = textwrap.wrap(text, 30) #sanitize text with 
    text = '\n'.join(text)         #newlines and stuff

    img = Image.open("background.png") #open prerendered background
    img = img.convert("RGB") #make it a jpeg (remove alpha)
    draw = ImageDraw.Draw(img) #drawing surface
    font = ImageFont.truetype("arial.ttf", 69) #make this whatever font
    draw.text((50, 150),text,(0,0,0),font=font) #draw the text
    img.save(outputPath) #save it

if __name__ == '__main__':
    makeStory("This is a demonstration of story3.py. Im guessing that this is pretty close to the original before i lost it....", 'demo.jpg')
