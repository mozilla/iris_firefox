from core.screen.screen import Screen
from core.image_search.pattern import Pattern
from core.image_search.finder import find_all, find, wait, match_template
from core.screen.region import Region
from core.enums import MatchTemplateType


region = Region(1920, 0, 300, 500)
# region.highlight()
print(region.find_all(Pattern('test.png', application='firefox')))


