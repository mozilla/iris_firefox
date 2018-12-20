from core.screen.region import Region

region = Region(0, 50, 300, 200)
# region.highlight()
# print(region.double_click(Pattern('test.png', application='firefox')))
print(region.exists('Project', 'Word found'))






