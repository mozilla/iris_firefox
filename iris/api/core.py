# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


# This class is used to wrap methods around the Sikuli API

import os
from platform import *

import pyautogui
pyautogui.FAILSAFE = False

import numpy as np
import random
import time
import sys
import os
from helpers.image_remove_noise import process_image_for_ocr

try:
    import Image
except ImportError:
    from PIL import Image

import pytesseract
import cv2




DEFAULT_IMG_ACCURACY = 0.8
IMAGES = {}
CURRENT_PLATFORM = None


def get_os():
    if os.path.exists("C:\\"):
        return "win"
    if os.path.exists("/Applications"):
        return "osx"
    else:
        return "linux"


def get_platform():
    if get_os() == "osx":
        return "osx"
    if sys.maxsize == 2 ** 31:
        return get_os() + "32"
    else:
        return get_os()


def get_module_dir():
    return os.path.realpath(os.path.split(__file__)[0] + "/../..")



if get_os() == "osx":
    pytesseract.pytesseract.tesseract_cmd = '<unknown>'
    CURRENT_PLATFORM = 'osx'
elif get_os() == "win":
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
    CURRENT_PLATFORM = 'win'
elif get_os() == "linux":
    pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
    CURRENT_PLATFORM = 'linux'

PROJECT_BASE_PATH = os.path.abspath(os.path.join("iris", os.pardir))
for root, dirs, files in os.walk(PROJECT_BASE_PATH):
    for file_name in files:
        if file_name.endswith(".png"):
            if CURRENT_PLATFORM in root:
                print ("Pattern found: " + os.path.join(root, file_name))
                IMAGES[file_name] = os.path.join(root, file_name)

screenWidth, screenHeight = pyautogui.size()

'''

grabs a region (topx, topy, bottomx, bottomy)
to the tuple (topx, topy, width, height)

input : a tuple containing the 4 coordinates of the region to capture

output : a PIL image of the area selected.

'''


def _region_grabber(region):
    x1 = region[0]
    y1 = region[1]
    width = region[2] - x1
    height = region[3] - y1

    return pyautogui.screenshot(region=(x1, y1, width, height))


'''
Searchs for an image within an area

input :

image : path to the image file (see opencv imread for supported types)
x1 : top left x value
y1 : top left y value
x2 : bottom right x value
y2 : bottom right y value
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
im : a PIL image, usefull if you intend to search the same unchanging region for several elements

returns :
the top left corner coordinates of the element if found as an array [x,y] or [-1,-1] if not
'''


def _imagesearcharea(image_name, x1, y1, x2, y2, precision=0.8, im=None):
    image_path = IMAGES[image_name]
    if im is None:
        im = _region_grabber(region=(x1, y1, x2, y2))
        # im.save('testarea.png') usefull for debugging purposes, this will save the captured region as "testarea.png"

    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image_path, 0)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc


# @todo add more option for image_grabber
# @todo map data form image_to_data and search for text input

def text_search(text, debug):
    screenWidth, screenHeight = pyautogui.size()
    screencapture = _region_grabber(region=(screenWidth / 2 - 400, 50, screenWidth / 2, 800))
    screencapture.save('./debug.png')

    optimized_ocr_image = process_image_for_ocr('./debug.png')
    cv2.imwrite("./debug_ocr_ready.png", optimized_ocr_image)
    print(pytesseract.image_to_data(Image.fromarray(optimized_ocr_image)))


'''

click on the center of an image with a bit of random.
eg, if an image is 100*100 with an offset of 5 it may click at 52,50 the first time and then 55,53 etc
Usefull to avoid anti-bot monitoring while staying precise.

this function doesn't search for the image, it's only ment for easy clicking on the images.

input :

image : path to the image file (see opencv imread for supported types)
pos : array containing the position of the top left corner of the image [x,y]
action : button of the mouse to activate : "left" "right" "middle", see pyautogui.click documentation for more info
time : time taken for the mouse to move from where it was to the new position
'''


