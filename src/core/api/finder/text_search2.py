import difflib

import cv2
import pytesseract
from PIL import ImageEnhance

from src.core.api.screen.screenshot_image import ScreenshotImage
from src.core.api.rectangle import Rectangle

TRY_RESIZE_IMAGES = 3
OCR_RESULT_COLUMNS_COUNT = 12
PIXEL_COUNT = 30


def is_similar_result(result_list: list, x: int, y: int, pixels: int):
    if len(result_list) == 0:
        return False

    for result in result_list:
        if (x - pixels <= result.x <= x + pixels) and (y - pixels <= result.y <= y + pixels):
            return True
    return False


def _replace_multiple(main_string, replace_string, replace_with_string):
    for elem in replace_string:
        if elem in main_string:
            main_string = main_string.replace(elem, replace_with_string)

    return main_string


def _text_search(text, img, multiple_search=False):
    cutoffs = {'string': {'min_cutoff': 0.6, 'max_cutoff': 0.9, 'step': 0.1},
               'digit': {'min_cutoff': 0.75, 'max_cutoff': 0.9, 'step': 0.05}}

    digit_chars = ['.', '%', ',']
    cutoff_type = 'digit' if _replace_multiple(text, digit_chars, '').isdigit() else 'string'

    raw_gray_image = img.get_gray_image()
    enhanced_image = ImageEnhance.Contrast(img.get_gray_image()).enhance(10.0)
    stack_images = [raw_gray_image, enhanced_image]
    final_data = []

    for stack_image in stack_images:
        for index, scale in enumerate(range(1, TRY_RESIZE_IMAGES + 1)):
            stack_image = stack_image.resize([img.get_gray_image().width * scale, img.get_gray_image().height * scale])
            processed_data = pytesseract.image_to_data(stack_image)
            for line in processed_data.split('\n'):
                d = line.split()
                if len(d) == OCR_RESULT_COLUMNS_COUNT:
                    cutoff = cutoffs[cutoff_type]['max_cutoff']
                    while cutoff >= cutoffs[cutoff_type]['min_cutoff']:
                        if difflib.get_close_matches(text, [d[11]], cutoff=cutoff):
                            try:
                                x = int(int(d[6]) / scale)
                                y = int(int(d[7]) / scale)
                                width = int(int(d[8]) / scale)
                                height = int(int(d[9]) / scale)
                                virtual_data = Rectangle(x, y, width, height)

                                if multiple_search:
                                    if len(final_data) == 0:
                                        final_data.append(virtual_data)
                                    else:
                                        if not is_similar_result(final_data, x, y, PIXEL_COUNT):
                                            final_data.append(virtual_data)
                                else:
                                    cv2.rectangle(img.get_gray_array(), (x, y), (x + width, y + height), (0, 0, 255), 1)
                                    cv2.imwrite('x5.png', img.get_gray_array(), [int(cv2.IMWRITE_JPEG_QUALITY), 50])
                                    return virtual_data
                            except ValueError:
                                continue
                        cutoff -= cutoffs[cutoff_type]['step']

    for d in final_data:
        cv2.rectangle(img.get_gray_array(), (d.x, d.y), (d.x + d.width, d.y + d.height), (0, 0, 255), 1)
        cv2.imwrite('x5.png', img.get_gray_array(), [int(cv2.IMWRITE_JPEG_QUALITY), 50])
    return final_data


def text_find(text, img):
    return _text_search(text, img, False)


def text_find_all(text, img):
    return _text_search(text, img, True)


image = ScreenshotImage(Rectangle(0, 0, 300, 500))
image.get_gray_image().show()
print(text_find('Top Sites', image))
