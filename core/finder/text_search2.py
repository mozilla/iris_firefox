import difflib

import cv2
import pytesseract
from PIL import ImageEnhance

from core.helpers.rectangle import Rectangle
from core.screen.screenshot_image import ScreenshotImage


def text_find(text, img, multiple_search=False):
    stack_image = ImageEnhance.Contrast(img.get_gray_image()).enhance(10.0)
    final_data = []
    try_resize_image = 6
    for scale in range(1, try_resize_image + 1):
        stack_image = stack_image.resize([img.get_gray_image().width * scale, img.get_gray_image().height * scale])
        processed_data = pytesseract.image_to_data(stack_image)
        for line in processed_data.split('\n'):
            data = line.split()
            if len(data) == 12 and difflib.get_close_matches(text, [data[11]]):
                try:
                    x = int(int(data[6]) / scale)
                    y = int(int(data[7]) / scale)
                    width = int(int(data[8]) / scale)
                    height = int(int(data[9]) / scale)
                    virtual_data = Rectangle(x, y, width, height)
                    cv2.rectangle(img.get_gray_array(), (x, y), (x + width, y + height), (0, 0, 255), 1)
                    cv2.imwrite('x5.png', img.get_gray_array(), [int(cv2.IMWRITE_JPEG_QUALITY), 50])
                    if multiple_search:
                        final_data.append(virtual_data)
                    else:
                        return virtual_data
                except ValueError:
                    continue

    return final_data


image = ScreenshotImage(Rectangle(0, 0, 200, 200))

print(text_find('SequenceMatcher', image))
