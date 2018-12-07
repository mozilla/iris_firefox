from core.screen.screen import Screen
from core.finder.pattern import Pattern
from core.finder.finder import find_all, find, wait, match_template
from core.screen.region import Region
from core.enums import MatchTemplateType
from core.mouse.mouse import Mouse
from core.helpers.location import Location
import time

# region = Region(1920, 50, 400, 600)
# # region.highlight()
# print(region.find(Pattern('test.png', application='firefox')))

time.sleep(2)
# from_location = Location(1980, 160)
# to_location = Location(1980, 50)
# Mouse().drag_and_drop(from_location, to_location)
Mouse().scroll_down(400, 3)




