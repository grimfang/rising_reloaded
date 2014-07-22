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

        self.loadMusic()
        self.menu = MenuMain()
        self.optionsmenu = MenuOptions(self.main.engine)
        self.menuBG = MenuBG()
        self.hud = PlayerHUD()
        self.startMenu()


        #Accept a special game event to be able to return to the menu
        self.accept("Quit", self.startMenu)

        # Add GameLoop Task
        taskMgr.add(self.gameLoop, "Game_loop")

    def startMenu(self):
        self.hud.hide()
        self.showMainMenu()
        self.menuBG.startBGLoop()
        self.acceptEvents()
        if self.main.engine.audioMgr.isMusicPlaying("main"):
            self.main.engine.audioMgr.stopMusic("main")
        if not self.main.engine.audioMgr.isMusicPlaying("menu"):
            self.main.engine.audioMgr.playMusic("menu")

    def loadMusic(self):
        self.main.engine.audioMgr.addMusic("menu", "menu.ogg")
        self.main.engine.audioMgr.addMusic("main", "main.ogg")
        self.main.engine.audioMgr.addMusic("boss", "boss.ogg")

    def showMainMenu(self):
        self.menu.show()
        if not self.main.engine.audioMgr.isMusicPlaying("menu"):
            self.main.engine.audioMgr.playMusic("menu")

    def hideMainMenu(self):
        self.menu.hide()

    def showOptions(self):
        self.hideMainMenu()
        self.optionsmenu.show()
        if not self.main.engine.audioMgr.isMusicPlaying("menu"):
            self.main.engine.audioMgr.playMusic("menu")

    def hideOptions(self):
        self.optionsmenu.hide()
        self.showMainMenu()

    def startGame(self):
        self.menu.hide()
        self.menuBG.stopBGLoop()
        self.hud.show()
        self.ignoreEvents()
        self.main.engine.loadLevel(self.menu.selectedLevel)
        self.main.engine.start()
        if self.main.engine.audioMgr.isMusicPlaying("menu"):
            self.main.engine.audioMgr.stopMusic("menu")
        if not self.main.engine.audioMgr.isMusicPlaying("main"):
            self.main.engine.audioMgr.playMusic("main")

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
        self.ignore("MainMenu_optionsMain")
        self.ignore("OptMenu_back")
        self.ignore("MainMenu_quitMain")

    def gameLoop(self, task):

        dt = globalClock.getDt()

        return task.cont
















