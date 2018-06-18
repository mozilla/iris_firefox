import os
import logging

logger = logging.getLogger(__name__)


def _parse_name(full_name):
    start_symbol = '@'
    end_symbol = 'x.'
    if start_symbol not in full_name:
        return full_name, 1
    else:
        try:
            start_index = full_name.index(start_symbol)
            end_index = full_name.index(end_symbol, start_index)
            scale_factor = float(full_name[start_index + 1:end_index])
            image_name = full_name[0:start_index] + full_name[end_index + 1:len(full_name)]
            return image_name, scale_factor

        except ValueError:
            logger.warning('Invalid file name format:%s' % full_name)
            return full_name, 1


class IrisImage:
    def __init__(self, file_name, dir_name):
        name, factor = _parse_name(file_name)
        self._name = name
        self._path = os.path.join(dir_name, file_name)
        self._scale_factor = factor

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def scale_factor(self):
        return self._scale_factor
