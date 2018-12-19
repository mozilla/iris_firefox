# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import copy
import datetime
import logging
import tempfile

import cv2
import numpy
import pytesseract

try:
    import Image
except ImportError:
    from PIL import Image

from core.helpers.os_helpers import OSHelper
from core.helpers.path_manager import PathManager
from core.screen.screenshot_image import ScreenshotImage
from core.save_debug_image.save_image import save_debug_image

logger = logging.getLogger(__name__)


class TextSearch:

    def search_phrase(self, phrase, text_dict):
        return_single = None

        matches_string = self.ocr_matches_string(text_dict)
        if phrase not in matches_string:
            return None

        l_text_words = phrase.split()
        l_words_len = len(l_text_words)
        temp_matches = []
        temp_debug = []

        phrase_start_index = matches_string.find(phrase)
        phrase_first_match_index = len(matches_string[0:phrase_start_index].split())

        if l_words_len > 0:
            for local_match_index, local_match_object in enumerate(text_dict):
                if local_match_index >= phrase_first_match_index:
                    for word_index, searched_word in enumerate(l_text_words):
                        if searched_word == local_match_object['value']:
                            temp_matches.append(local_match_object)
                            temp_debug.append(self.debug_data[local_match_index])
            return_single = self.combine_text_matches(temp_matches, phrase)
            self.save_ocr_debug_image(self.debug_img, temp_debug)
        return return_single

    def search_word(self, word, text_dict, local_multiple_matches):
        return_multiple = []
        return_single = None

        for index, object in enumerate(text_dict):
            if word == object['value']:
                if local_multiple_matches:
                    return_multiple.append(object)
                else:
                    self.save_ocr_debug_image(self.debug_img, [self.debug_data[index]])
                    return_single = object

        return return_multiple, return_single

    @staticmethod
    def save_ocr_debug_image(on_region, matches):
        if matches is None:
            return

        border_line = 2
        if isinstance(matches, list):
            for mt in matches:
                cv2.rectangle(on_region,
                              (mt['x'], mt['y']), (mt['x'] + mt['width'], mt['y'] + mt['height']),
                              (0, 0, 255),
                              border_line)
        current_time = datetime.datetime.now()
        temp_f = str(current_time).replace(' ', '_').replace(':', '_').replace('.', '_').replace('-', '_') + '.jpg'
        cv2.imwrite(PathManager.get_image_debug_path() + '/' + temp_f, on_region)

    @staticmethod
    def ocr_matches_string(matches):
        ocr_string = ''
        for match in matches:
            if match is not None and match['value']:
                ocr_string += ' ' + str(match['value'])
        return ocr_string

    @staticmethod
    def combine_text_matches(matches, value):
        new_match = {'x': 0, 'y': 0, 'width': 0, 'height': 0, 'precision': 0.0, 'value': value}

        total_elem = len(matches)

        if total_elem > 0:
            new_match['x'] = matches[0]['x']
            new_match['y'] = matches[0]['y']
            for match in matches:
                new_match['width'] = new_match['width'] + match['width']
                new_match['height'] = new_match['height'] + match['height']
                new_match['precision'] = new_match['precision'] + match['precision']

            new_match['height'] = int(new_match['height'] / total_elem * 1.5)
            new_match['precision'] = new_match['precision'] / total_elem
            return new_match
        else:
            return None

    @staticmethod
    def image_to_string(image_processing, region=None, image=None):
        if image is None:
            stack_image = ScreenshotImage(region).get_gray_image()
        else:
            stack_image = image

        match_min_len = 12
        input_image = stack_image
        input_image_array = numpy.array(input_image)
        debug_img = input_image_array

        if image_processing:
            input_image = ImproveImage().process_image_for_ocr(image_array=input_image)
            input_image_array = numpy.array(input_image)
            debug_img = cv2.cvtColor(input_image_array, cv2.COLOR_GRAY2BGR)

        processed_data = pytesseract.image_to_data(input_image)

        length_x, width_y = stack_image.size
        dpi_factor = max(1, int(1800 / length_x))

        final_data, debug_data = [], []
        is_uhd = OSHelper.is_high_def_display()
        uhd_factor = OSHelper.get_display_factor()

        for line in processed_data.split('\n'):
            try:
                data = line.encode('ascii').split()
                if len(data) is match_min_len:
                    precision = int(data[10]) / float(100)
                    virtual_data = {'x': int(data[6]),
                                    'y': int(data[7]),
                                    'width': int(data[8]),
                                    'height': int(data[9]),
                                    'precision': float(precision),
                                    'value': str(data[11])
                                    }
                    debug_data.append(virtual_data)

                    left_offset, top_offset = 0, 0
                    scale_divider = uhd_factor if is_uhd else 1

                    if region is not None:
                        left_offset = region.x
                        top_offset = region.y

                    # Scale down coordinates since actual screen has different dpi
                    if image_processing:
                        screen_data = copy.deepcopy(virtual_data)
                        screen_data['x'] = screen_data['x'] / dpi_factor / scale_divider + left_offset
                        screen_data['y'] = screen_data['y'] / dpi_factor / scale_divider + top_offset
                        screen_data['width'] = screen_data['width'] / dpi_factor / scale_divider
                        screen_data['height'] = screen_data['height'] / dpi_factor / scale_divider
                        final_data.append(screen_data)
                    else:
                        if scale_divider >= 1:
                            screen_data = copy.deepcopy(virtual_data)
                            screen_data['x'] = screen_data['x'] / scale_divider
                            screen_data['y'] = screen_data['y'] / scale_divider
                            screen_data['width'] = screen_data['width'] / scale_divider
                            screen_data['height'] = screen_data['height'] / scale_divider
                            final_data.append(screen_data)
            except Exception:
                continue

        return final_data, debug_img, debug_data

    def text_search(self, text, match_case=True, region=None, multiple_matches=False):
        if not isinstance(text, str):
            return ValueError('Invalid input')

        text_dict, self.debug_img, self.debug_data = self.image_to_string(True, region)

        if len(text_dict) <= 0:
            return None

        if not match_case:
            text = text.lower()

        final_m_matches = []

        words_n = len(text.split())
        should_search_phrase = True if words_n > 1 else False

        logger.debug('> All words on region/screen: ' + self.ocr_matches_string(text_dict))

        if should_search_phrase:
            logger.debug('> Search for phrase: %s' % text)
            final_s_match = self.search_phrase(text, text_dict)
        else:
            logger.debug('> Search for word: %s' % text)
            final_m_matches, final_s_match = self.search_word(text, text_dict, multiple_matches)

        if multiple_matches:
            if len(final_m_matches) > 0:
                return final_m_matches
        else:
            if final_s_match is not None:
                return final_s_match

        # At this point no match was found.
        # Retry matching with auto zoom search over each word

        logger.debug('> No match, try zoom search')

        for match_index, match_object in enumerate(text_dict):
            # Word region
            if match_object['width'] > 0 and match_object['height'] > 0:
                from core.screen.region import Region
                zoomed_word_image = ScreenshotImage(
                    region=Region(int(match_object['x']), int(match_object['y'] - 2),
                                  int(match_object['width'] + 6),
                                  int(match_object['height'] + 4))).get_gray_image()

                w_img_w, w_img_h = zoomed_word_image.size
                # New white image background for zoom in search
                word_background = Image.new('RGBA', (int(match_object['width'] * 10), int(match_object['height'] * 5)),
                                            (255, 255, 255, 255))

                b_img_w, b_img_h = word_background.size
                # Offset to paste image on center
                offset = ((b_img_w - w_img_w) // 2, (b_img_h - w_img_h) // 2)

                word_background.paste(zoomed_word_image, offset)

                found, debug_img_a, debug_data_a = self.image_to_string(True, None, word_background)
                if len(found) > 0:
                    text_dict[match_index]['value'] = found[0]['value']
                    # save_ocr_debug_image(debug_img_a, debug_data_a)
                    logger.debug('> (Zoom search) new match: %s' % found[0]['value'])
                    if text == found[0]['value']:
                        break
                    if text in self.ocr_matches_string(text_dict):
                        break

        logger.debug('> (Zoom search) All words on region/screen: ' + self.ocr_matches_string(text_dict))

        if should_search_phrase:
            logger.debug('> Search with zoom for phrase: %s' % text)
            final_s_match = self.search_phrase(text, text_dict)
        else:
            logger.debug('> Search with zoom for word: %s' % text)
            final_m_matches, final_s_match = self.search_word(text, text_dict, multiple_matches)

        if multiple_matches:
            if len(final_m_matches) > 0:
                return final_m_matches
            else:
                save_debug_image(text, region, None)
                return None
        else:
            if final_s_match is not None:
                return final_s_match
            else:
                save_debug_image(text, region, None)
                return None


class ImproveImage:

    def process_image_for_ocr(self, file_path=None, image_array=None):
        temp_filename = self.set_image_dpi(file_path=file_path, image_array=image_array)
        im_new = self.remove_noise_and_smooth(temp_filename)
        return im_new

    def set_image_dpi(self, file_path=None, image_array=None):
        if image_array is None:
            im = Image.open(file_path)
        elif file_path is None:
            im = image_array

        no_alpha_image = im.convert('RGB')
        input_size = self.get_size_of_scaled_image(no_alpha_image)
        resized_image = no_alpha_image.resize(input_size, Image.ANTIALIAS)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        temp_filename = temp_file.name
        resized_image.save(temp_filename, dpi=(300, 300))
        return temp_filename

    @staticmethod
    def get_size_of_scaled_image(image):
        size = None
        if size is None:
            length_x, width_y = image.size
            factor = max(1, int(1800 / length_x))
            size = factor * length_x, factor * width_y
        return size

    @staticmethod
    def remove_noise_and_smooth(image):
        image = cv2.imread(image, 0)
        filtered = cv2.adaptiveThreshold(image.astype(numpy.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                         cv2.THRESH_BINARY, 41, 3)

        # Apply dilation and erosion to remove some noise
        kernel = numpy.ones((1, 1), numpy.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        image = cv2.erode(image, kernel, iterations=1)
        opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

        # Apply threshold to get image with only b&w (binarization)
        ret1, th1 = cv2.threshold(image, 180, 255, cv2.THRESH_BINARY)
        ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        blur = cv2.GaussianBlur(th2, (1, 1), 0)
        ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        or_image = cv2.bitwise_or(th3, closing)

        if OSHelper.is_mac():
            median_blur = cv2.medianBlur(or_image, 3)
            return median_blur
        else:
            return or_image
