#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Documentation: .py
  Classes and functions:
    N.A.
  Description:
    This is the main settings class. All other settings classes are derived
    from this one
"""

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

import logging
import os
import tempfile
import ConfigParser
from panda3d.core import Filename
from panda3d.core import ConfigPageManager
from panda3d.core import OFileStream
from pandac.PandaModules import loadPrcFile


class Settings:
    """Settings class contains as the classname says all settings variables,
    all properties and also holds variables which should accessable through
    the game."""


    def __init__(self):
        self.join = os.path.join
        self.home = os.path.expanduser("~")
        self.__set_defaults()


    def __set_defaults(self):
        """Set default values for all settings variables"""

        # pathnames to all the directories and files needed by this game
        # temp path of the OS
        self.appNameHidden = r"." + appName
        self.tmpPath = Filename.fromOsSpecific(os.path.join(tempfile.gettempdir(), appName))
        self.settingsPath = self.join(self.home, self.appNameHidden) + os.sep
        self.settingsFile = self.join(self.settingsPath, r"settings.cfg")
        self.prcFile = self.join(self.settingsPath, r"config.prc")
        # create the users main directory if it doesn't exist already
        self.checkPathExistance(self.settingsPath)
        # if the Rising specific panda config file does not exist,
        # create and load it here.
        if not os.path.exists(self.prcFile):
            cpMgr = ConfigPageManager.getGlobalPtr()
            page = cpMgr.makeExplicitPage("Rising Pandaconfig")
            page.makeDeclaration("window-title", "Rising")
            configfile = OFileStream(self.prcFile)
            page.write(configfile)
            configfile.close()
            loadPrcFile(Filename.fromOsSpecific(self.prcFile))

        # Player interaction start
        self.playerKeys = {"forward": ["w", "shift-w"],
                      "left": ["a", "shift-a"],
                      "right": ["d", "shift-d"],
                      "backward": ["s", "shift-s"],
                      "run": ["shift"],
                      "jump": ["space", "shift-space"],
                      "cam_left": ["page_down", "shift-page_down"],
                      "cam_right": ["delete", "shift-delete"],
                      "cam_up": ["home", "shift-home"],
                      "cam_down": ["end", "shift-end"],
                      "cam_center": ["page_up", "shift-page_up"],
                      "action": ["e", "shift-e"],
                      "inteligentAction": ["rcontrol", "shift-rcontrol", "mouse1"],
                      "special": ["arrow_up", "shift-arrow_up", "mouse3"],
                      "special_left": ["arrow_left", "shift-arrow_left", "wheel_up"],
                      "special_right": ["arrow_right", "shift-arrow_right", "wheel_down"],
                      "special_flip": ["arrow_down", "shift-arrow_down"],
                      "cam_zoomIn": ["=", "shift-="],
                      "cam_zoomOut": ["-", "shift--"]}

        # Logging
        self.__LOGGING_LEVELS = {"critical": logging.CRITICAL,
                            "error": logging.ERROR,
                            "warning": logging.WARNING,
                            "info": logging.INFO,
                            "debug": logging.DEBUG}
        self.logPath = self.settingsPath
        self.logFileNout = self.join(self.logPath, r"out.log")
        self.logFile = self.join(self.logPath, r"out_debug.log")
        self.logFormatString = "%(asctime)s %(levelname)s: %(message)s"
        self.logDateTimeFormatString = "%d-%m-%Y %H:%M:%S"
        self.logLevel = self.__LOGGING_LEVELS["debug"]

        # Grafics start
        self.windowSize = [800, 600]
        self.fullscreen = False
        self.graphicquality = 0

        # sound options
        self.muted = False
        self.volume = 1.0

        # Internationalisation and Localisation
        self.selectedLanguage = "en-US"

        # Physics
        self.gravity_x = 0.0
        self.gravity_y = 0.0
        self.gravity_z = -9.81

    def checkPathExistance(self, path):
        """Check if the given directory exists and if not creat it"""
        if not os.path.exists(path):
            os.makedirs(path)

    def readConfig(self):
        #
        # Load the config file if it exist
        #
        if not os.path.exists(Settings.settingsFile): return
        config = ConfigParser.RawConfigParser()
        config.readfp(open(Settings.settingsFile))

        #
        # Player section
        #
        section = "player"
        # get the player control keys
        tmpKeys = self.playerKeys
        self.playerKeys = eval(config.get(section, "keybindings"))
        # now check if any key is in the loaded map
        for key in tmpKeys.keys():
            if not key in self.playerKeys:
                self.playerKeys[key] = tmpKeys[key]

        #
        # Audio section
        #
        section = "audio"
        # try to load the mute state of the sound in the game
        tmpMuted = self.muted
        try:
            self.muted = config.getboolean(section, "muted")
        except:
            self.muted = tmpMuted
        # try to load the volume and set it to default if something failed
        tmpVolume = Settings.volume
        try:
            Settings.volume = config.getfloat(section, "volume")
            if self.volume < 0.0 or Settings.volume > 1.0:
                self.volume = tmpVolume
        except:
            self.volume = tmpVolume

        #
        # Graphic section
        #
        section = "graphic"
        # get the window size
        tmpWinSize = Settings.windowSize
        self.windowSize = eval(config.get(section, "windowSize"))
        # check if we have the to dimensions x/y and not more or less
        if len(self.windowSize) != 2:
            self.windowSize = tmpWinSize
        # try to load the fullscreen state of the application and set
        # it to it's default if something failed
        tmpFullscreen = self.fullscreen
        try:
            self.fullscreen = config.getboolean(section, "fullscreen")
        except:
            self.fullscreen = tmpFullscreen
        # try to load the graphic quality and
        # set it to default if something failed
        tmpGraphicQuality = Settings.graphicquality
        try:
            self.graphicquality = config.getint(section, "graphicquality")
            if self.graphicquality < 0 or Settings.graphicquality > 99:
                self.graphicquality = tmpGraphicQuality
        except:
            self.graphicquality = tmpGraphicQuality

        #
        # Language section
        #
        section = "multilingual"
        self.selectedLanguage = config.get(section, "language")

        # load the config file for this game
        if os.path.exists(self.prcFile):
            loadPrcFile(self.prcFile)


    def writeConfig(self):
        config = ConfigParser.RawConfigParser()

        section = "player"
        config.add_section(section)
        config.set(section, "keybindings", self.playerKeys)

        section = "audio"
        config.add_section(section)
        config.set(section, "Muted", self.muted)
        config.set(section, "Volume", self.volume)

        section = "graphic"
        config.add_section(section)
        config.set(section, "windowSize", self.windowSize)
        config.set(section, "fullscreen", self.fullscreen)
        config.set(section, "graphicquality", self.graphicquality)

        config.add_section("multilingual")
        config.set("multilingual", "Language", self.selectedLanguage)

        with open(Settings.settingsFile, "wb") as configfile:
            config.write(configfile)

