"""-------Import OS : used to manage files...-------"""
import os
from PIL import Image

def image_cropping(directory:str, uuid_selected:str, extension:str):
    """function that crop an image and save it
    
    Keyword arguments:
    directory:str -- directory where the image is stocked (ex: "static/miniatures")
    uuid_selected:str -- uuid of the file
    extension:str -- the filetype (ex: ".jpg")
    Return: nothing
    """
    print(directory)
    image = Image.open(fr"{directory}/{uuid_selected}{extension}")
    print(image)
    width, height = image.size
    # Setting the points for cropped image
    left = (width/2)-600
    top = (height/2)-400
    right = (width/2)+600
    bottom = (height/2)+400
    # Cropped image of above dimension
    # (It will not change original image)
    im1 = image.crop((left, top, right, bottom))
    print(fr"{directory}/{uuid_selected}_crop{extension}")
    im1.save(fr"./{directory}/{uuid_selected}_crop{extension}")
    os.remove(fr"{directory}/{uuid_selected}{extension}")

print("Image Management launched !")
