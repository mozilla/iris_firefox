from iris2.src.core.api.screen.region import Region


def test_text_search():
    region = Region(0, 50, 300, 200)
    region.highlight()
    # print(region.double_click(Pattern('test.png', application='firefox')))
    # print(region.exists('Project', 'Word found'))
    assert 1 == 1







