from src.core.api.screen.region import Region


def test_text_search():
    region = Region(0, 40, 200, 100)
    region.highlight()
    # print(region.double_click(Pattern('test.png', application='firefox')))
    # print(region.exists('Project', 'Word found'))
    print(region.exists('Search a very'))
    assert 1 == 1







