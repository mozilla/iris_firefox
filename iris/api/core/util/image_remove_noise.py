# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import platform
import tempfile

import cv2
import numpy as np
from PIL import Image

OCR_IMAGE_SIZE = 1800
BINARY_THRESHOLD = 180


def get_size_of_scaled_image(im):
    size = None
    if size is None:
        length_x, width_y = im.size
        factor = max(1, int(OCR_IMAGE_SIZE / length_x))
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

    no_alpha_image = im.convert('RGB')
    input_size = get_size_of_scaled_image(no_alpha_image)
    im_resized = no_alpha_image.resize(input_size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))
    return temp_filename


def image_smoothing(img):
    # Apply threshold to get image with only b&w (binarization)
    ret1, th1 = cv2.threshold(img, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3


def remove_noise_and_smooth(file_name):
    img = cv2.imread(file_name, 0)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 3)
    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothing(img)
    or_image = cv2.bitwise_or(img, closing)

    if platform.system() == 'Darwin':
        median_blur = cv2.medianBlur(or_image, 3)
        return median_blur
    else:
        return or_image
