from core.screen.screen import Screen
from core.image_search.pattern import Pattern

print(Screen(1).wait(Pattern('test.png', application='firefox'), 10))