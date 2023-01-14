MODEL_FILENAME = 'numeric_captcha_model.hdf5'
NUMBER_OF_CHARS = 5

from keras.models import load_model
import numpy as np
import cv2
import base64
import imutils
import time


cnn = load_model(MODEL_FILENAME)

def resize_to_fit(image, width, height):
    (h, w) = image.shape[:2]
    if w > h:
        image = imutils.resize(image, width=width)
    else:
        image = imutils.resize(image, height=height)
    image = cv2.resize(image, (width, height))
    return image


def slice(img):
    # mask black color
    lower = np.array([0, 0, 0])  # -- Lower range --
    upper = np.array([30, 30, 30])  # -- Upper range --
    mask = cv2.inRange(img, lower, upper)
    img = cv2.bitwise_not(img, img, mask=mask)
    # cv2.imshow('mask', mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # convert to grayscale
    gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gry', gry)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # upscale
    (h, w) = gry.shape[:2]
    gry = cv2.resize(gry, (w * 2, h * 2))
    # cv2.imshow('resize', gry)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # morph close
    cls = cv2.morphologyEx(gry, cv2.MORPH_CLOSE, None)
    # cv2.imshow('cls', cls)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # remove background
    thr = cv2.threshold(cls, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # cv2.imshow('image', thr)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # remove small objects
    element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
    cls2 = cv2.morphologyEx(thr, cv2.MORPH_CLOSE, element)
    # cv2.imshow('cls2', cls2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    blur = cv2.blur(cls2, (10, 10))
    # cv2.imshow('blur', blur)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # downscale
    (h, w) = blur.shape[:2]
    blur2 = cv2.resize(blur, (w // 2, h // 2))
    # cv2.imshow('blur2', blur2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # trim
    inverted = 255 * (blur2 < 128).astype(np.uint8)
    coords = cv2.findNonZero(inverted)  # Find all non-zero points (text)
    x, y, w, h = cv2.boundingRect(coords)  # Find minimum spanning bounding box
    rect = blur2[y:y + h, x:x + w]
    # cv2.imshow('rect', rect)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    (h, w) = rect.shape[:2]
    letter_image_regions = []

    for idx in range(NUMBER_OF_CHARS):
        letter_image_regions.append((idx * w // NUMBER_OF_CHARS, 0, w // NUMBER_OF_CHARS, h))

    letter_images = []
    for letter_bounding_box in letter_image_regions:
        # Grab the coordinates of the letter in the image
        x, y, w, h = letter_bounding_box

        # Extract the letter from the original image with a 2-pixel margin around the edge
        letter_images.append(rect[y:y + h, x:x + w])

    return letter_images


def base64_to_image(base64string):
    np_arr = np.frombuffer(base64.b64decode(base64string), np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return img

def solve_char(char_image):
    char_image = resize_to_fit(char_image, 64, 64)
    char_image = np.expand_dims(char_image, axis=0)
    prediction_result = cnn.predict(char_image / 255.0)
    return str(np.argmax(prediction_result[0]))

def solve(img):
    letter_images = slice(img)

    start_time = time.time()
    predictions = [None for i in range(NUMBER_OF_CHARS)]
    for idx in range(NUMBER_OF_CHARS):
        predictions[idx] = solve_char(letter_images[idx])

    print(predictions)
    end_time = time.time()
    print('Time elapsed: ', end_time - start_time)

    return ''.join(predictions)

def solve_base64(base64):
    return solve(base64_to_image(base64))

if (__name__ == '__main__'):
    solve_base64(
        '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')
