from applications.firefox.app import FirefoxApp


def run_firefox():
    FirefoxApp.launch_firefox(path='/usr/bin/firefox')
