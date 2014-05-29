#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Documentation: .py
  Classes and functions:
    N.A.
  Description:
    this class handles the main menu seen on startup.
"""

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from menus.Menu import Menu
from direct.gui.DirectGui import DirectButton
from panda3d.core import TextNode

class MenuMain(Menu):

    def __init__(self):
        Menu.__init__(self)

        screenResMultiplier = 1.33

        self.btnStart = DirectButton(
            # size of the button
            scale = (0.25, 0.25, 0.25),
            # some temp text
            text = "ABC",
            # size of the text
            text_scale = (0.5*screenResMultiplier, 0.5, 0.5),
            # set the alignment to right
            text_align = TextNode.ARight,
            # put the text on the right side of the button
            text_pos = (4.1, -0.15),
            # set the text color to white
            text_fg = (1,1,1,1),
            # set the font of the text
            text_font = self.defaultFont,
            # set the buttons images
            geom = (self.defaultBtnMaps.find("**/button_ready"),
                    self.defaultBtnMaps.find("**/button_click"),
                    self.defaultBtnMaps.find("**/button_rollover"),
                    self.defaultBtnMaps.find("**/button_disabled")),
            # set no relief
            relief = 1,
            frameColor = (0,0,0,0),
            # No sink in when press
            pressEffect = False,
            # position on the window
            pos = (-1, 0, .55),
            # the event which is thrown on clickSound
            command = self.btnStart_Click,
            # sounds that should be played
            rolloverSound = None,
            clickSound = None)
        self.btnStart.setTransparency(1)

        self.btnOptions = DirectButton(
            scale = (0.25, 0.25, 0.25),
            # some temp text
            text = "ABC",
            text_scale = (0.45*screenResMultiplier, 0.45, 0.45),
            # set the alignment to right
            text_align = TextNode.ARight,
            # put the text on the right side of the button
            text_pos = (4.1, -0.15),
            # set the text color to white
            text_fg = (1,1,1,1),
            # set the font of the text
            text_font = self.defaultFont,
            # set the buttons images
            geom = (self.defaultBtnMaps.find("**/button_ready"),
                    self.defaultBtnMaps.find("**/button_click"),
                    self.defaultBtnMaps.find("**/button_rollover"),
                    self.defaultBtnMaps.find("**/button_disabled")),
            relief = 1,
            frameColor = (0,0,0,0),
            pressEffect = False,
            pos = (-1.5, 0, .15),
            command = self.btnOptions_Click,
            rolloverSound = None,
            clickSound = None)
        self.btnOptions.setTransparency(1)

        self.btnQuit = DirectButton(
            scale = (0.25, 0.25, 0.25),
            # some temp text
            text = "ABC",
            text_scale = (0.5*screenResMultiplier, 0.5, 0.5),
            # set the alignment to right
            text_align = TextNode.ARight,
            # put the text on the right side of the button
            text_pos = (4.1, -0.15),
            # set the text color to white
            text_fg = (1,1,1,1),
            # set the font of the text
            text_font = self.defaultFont,
            # set the buttons images
            geom = (self.defaultBtnMaps.find("**/button_ready"),
                    self.defaultBtnMaps.find("**/button_click"),
                    self.defaultBtnMaps.find("**/button_rollover"),
                    self.defaultBtnMaps.find("**/button_disabled")),
            relief = 1,
            frameColor = (0,0,0,0),
            pressEffect = False,
            pos = (-1.75, 0, -.25),
            command = self.btnQuit_Click,
            rolloverSound = None,
            clickSound = None)
        self.btnQuit.setTransparency(1)

        self.btnStart.reparentTo(self.frameMain)
        self.btnOptions.reparentTo(self.frameMain)
        self.btnQuit.reparentTo(self.frameMain)

        self.recalcAspectRatio()

        # set the text of all GUI elements
        self.setText()

        # hide all buttons at startup
        self.hideBase()

        self.accept("LanguageChanged", self.setText)

    def show(self):
        self.title["text"] = _("Main Menu")
        self.showBase()

    def hide(self):
        self.hideBase()

    def setText(self):
        self.title["text"] = _("Main Menu")
        self.btnStart["text"] = _("Start")
        self.btnOptions["text"] = _("Options")
        self.btnQuit["text"] = _("Quit")

    def btnStart_Click(self):
        base.messenger.send("MainMenu_startGame")

    def btnOptions_Click(self):
        base.messenger.send("MainMenu_optionsMain")

    def btnQuit_Click(self):
        base.messenger.send("MainMenu_quitMain")
