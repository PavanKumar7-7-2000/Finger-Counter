import os
import cv2

def loadImages():

    ##  Path To Images Folder   ##
    source = os.path.join("finger_images")

    ## Path to 0-5 Image Files  ##
    images_path = os.path.join(source, "images")
    
    ## Loading Image Files in directory ##
    image_files = os.listdir(images_path)

    ## Image List of 0-5 images ##
    images = []

    ##  Loading Images 0-5  ##
    for file in image_files:
        image_path = os.path.join(images_path, file)
        image = cv2.imread(image_path)
        images.append(image)
    
    return images

def loadBlankImage():
    ##  Path To Images Folder   ##
    source = os.path.join("finger_images")

    ## Path to Blank Image File  ##
    blank_image_path = os.path.join(source, "blank", "blank.jpg")
    
    ##  Loading Blank Image  ##
    blank_image = cv2.imread(blank_image_path)

    return blank_image

