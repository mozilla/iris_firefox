from iris2.core.screen.screen import Screen
from iris2.core.finder.pattern import Pattern
from iris2.core.finder.finder import find_all, find, verify, match_template
from iris2.core.screen.region import Region
from iris2.core.enums import MatchTemplateType
from iris2.core.mouse.mouse_controller import Mouse
from iris2.core.helpers.location import Location
import time

region = Region(0, 50, 400, 600)
# region.highlight()
print(region.right_click(Pattern('test.png', application='firefox')))





