#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Documentation: .py
  Classes and functions:
    N.A.
  Description:
    This class handles the menu which appears when the player hits the pause
    button inside a running game.
"""

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from menus.Menu import Menu
from direct.gui.DirectGui import DirectButton
from panda3d.core import TextNode

class MenuPause(Menu):

    def __init__(self):
        Menu.__init__(self)
        self.frameMain.setTransparency(True)
        self.frameMain.frameColor = (0.25, 0, 1, 0.25)

        screenResMultiplier = 1.33

        self.btnReturn = DirectButton(
            # size of the button
            scale = (0.25, 0.25, 0.25),
            # some temp text
            text = "ABC",
            # size of the text
            text_scale = (0.5*screenResMultiplier, 0.5, 0.5),
            # set the alignment to center
            text_align = TextNode.ACenter,
            # put the text on the left side of the button
            text_pos = (0, -0.15),
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
            pos = (0, 0, .25),
            # the event which is thrown on clickSound
            command = self.btnReturn_Click,
            # sounds that should be played
            rolloverSound = None,
            clickSound = None)
        self.btnReturn.setTransparency(1)

        self.btnQuit = DirectButton(
            scale = (0.25, 0.25, 0.25),
            # some temp text
            text = "ABC",
            text_scale = (0.5*screenResMultiplier, 0.5, 0.5),
            # set the alignment to center
            text_align = TextNode.ACenter,
            # put the text on the left side of the button
            text_pos = (0, -0.15),
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
            pos = (0, 0, -.25),
            command = self.btnQuit_Click,
            rolloverSound = None,
            clickSound = None)
        self.btnQuit.setTransparency(1)

        self.btnReturn.reparentTo(self.frameMain)
        self.btnQuit.reparentTo(self.frameMain)

        self.recalcAspectRatio()

        # set the text of all GUI elements
        self.setText()

        self.hideBase()

    def show(self):
        self.title["text"] = _("Pause")
        self.showBase()

    def hide(self):
        self.hideBase()

    def setText(self):
        self.title["text"] = _("Main Menu")
        self.btnReturn["text"] = _("Return")
        self.btnQuit["text"] = _("Quit")

    def btnReturn_Click(self):
        base.messenger.send("PauseMenu_return")

    def btnQuit_Click(self):
        base.messenger.send("PauseMenu_quit")
