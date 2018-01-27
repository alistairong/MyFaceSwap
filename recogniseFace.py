import face_recognition
import cv2
import numpy
debug = False



def getFaceCoordinates(input_image, upfactor=1, mode='hog', returnmode='2D'):
    '''
    Function can take in either a path string or an image object created by cv2.imread()
    getFaceCoordinates returns a tuple of coordinates of the face detected as

    returnmode: 1D
        [(left, top, right, bottom)...]

    returnmode: 2D
        [((left, top), (right, top), (right, bottom), (left, bottom))...]
    '''
    # Allows for multiple argument types
    if (type(input_image) is str):
        input_image = cv2.imread(input_image)
    elif (type(input_image) is numpy.ndarray):
        pass
    height, width, channels = input_image.shape
    scale = 800 / height

    # input_image = cv2.resize(input_image, (0, 0), fx=scale, fy=scale)
    # [(left, top, right, bottom)] = face_recognition.face_locations(input_image)

    array_of_face_locations = []
    # model='hog' quick and dirty model='cnn' slower but accurate
    for (bottom, right, top, left) in face_recognition.face_locations(input_image,
                                                                      number_of_times_to_upsample=upfactor ,model=mode):
        array_of_face_locations.append((left, top, right, bottom))

    if (debug):
        for (left, top, right, bottom) in array_of_face_locations:
            cv2.rectangle(input_image, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.imshow("Test Image", input_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    if(returnmode == "1D"):
        return array_of_face_locations

    elif(returnmode == "2D"):
        array_of_face_coordinates = []
        for (left, top, right, bottom) in array_of_face_locations:
            topleft = (left, top)
            topright = (right, top)
            bottomleft = (left, bottom)
            bottomright = (right, bottom)
            array_of_face_coordinates.append((topleft, topright, bottomright, bottomleft))
        return array_of_face_coordinates

if debug:
    test = cv2.imread("test.jpg")
    print(getFaceCoordinates("test2.jpg", returnmode="2D"))
    # Draw a box around the face