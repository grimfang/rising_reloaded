#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Documentation: DebugConsole.py
    this class provides a console and head-up-display for debuging informations
"""

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectWaitBar, DirectFrame
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import LerpHprInterval
from direct.gui.DirectGui import DirectLabel
from panda3d.core import TextNode

class PlayerHUD(DirectObject):
    def __init__(self):
        #
        # Player status section
        #
        self.frameCharStatus = DirectFrame(
            # size of the frame
            frameSize = (0, .5,
                         -.15, 0),
            # bg color Transparent
            frameColor = (1, 0, 0, .5))
        self.frameCharStatus.reparentTo(base.a2dTopLeft)
        self.statusStamina = DirectWaitBar(
            text = "",
            value = 100,
            frameSize = (0.145, .5, -0.02, 0),
            pos = (0, 1, -0.05),
            barColor = (0, 1, 0, 1))
        self.statusStamina.reparentTo(self.frameCharStatus)
        self.statusHealth = OnscreenImage(
            image = "game/textures/gui/hud/playerHealth/playerHealth100.png",
            scale = (0.075, 1, 0.075),
            pos = (0.075, 0, -0.075))
        self.statusHealth.setTransparency(True)
        self.statusHealth.reparentTo(self.frameCharStatus)

        self.frameCollectables = DirectFrame(
            frameSize = (-0.25, 0, 0, 0.25),
            pos = (-0.05, 0, 0.05),
            frameColor = (0, 0, 0, 0))
        self.frameCollectables.reparentTo(base.a2dBottomRight)

        self.statusCollectable = OnscreenImage(
            image = "game/textures/gui/hud/collectables/collectable.png",
            scale = (0.125, 1, 0.125),
            pos = (-0.125, 0, 0.125)
            )
        self.statusCollectable.setTransparency(True)
        self.statusCollectable.reparentTo(self.frameCollectables)

        self.statusCollectableText = DirectLabel(
            text = "0",
            scale = 0.1,
            pos = (-0.13, 0, .1 ),
            frameColor = (0,0,0,0),
            text_fg = (1,1,1,1),
            text_align = TextNode.ACenter)
        self.statusCollectableText.reparentTo(self.frameCollectables)

        #TODO: This is just for testing the hud, need to be done better
        self.collectableCounter = 0

        self.accept("staminaChanged", self.setStaminaStatus)
        self.accept("healthChanged", self.setHealthStatus)
        self.accept("collectableChanged", self.setCollectableStatus)

    def show(self):
        self.frameCharStatus.show()
        self.frameCharSpecialMoves.show()

    def hide(self):
        self.frameCharStatus.hide()
        self.frameCharSpecialMoves.hide()

    def cleanup(self):
        self.hide()
        self.ignore("staminaChanged")
        self.ignore("healthChanged")
        self.frameCharStatus.destroy()
        self.statusStamina.destroy()
        self.statusHealth.destroy()

    def setStaminaStatus(self, value):
        self.statusStamina["value"] = value

    def setHealthStatus(self, value):
        """this function will set the health image in the top righthand corner
        according to the given value, where value is a integer between 0 and 100
        """
        path = "game/textures/gui/hud/playerHealth/"
        if value > 80:
            self.statusHealth.setImage(path + "playerHealth100.png")
        elif value > 60:
            self.statusHealth.setImage(path + "playerHealth80.png")
        elif value > 40:
            self.statusHealth.setImage(path + "playerHealth60.png")
        elif value > 20:
            self.statusHealth.setImage(path + "playerHealth40.png")
        else:
            self.statusHealth.setImage(path + "playerHealth20.png")
        self.statusHealth.setTransparency(True)

    def setCollectableStatus(self):
        self.collectableCounter += 1
        self.statusCollectableText["text"] = str(self.collectableCounter)

