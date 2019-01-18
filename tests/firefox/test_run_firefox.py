from targets.firefox.app import Target
from targets.firefox.profile import FirefoxProfile


brand_new = FirefoxProfile.BRAND_NEW

profile = FirefoxProfile()
app = Target()

session = app.firefox_session(path=app.path, profile=profile.make_profile(brand_new))
session.start()
