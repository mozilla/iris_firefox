from core.screen.screen import Screen
from core.image_search.pattern import Pattern
from core.image_search.finder import find_all, find, wait

screen = Screen(1)
print(screen.find(Pattern('test.png', application='firefox')))
