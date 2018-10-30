class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print ""
print bcolors.OKBLUE + "Testing Libraries imports" + bcolors.ENDC
print ""

try:
    import mozrunner
    import mozdownload
    import mozinstall
    import mozinfo
    import mozversion
    import pyautogui
    import pytesseract
    import mss
    import cv2
    import os
    import sys
except ImportError as e:
    print bcolors.FAIL + "ERROR" + bcolors.ENDC
    print e
else:
    print bcolors.BOLD + bcolors.OKGREEN + "All libraries imports succeeded." + bcolors.ENDC


print ""
print "_____________________________________________________________________________________"
print ""
print bcolors.OKBLUE + "Testing Mozdownload" + bcolors.ENDC
print ""

try:
    from mozdownload import FactoryScraper

    scraper = FactoryScraper('daily')
    print scraper.url
    print scraper.filename
except (IOError, OSError) as e:
    print bcolors.FAIL + "ERROR" + bcolors.ENDC
    print e
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
else:
    print ""
    print "Version: " + mozdownload.__version__
    print ""
    print bcolors.BOLD + bcolors.OKGREEN + "Mozdownload working correctly." + bcolors.ENDC


print "_____________________________________________________________________________________"
print ""
print bcolors.OKBLUE + "Testing Mozrunner" + bcolors.ENDC
print ""

try:
    print "Importing FirefoxRunner"
    from mozprofile import FirefoxProfile
    from mozrunner import FirefoxRunner
except ImportError as e:
    print bcolors.FAIL + "ERROR" + bcolors.ENDC
    print e
else:
    print ""
    print bcolors.BOLD + bcolors.OKGREEN + "Mozrunner working correctly." + bcolors.ENDC


print "_____________________________________________________________________________________"
print ""
print bcolors.OKBLUE + "Testing OpenCV" + bcolors.ENDC
print ""

try:
    cv2.__version__
except (IOError, OSError) as e:
    print bcolors.FAIL + "ERROR" + bcolors.ENDC
    print e
else:
    print "Version: " + cv2.__version__
    print("")
    print bcolors.BOLD + bcolors.OKGREEN + "OpenCV working correctly." + bcolors.ENDC


print "_____________________________________________________________________________________"
print ""
print bcolors.OKBLUE + "Testing PyAutoGui" + bcolors.ENDC
print ""

print bcolors.OKBLUE + "Testing PyAutoGui screenshot" + bcolors.ENDC
try:
    pyautogui.screenshot()
    print pyautogui.screenshot()
except (IOError, OSError) as e:
    print bcolors.FAIL + "ERROR" + bcolors.ENDC
    print e
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

print bcolors.OKBLUE + "Testing PyAutoGui keyboard" + bcolors.ENDC
try:
    pyautogui.typewrite('')
    print pyautogui.typewrite('')
except (IOError, OSError) as e:
    print bcolors.FAIL + "ERROR" + bcolors.ENDC
    print e
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

print bcolors.OKBLUE + "Testing PyAutoGui mouse" + bcolors.ENDC
try:
    pyautogui.position()
    print pyautogui.position()
except (IOError, OSError) as e:
    print bcolors.FAIL + "ERROR" + bcolors.ENDC
    print e
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
else:
    print "Version: " + pyautogui.__version__
    print ""
    print bcolors.BOLD + bcolors.OKGREEN + "PyAutoGui working correctly." + bcolors.ENDC

print ""
print "_____________________________________________________________________________________"
print ""
print bcolors.OKBLUE + "Testing MSS" + bcolors.ENDC
print ""

print bcolors.OKBLUE + "Testing MSS screenshot" + bcolors.ENDC
try:
    with mss.mss() as sct:
        filename = sct.shot(mon=-1, output='mss_fullscreen.png')
    print (filename)
    print ("Removing the MSS screenshot.")
    import os
    os.remove('mss_fullscreen.png')
except (IOError, OSError) as e:
    print bcolors.FAIL + "ERROR" + bcolors.ENDC
    print e
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
else:
    print ""
    print "Version: " + mss.__version__
    print ""
    print bcolors.BOLD + bcolors.OKGREEN + "MSS working correctly." + bcolors.ENDC


print "_____________________________________________________________________________________"
print ""
print bcolors.OKBLUE + "Testing Pytesseract" + bcolors.ENDC
print ""

try:
    print "pytesseract.get_tesseract_version()"
    print pytesseract.get_tesseract_version()
except (IOError, OSError) as e:
    print bcolors.FAIL + "ERROR" + bcolors.ENDC
    print e
else:
    print("")
    print bcolors.BOLD + bcolors.OKGREEN + "Pytesseract working correctly." + bcolors.ENDC
