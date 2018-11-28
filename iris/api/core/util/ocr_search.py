# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import copy

import cv2
import numpy as np

try:
    import Image
except ImportError:
    from PIL import Image

from core_helper import *
from image_remove_noise import process_image_for_ocr, OCR_IMAGE_SIZE
from save_debug_image import save_debug_image

logger = logging.getLogger(__name__)


class OCRSearch:

    def search_for_phrase(self, local_what, local_text_dict):
        return_single = None

        matches_string = self.ocr_matches_to_string(local_text_dict)
        if local_what not in matches_string:
            return None

        l_what_words = local_what.split()
        l_words_len = len(l_what_words)
        temp_matches = []
        temp_debug = []

        phrase_start_index = matches_string.find(local_what)
        phrase_first_match_index = len(matches_string[0:phrase_start_index].split())

        if l_words_len > 0:
            for local_match_index, local_match_object in enumerate(local_text_dict):
                if local_match_index >= phrase_first_match_index:
                    for word_index, searched_word in enumerate(l_what_words):
                        if searched_word == local_match_object['value']:
                            temp_matches.append(local_match_object)
                            temp_debug.append(self.debug_data[local_match_index])
            return_single = self._combine_text_matches(temp_matches, local_what)
            self.save_ocr_debug_image(self.debug_img, temp_debug)
        return return_single

    def search_for_word(self, local_what, local_text_dict, local_multiple_matches):
        return_multiple = []
        return_single = None

        for local_match_index, local_match_object in enumerate(local_text_dict):
            if local_what == local_match_object['value']:
                if local_multiple_matches:
                    return_multiple.append(local_match_object)
                else:
                    self.save_ocr_debug_image(self.debug_img, [self.debug_data[local_match_index]])
                    return_single = local_match_object

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
        cv2.imwrite(IrisCore.get_image_debug_path() + '/' + temp_f, on_region)

    @staticmethod
    def ocr_matches_to_string(matches):
        ocr_string = ''
        for match in matches:
            if match is not None and match['value']:
                ocr_string += ' ' + str(match['value'])
        return ocr_string

    @staticmethod
    def _combine_text_matches(matches, value):
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
    def text_search_all(with_image_processing=True, in_region=None, in_image=None):
        if in_image is None:
            stack_image = IrisCore.get_region(in_region, True)
        else:
            stack_image = in_image

        match_min_len = 12
        input_image = stack_image
        input_image_array = np.array(input_image)
        debug_img = input_image_array

        if with_image_processing:
            input_image = process_image_for_ocr(image_array=input_image)
            input_image_array = np.array(input_image)
            debug_img = cv2.cvtColor(input_image_array, cv2.COLOR_GRAY2BGR)

        processed_data = pytesseract.image_to_data(input_image)

        length_x, width_y = stack_image.size
        dpi_factor = max(1, int(OCR_IMAGE_SIZE / length_x))

        final_data, debug_data = [], []
        is_uhd, uhd_factor = IrisCore.get_uhd_details()

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

                    if in_region is not None:
                        left_offset = in_region.x
                        top_offset = in_region.y

                    # Scale down coordinates since actual screen has different dpi
                    if with_image_processing:
                        screen_data = copy.deepcopy(virtual_data)
                        screen_data['x'] = screen_data['x'] / dpi_factor / scale_divider + left_offset
                        screen_data['y'] = screen_data['y'] / dpi_factor / scale_divider + top_offset
                        screen_data['width'] = screen_data['width'] / dpi_factor / scale_divider
                        screen_data['height'] = screen_data['height'] / dpi_factor / scale_divider
                        final_data.append(screen_data)
                    else:
                        if scale_divider > 1:
                            screen_data = copy.deepcopy(virtual_data)
                            screen_data['x'] = screen_data['x'] / scale_divider
                            screen_data['y'] = screen_data['y'] / scale_divider
                            screen_data['width'] = screen_data['width'] / scale_divider
                            screen_data['height'] = screen_data['height'] / scale_divider
                            final_data.append(screen_data)
            except Exception:
                continue

        return final_data, debug_img, debug_data

    def text_search_by(self, what, match_case=True, in_region=None, multiple_matches=False):
        if not isinstance(what, str):
            return ValueError(INVALID_GENERIC_INPUT)

        text_dict, self.debug_img, self.debug_data = self.text_search_all(True, in_region)

        if len(text_dict) <= 0:
            return None

        if not match_case:
            what = what.lower()

        final_m_matches = []

        words_n = len(what.split())
        should_search_phrase = True if words_n > 1 else False

        logger.debug('> All words on region/screen: ' + self.ocr_matches_to_string(text_dict))

        if should_search_phrase:
            logger.debug('> Search for phrase: %s' % what)
            final_s_match = self.search_for_phrase(what, text_dict)
        else:
            logger.debug('> Search for word: %s' % what)
            final_m_matches, final_s_match = self.search_for_word(what, text_dict, multiple_matches)

        if multiple_matches:
            if len(final_m_matches) > 0:
                return final_m_matches
        else:
            if final_s_match is not None:
                return final_s_match

        # At this point no match was found.
        # Retry matching with auto zoom search over each word.

        logger.debug('> No match, try zoom search')

        for match_index, match_object in enumerate(text_dict):
            # Crop word region.
            if match_object['width'] > 0 and match_object['height'] > 0:
                from iris.api.core.region import Region
                zoomed_word_image = IrisCore.get_screenshot(region=Region(match_object['x'] - 3, match_object['y'] - 2,
                                                                          match_object['width'] + 6,
                                                                          match_object['height'] + 4))

                w_img_w, w_img_h = zoomed_word_image.size
                # New white image background for zoom in search.
                word_background = Image.new('RGBA', (match_object['width'] * 10, match_object['height'] * 5),
                                            (255, 255, 255, 255))

                b_img_w, b_img_h = word_background.size
                # Offset to paste image on center.
                offset = ((b_img_w - w_img_w) // 2, (b_img_h - w_img_h) // 2)

                word_background.paste(zoomed_word_image, offset)

                found, debug_img_a, debug_data_a = self.text_search_all(True, None, word_background)
                if len(found) > 0:
                    text_dict[match_index]['value'] = found[0]['value']
                    logger.debug('> (Zoom search) new match: %s' % found[0]['value'])
                    if what == found[0]['value']:
                        break
                    if what in self.ocr_matches_to_string(text_dict):
                        break

        logger.debug('> (Zoom search) All words on region/screen: ' + self.ocr_matches_to_string(text_dict))

        if should_search_phrase:
            logger.debug('> Search with zoom for phrase: %s' % what)
            final_s_match = self.search_for_phrase(what, text_dict)
        else:
            logger.debug('> Search with zoom for word: %s' % what)
            final_m_matches, final_s_match = self.search_for_word(what, text_dict, multiple_matches)

        if multiple_matches:
            if len(final_m_matches) > 0:
                return final_m_matches
            else:
                save_debug_image(what, in_region, None, True)
                return None
        else:
            if final_s_match is not None:
                return final_s_match
            else:
                save_debug_image(what, in_region, None, True)
                return None
