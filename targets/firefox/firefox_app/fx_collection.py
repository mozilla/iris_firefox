from targets.firefox.firefox_app.fx_browser import FirefoxApp, normalize_str


class FirefoxCollection:
    def __init__(self):
        self.fx_collection = {}

    def add(self, version, locale):
        fx_browser_key = 'firefox{}{}'.format(normalize_str(version), normalize_str(locale))
        self.fx_collection[fx_browser_key] = FirefoxApp(version=version, locale=locale)

    def get(self, version, locale):
        fx_browser_key = 'firefox{}{}'.format(normalize_str(version), normalize_str(locale))
        return self.fx_collection.get(fx_browser_key)


FX_Collection = FirefoxCollection()
