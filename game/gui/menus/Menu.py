#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Documentation: Menu.py
  Classes and functions:
    Menu main class of this modul
  Description:
    the base class for the menus. All other menu classes should be derived from this
    one
"""

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DirectLabel
from direct.gui.DirectGui import DirectButton
from panda3d.core import TextNode

import time

class Menu(DirectObject):
    def __init__(self):
        """Default constructor"""
        # load the default fonts
        #self.defaultFont = loader.loadFont("gui/fonts/UbuntuBold")
        #self.defaultFontRegular = loader.loadFont("gui/fonts/UbuntuRegular")
        # load the default button image map
        self.defaultBtnMaps = base.loader.loadModel(
            "gui/buttons/mainMenu/button_maps")

        # this button can be created with the createBackButton function
        self.btnBack = None

        self.frameMain = DirectFrame(
            # size of the frame
            frameSize = (base.a2dLeft, base.a2dRight,
                         base.a2dTop, base.a2dBottom),
            # position of the frame
            pos = (0, 0, 0),
            # tramsparent bg color
            frameColor = (0, 0, 0, 0))

        self.title = DirectLabel(
            scale = 0.25,
            pos = (0, 0, -0.25),
            frameColor = (0, 0, 0, 0),
            text = "Missing Title",
            text_align = TextNode.ACenter,
            text_fg = (1,1,1,1),
            #text_font = self.defaultFont
            )
        self.title.reparentTo(base.a2dTopCenter)

        self.clock = DirectLabel(
            scale = 0.1,
            pos = (-.1,0,.1),
            frameColor = (0, 0, 0, 0),
            text = "00:00",
            text_align = TextNode.ARight,
            text_fg = (1,1,1,1))
        self.clock.reparentTo(base.a2dBottomRight)


        self.hide()

    def showBase(self):
        """Show all GUI controls of the base menu"""
        self.accept("RatioChanged", self.recalcAspectRatio)
        self.frameMain.show()
        self.clock.show()
        self.title.show()
        if self.btnBack:
            self.btnBack.show()
        if not taskMgr.hasTaskNamed("clock"):
            taskMgr.add(self.clockTask, "clock")

    def hideBase(self):
        """Hide all GUI controls of the base menu"""
        self.ignore("RatioChanged")
        self.frameMain.hide()
        self.clock.hide()
        self.title.hide()
        if self.btnBack:
            self.btnBack.hide()
        if taskMgr.hasTaskNamed("clock"):
            taskMgr.remove("clock")

    def createBackButton(self, func):
        """Create the back button on the bottom left edge of the window"""
        self.btnBack = DirectButton(
            # size of the button
            scale = (0.25, 0.25, 0.25),
            # size of the text
            text_scale = (0.5*1.33, 0.5, 0.5),
            # the text on the button
            text = "ABC",
            # set the alignment to right
            text_align = TextNode.ARight,
            # put the text on the left side of the button
            text_pos = (4.1, -0.15),
            # set the text color to white
            text_fg = (1,1,1,1),
            # set the font of the text
            #text_font = self.defaultFont,
            # set the buttons images
            geom = (self.defaultBtnMaps.find("**/button_ready"),
                    self.defaultBtnMaps.find("**/button_click"),
                    self.defaultBtnMaps.find("**/button_rollover"),
                    self.defaultBtnMaps.find("**/button_disabled")),
            # set no relief
            relief = 1,
            # make it transparent
            frameColor = (0,0,0,0),
            # No sink in when press
            pressEffect = False,
            # position on the window
            pos = (0.0, 0, 0.2),
            # the event which is thrown on clickSound
            command = func,
            # sounds that should be played
            rolloverSound = None,
            clickSound = None)
        self.btnBack.reparentTo(base.a2dBottomLeft)

    def clockTask(self, task):
        self.clock["text"] = time.strftime("%H:%M")
        return task.cont

    def recalcAspectRatio(self):
        """get the new aspect ratio to resize the mainframe"""
        self.frameMain["frameSize"] = (
            base.a2dLeft, base.a2dRight,
            base.a2dTop, base.a2dBottom)
