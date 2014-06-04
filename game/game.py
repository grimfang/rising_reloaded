#!/usr/bin/python

#----------------------------------------------------------------------#
# The MIT License (MIT)
# See the license.txt for license information
#----------------------------------------------------------------------#

"""@ package Game

Start the Game.
"""

# System Imports
import logging as log
import __builtin__

# set the application Name
__builtin__.appName = "Rising"

# Panda Engine Imports
from direct.showbase.DirectObject import DirectObject

# MeoTech Imports
from gui.playerHUD import PlayerHUD
from gui.menus.MenuBG import MenuBG
from gui.menus.MenuMain import MenuMain
from gui.menus.MenuOptions import MenuOptions


#----------------------------------------------------------------------#

# Game
class Game(DirectObject):
    """The Game handles the actual game and custom scripts.
    """
    def __init__(self, _main):

        print "Game - init >>>"

        # Meotech
        self.main = _main

        self.menu = MenuMain()
        self.showMainMenu()
        self.optionsmenu = MenuOptions(self.main.engine)
        self.menuBG = MenuBG()
        self.menuBG.startBGLoop()

        self.acceptEvents()

        # Add GameLoop Task
        taskMgr.add(self.gameLoop, "Game_loop")

    def showMainMenu(self):
        self.menu.show()

    def hideMainMenu(self):
        self.menu.hide()

    def showOptions(self):
        self.hideMainMenu()
        self.optionsmenu.show()

    def hideOptions(self):
        self.optionsmenu.hide()
        self.showMainMenu()

    def startGame(self):
        self.menu.hide()
        self.menuBG.stopBGLoop()
        self.hud = PlayerHUD()
        self.main.engine.loadLevel("DevDemo")
        self.main.engine.start()

    def quitGame(self):
        self.menu.hide()
        self.ignoreEvents()
        self.main.quit()

    def acceptEvents(self):
        self.accept("MainMenu_startGame", self.startGame)
        self.accept("MainMenu_optionsMain", self.showOptions)
        self.accept("OptMenu_back", self.hideOptions)
        self.accept("MainMenu_quitMain", self.quitGame)

    def ignoreEvents(self):
        self.ignore("MainMenu_startGame")
        #self.ignore("MainMenu_optionsMain")
        self.ignore("MainMenu_quitMain")

    def gameLoop(self, task):

        dt = globalClock.getDt()

        return task.cont
















