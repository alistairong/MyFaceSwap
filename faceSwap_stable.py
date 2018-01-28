from PIL import Image
from recogniseFace import *
import cv2
# from blendImages import *

debug = False

def replace_all(source, destination, scale=1.00):
    destination_cv2 = cv2.imread(destination)
    source = Image.open(source)
    destination = Image.open(destination)

    array_of_faces = getFaceCoordinates(destination_cv2, returnmode="1D")
    # print(array_of_faces) #debugging
    for (left, top, right, bottom) in array_of_faces:
        left = int(left / scale)
        top = int(top / scale)
        right = int(scale * right)
        bottom = int(scale * bottom)

        width = right - left
        height = bottom - top

        source = source.resize((width, height), Image.ANTIALIAS)
        destination.paste(source, (left, top, right, bottom))
    destination = destination.convert("RGB")
    return destination

def crop_image(image_path, scale=1.00):
    # assert that the image only contains one face
    left_result = None
    top_result = None
    right_result = None
    bottom_result = None

    for (left, top, right, bottom) in getFaceCoordinates(image_path, returnmode="1D"):
        # print(getFaceCoordinates(image_path, returnmode="1D")) #debugging
        left_result = int(left / scale)
        top_result = int(top / (scale))
        right_result = int(right * scale)
        bottom_result = int(bottom * scale)

    image_pil = Image.open(image_path)
    return image_pil.crop((left_result, top_result, right_result, bottom_result))

def faceSwap(source_path, destination_path, userid="default_" ,scale=1.00):
    crop_image(source_path, scale).save('./cropped.jpg')
    # blendImages("cropped.jpg")
    replace_all("cropped.jpg", destination_path, scale).save('./' + 'result.jpg')

# faceSwap("yara.jpg", "barack-obama.jpg")
#Image.open('./' + 'userid' + 'result.jpg').show()

# if debug:
#     faceSwap("temp.jpg", "test2.jpg")
#     Image.open('result.jpg').show()