def _click_image(image, pos, action, timestamp, offset=5):
    imagepath = IMAGES[image]
    img = cv2.imread(imagepath)
    height, width, channels = img.shape
    pyautogui.moveTo(pos[0] + rnd(width / 2, offset), pos[1] + rnd(height / 2, offset), timestamp)
    pyautogui.click(button=action)


'''
Searchs for an image on the screen

input :

image : path to the image file (see opencv imread for supported types)
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
im : a PIL image, usefull if you intend to search the same unchanging region for several elements

returns :
the top left corner coordinates of the element if found as an array [x,y] or [-1,-1] if not

'''


def _imagesearch(image, precision=0.8):
    im = pyautogui.screenshot()
    # im.save('testarea.png') usefull for debugging purposes, this will save the captured region as "testarea.png"
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc


'''
Searchs for an image on screen continuously until it's found.

input :
image : path to the image file (see opencv imread for supported types)
time : Waiting time after failing to find the image 
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8

returns :
the top left corner coordinates of the element if found as an array [x,y] 

'''


def _imagesearch_loop(imagename, timesample, attempts=5, precision=0.8):
    imagepath = IMAGES[imagename]
    pos = _imagesearch(imagepath, precision)
    tries = 0
    print("Looking for: " + imagepath)
    while (pos[0] == -1) and (tries < attempts):
        print(imagepath + " not found, waiting")
        time.sleep(timesample)
        pos = _imagesearch(imagepath, precision)
        tries += 1
    return pos


'''
Searchs for an image on a region of the screen continuously until it's found.

input :
image : path to the image file (see opencv imread for supported types)
time : Waiting time after failing to find the image 
x1 : top left x value
y1 : top left y value
x2 : bottom right x value
y2 : bottom right y value
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8

returns :
the top left corner coordinates of the element as an array [x,y] 

'''


def _imagesearch_region_loop(image, timesample, x1, y1, x2, y2, precision=0.8):
    pos = _imagesearcharea(image, x1, y1, x2, y2, precision)

    while pos[0] == -1:
        time.sleep(timesample)
        pos = _imagesearcharea(image, x1, y1, x2, y2, precision)
    return pos


def rnd(num, rand):
    return num + rand * random.random()


'''

Sikuli wrappers
- wait
- waitVanish
- click
- exists 

'''


def wait(image_name, attempts, time_sample=0.5, precision=DEFAULT_IMG_ACCURACY):
    image_path = IMAGES[image_name]
    image_found = _imagesearch_loop(image_name, time_sample, attempts, precision)
    if (image_found[0] != -1) & (image_found[1] != -1):
        print(image_path + " found")
        return True
    return False


def waitVanish(image_name, attempts, time_sample=0.5, precision=DEFAULT_IMG_ACCURACY):
    image_path = IMAGES[image_name]
    image_found = _imagesearch_loop(image_name, time_sample, attempts, precision)
    if (image_found[0] == -1) & (image_found[1] == -1):
        print(image_path + " has vanish")
        return True
    return False


def click(imagename):
    # @todo Search in regions for faster results
    pos = _imagesearcharea(imagename, 0, 0, screenWidth, screenHeight)
    if pos[0] != -1:
        print("Found " + imagename + " position : ", pos[0], pos[1])
        _click_image(imagename, pos, "left", 0, offset=5)
        time.sleep(1)
        return pos
    else:
        print("Image not found:", imagename)


def exists(image_name, time_sample):
    # return wait(image_name, 2, time_sample)
    return wait(image_name, 5, 0.5)


# @todo to take in consideration the number of screens
def get_screen(debug=False):
    pyautogui.displayMousePosition()
    screenWidth, screenHeight = pyautogui.size()
    screencapture = _region_grabber(region=(0, 0, screenWidth / 2, screenHeight))
    if (debug):
        screencapture.save(PROJECT_BASE_PATH + 'debug.png')
    return screencapture


def hover(x=0, y=0, duration=0.0, tween='linear', pause=None):
    print x
    print y
    pyautogui.moveTo(x, y, duration, tween, pause)
