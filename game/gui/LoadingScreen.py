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

from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DirectWaitBar
from direct.gui.DirectGui import DirectLabel
from panda3d.core import TextNode

class LoadingScreen():
    def __init__(self):
        self.defaultFont = loader.loadFont("gui/fonts/UbuntuBold.bam")

        # a fill panel so the player doesn't see how everything
        # gets loaded in the background
        self.frameMain = DirectFrame(
            # size of the frame
            frameSize = (base.a2dLeft, base.a2dRight,
                         base.a2dTop, base.a2dBottom),
            # position of the frame
            #pos = (0, 0, 0),
            # tramsparent bg color
            frameColor = (0.05, 0.1, 0.25, 1))

        # the text Loading... on top
        self.lblLoading = DirectLabel(
            scale = 0.25,
            pos = (0, 0, 0.5),
            frameColor = (0, 0, 0, 0),
            text = "Loading...",
            text_align = TextNode.ACenter,
            text_fg = (1,1,1,1),
            text_font = self.defaultFont)
        self.lblLoading.reparentTo(self.frameMain)

        # the waitbar on the bottom
        self.wbLoading = DirectWaitBar(
            text = "0%",
            text_fg = (1,1,1,1),
            text_font = self.defaultFont,
            value = 100,
            pos = (0, 0, -0.5),
            barColor = (0, 0, 1, 1))
        self.wbLoading.reparentTo(self.frameMain)

        self.setText()
        self.hide()

    def show(self):
        # make sure, the frame fill in the whole screen
        self.frameMain["frameSize"] = (
            base.a2dLeft, base.a2dRight,
            base.a2dTop, base.a2dBottom)
        # ensure the texts are translated
        self.setText()
        # now show the main frame
        self.frameMain.show()
        # and render two frames so the loading screen
        # is realy shown on screen
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()

    def hide(self):
        self.frameMain.hide()

    def setLoadingValue(self, value):
        """Set the waitbar value to the given value, where
        value has to be a integer from 0 to 100"""
        if value > 100: value = 100
        if value < 0: value = 0
        self.wbLoading["value"] = value
        self.wbLoading["text"] = "{0}%".format(value)
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()

    def setText(self):
        self.lblLoading["text"] = _("Loading...")
