# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import ConfigParser
import glob
import os
import struct


class FirefoxApp(object):
    """Class holding information about an extracted Firefox application directory"""

    __locations = {
        "osx": {
            "base": os.path.join("*", "*.app"),
            "exe": os.path.join("Contents", "MacOS", "firefox"),
            "browser": os.path.join("Contents", "Resources", "browser"),
            "gredir": os.path.join("Contents", "Resources"),
            "ini": os.path.join("Contents", "Resources", "application.ini"),
        },
        "linux": {
            "base": "firefox",
            "exe": "firefox",
            "browser": "browser",
            "gredir": "",
            "ini": "application.ini",
        },
        "win": {
            "base": "core",
            "exe": "firefox.exe",
            "browser": "browser",
            "gredir": "",  # FIXME: this may be wrong
            "ini": "application.ini",
        },
    }

    def __init__(self, directory):

        # Assuming that directory points to a directory
        # where a stock Firefox archive was extracted.
        self.platform = None
        self.app_dir = None
        for platform in self.__locations:
            base = self.__locations[platform]["base"]
            matches = glob.glob(os.path.join(directory, base))
            if len(matches) == 0:
                continue
            elif len(matches) >= 1:
                if os.path.isdir(matches[0]):
                    self.platform = platform
                    self.app_dir = matches[0]
                    break
            raise Exception("Unsupported application package format (missing or ambiguous base folder)")

        if self.platform is None:
            raise Exception("Unsupported application package platform")

        # Fill in the rest of the package locations
        self.exe = os.path.join(self.app_dir, self.__locations[self.platform]["exe"])
        self.browser = os.path.join(self.app_dir, self.__locations[self.platform]["browser"])
        self.gredir = os.path.join(self.app_dir, self.__locations[self.platform]["gredir"])
        self.app_ini = os.path.join(self.app_dir, self.__locations[self.platform]["ini"])

        # Sanity checks
        if not os.path.isfile(self.exe) or not os.path.isdir(self.browser):
            raise Exception("Unsupported application package format (missing files)")

        # For `linux`: byte 4 in ELF header is 01/02 for 32/64 bit
        if self.platform == "linux":
            with open(self.exe) as f:
                head = f.read(5)
            if head[4] == '\x01':
                self.platform = "linux32"
            elif head[4] == '\x02':
                self.platform = "linux"
            else:
                raise Exception("Unsupported ELF binary (%s)" % ord(head[4]))
        # Windows PE header offset is at 0x3c. Bytes 4 and 5 there tell 32 from 64 bit
        elif self.platform == "win":
            with open(self.exe) as f:
                try:
                    f.seek(0x3c)
                    pe_header_offset = struct.unpack("<I", f.read(4))[0]
                    f.seek(pe_header_offset)
                    pe_sig, machine_type = struct.unpack("<4sH", f.read(6))
                except struct.error:
                    # Definitely invalid
                    pe_sig, machine_type = (b'', 0)
                if (pe_sig, machine_type) == (b"PE\x00\x00", 0x14c):
                    self.platform = "win32"
                elif (pe_sig, machine_type) == (b"PE\x00\x00", 0x8664):
                    self.platform = "win"
                else:
                    raise Exception("Unsupported PE binary format")

        # Determine Firefox version
        ini_parser = ConfigParser.SafeConfigParser()
        ini_parser.read(self.app_ini)
        self.application_ini = dict(ini_parser.items("App"))
        self.version = ini_parser.get("App", "Version")
        # For versions that have no `CodeName` specified, extract it from the repo name.
        try:
            self.release = ini_parser.get("App", "CodeName")
        except ConfigParser.NoOptionError:
            self.release = ini_parser.get("App", "sourcerepository").split("-")[-1]

        # Field for optional package origin metadata (must be provided externally)
        self.package_origin = None
