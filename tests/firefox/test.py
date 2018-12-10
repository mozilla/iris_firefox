from core.screen.screen import Screen
from core.finder.pattern import Pattern
from core.finder.finder import find_all, find, wait, match_template
from core.screen.region import Region
from core.enums import MatchTemplateType
from core.mouse.mouse_controller import Mouse
from core.helpers.location import Location
import time

region = Region(1920, 50, 400, 600)
# region.highlight()
print(region.double_click(Pattern('test.png', application='firefox')))





