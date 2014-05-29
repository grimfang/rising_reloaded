#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Documentation: .py
  Classes and functions:
    N.A.
  Description:
    This class creates the menu, which appears when a player want to join a
    game on one of the found servers
"""

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from menus.Menu import Menu
from direct.gui.DirectGui import DirectButton
from direct.actor.Actor import Actor


class MenuStartGame(Menu):

    def __init__(self):
        self.charA = None
        self.charB = None
        Menu.__init__(self)

        self.charSelectBtnMaps = base.loader.loadModel(
            "gui/buttons/charSelection/button_maps.bam")

        self.btnCharA = DirectButton(
            # size of the button
            scale = (2.5, 1, 1.6),
            # size of the text
            #text_scale = (0.5*1.33, 0.5, 0.5),
            # the text on the button
            text = "",
            # set no relief
            relief = 1,
            frameColor = (0,0,0,0),
            # No sink in when press
            pressEffect = False,
            # set the buttons images
            geom = (self.charSelectBtnMaps.find("**/char_ready"),
                    self.charSelectBtnMaps.find("**/char_click"),
                    self.charSelectBtnMaps.find("**/char_rollover"),
                    self.charSelectBtnMaps.find("**/char_disabled")),
            # position on the window
            pos = (-1, 0, 0),
            # the event which is thrown on clickSound
            command = self.btnCharA_Click,
            # sounds that should be played
            rolloverSound = None,
            clickSound = None)
        self.btnCharA.setTransparency(1)

        self.btnCharB = DirectButton(
            # size of the button
            scale = (2.5, 1, 1.6),
            # size of the text
            text_scale = (0.5*1.33, 0.5, 0.5),
            # the text on the button
            text = "",
            # set no relief
            relief = 1,
            frameColor = (0,0,0,0),
            # No sink in when press
            pressEffect = False,
            # set the buttons images
            geom = (self.charSelectBtnMaps.find("**/char_ready"),
                    self.charSelectBtnMaps.find("**/char_click"),
                    self.charSelectBtnMaps.find("**/char_rollover"),
                    self.charSelectBtnMaps.find("**/char_disabled")),
            # position on the window
            pos = (1, 0, 0),
            # the event which is thrown on clickSound
            command = self.btnCharB_Click,
            # sounds that should be played
            rolloverSound = None,
            clickSound = None)
        self.btnCharB.setTransparency(1)
        self.btnCharB["state"] = 0

        # add every item to the mainframe
        self.btnCharA.reparentTo(self.frameMain)
        self.btnCharB.reparentTo(self.frameMain)

        self.charA = Actor("models/avatars/AvatarA/Avatar1.bam",
              {"idle": "models/avatars/AvatarA/Avatar1-Idle.bam"})
        self.charA.setScale(0.30)
        self.charA.setPos(-1, 4, -0.5)
        self.charA.reparentTo(camMgr.activeCameras["menuCam"].camNP)
        self.charA.setPlayRate(0.5, "idle")
        self.charA.loop("idle")

        self.charB = Actor("models/avatars/AvatarB/avatar.bam",
              {"idle": "models/avatars/AvatarB/avatar-Idle.bam"})
        self.charB.setScale(0.10)
        self.charB.setPos(1, 4, 0)
        self.charB.reparentTo(camMgr.activeCameras["menuCam"].camNP)
        self.charB.loop('idle')

        self.createBackButton(self.btnBack_Click)

        # set the text of all GUI elements
        self.setText()

        self.hideBase()

        self.accept("LanguageChanged", self.setText)

    def show(self):
        self.title["text"] = _("Select your Character")
        self.showBase()

    def hide(self):
        self.hideBase()
        if self.charA:
            self.charA.hide()
        if self.charB:
            self.charB.hide()

    def setText(self):
        self.title["text"] = _("Select your Character")
        self.btnBack["text"] = _("Back")

    def btnBack_Click(self):
        # throw event to go back to the main menu
        base.messenger.send("StartGameMenu_back")

    def btnCharA_Click(self):
        # throw event to select Character A for the game
        base.messenger.send("StartGameMenu_CharacterA")

    def btnCharB_Click(self):
        # throw event to select Character B for the game
        base.messenger.send("StartGameMenu_CharacterB")
