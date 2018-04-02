import tempfile

import cv2
import numpy as np
from PIL import Image

IMAGE_SIZE = 1800
BINARY_THREHOLD = 180

size = None


def get_size_of_scaled_image(im):
    global size
    if size is None:
        length_x, width_y = im.size
        factor = max(1, int(IMAGE_SIZE / length_x))
        size = factor * length_x, factor * width_y
    return size


def process_image_for_ocr(file_path=None, image_array=None):
    temp_filename = set_image_dpi(file_path=file_path, image_array=image_array)
    im_new = remove_noise_and_smooth(temp_filename)
    return im_new


def set_image_dpi(file_path=None, image_array=None):
    if image_array is None:
        im = Image.open(file_path)
    elif file_path is None:
        im = image_array

    no_alpha_image = im.convert("RGB")
    input_size = get_size_of_scaled_image(no_alpha_image)
    im_resized = no_alpha_image.resize(input_size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))
    return temp_filename


def image_smoothening(img):
    ret1, th1 = cv2.threshold(img, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3


def remove_noise_and_smooth(file_name):
    img = cv2.imread(file_name, 0)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothening(img)
    or_image = cv2.bitwise_or(img, closing)
    return or_image
