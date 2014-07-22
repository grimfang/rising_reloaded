#!/usr/bin/python

#----------------------------------------------------------------------#
# The MIT License (MIT)
# See the license.txt for license information
#----------------------------------------------------------------------#

"""@ package BaseCamera

Different Cameras
"""

# System Imports
import logging as log

# Panda Engine Imports
from direct.task import Task
from panda3d.core import PandaNode,NodePath
# MeoTech Imports

#----------------------------------------------------------------------#

# BaseCamera
class CameraHandler():
    """Hold the different cameras"""

    def __init__(self, _engine, _mode):
        self.mode = _mode
    	self.engine = _engine
        self.camDummy = None
    	player = self.engine.GameObjects["player"].bulletBody
        if self.mode == "TPA":
            self.initTPAMode(player)
        else:
            self.initTPSMode(player)

    def update(self, dt):
        if self.mode == "TPA":
            self.followPlayerTPA(dt)
        else:
            self.followPlayerTPS(dt)

    def stop(self):
        base.camera.reparentTo(render)
        base.camera.setPos(0,0,0)

    #
    # Third person shooter mode
    #
    def initTPSMode(self, player):
        """Sets the cam mode to a third person shooter mode, so the
        cam will be up and behind the player as well as always look
        in the direction the player faces"""
        # Setup the camera so that its on the player
        self.camDummy = NodePath(PandaNode("camDummy"))
        self.camDummy.reparentTo(player.movementParent)
        self.camDummy.setPos(0, 0, 1.8)
        base.camera.reparentTo(self.camDummy)
        base.camera.setPos(0, -8, 2)

    def followPlayerTPS(self, dt):
    	player = self.engine.GameObjects["player"].bulletBody
        ih = self.engine.inputHandler
        if base.win.movePointer(0, ih.winXhalf, ih.winYhalf) \
               and base.mouseWatcherNode.hasMouse():
            cam = self.camDummy.getP() - (ih.mouseY - ih.winYhalf) * ih.mouseSpeedY
            if cam <-80:
                cam = -80
            elif cam > 90:
                cam = 90
            self.camDummy.setP(cam)
    	base.camera.lookAt(self.camDummy)

    #
    # Third person adventure mode
    #
    def initTPAMode(self, player):
        """Sets the cam mode to a third person adventure mode, so the
        cam will be up and behind the player and will be lazily move
        behind the player."""
        # create a new dummy node that the cam will look at
        self.camDummy = NodePath(PandaNode("camDummy"))
        self.camDummy.reparentTo(render)
        # Setup the camera so that its on the player
        base.camera.reparentTo(self.camDummy)
        base.camera.setPos(player.getX(), player.getY() - 6.0, player.getZ() + 4.0)

    def followPlayerTPA(self, dt):
    	player = self.engine.GameObjects["player"].bulletBody
        base.camera.lookAt(player.getPos())

        ih = self.engine.inputHandler
        if base.win.movePointer(0, ih.winXhalf, ih.winYhalf) \
               and base.mouseWatcherNode.hasMouse():
            omega = (ih.mouseX - ih.winXhalf)*-ih.mouseSpeedX * dt * 0.25
            if omega != 0.0:
                base.camera.setX(base.camera, omega)

        camvec = player.getPos() - base.camera.getPos()
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()
        minCamDist = 2.0
        maxCamDist = 8.0
        if camdist > maxCamDist:
            base.camera.setPos(base.camera.getPos() + camvec*(camdist-maxCamDist))
            camdist = maxCamDist
        if camdist < minCamDist:
            base.camera.setPos(base.camera.getPos() - camvec*(minCamDist-camdist))
            camdist = minCamDist

        if base.camera.getZ() > self.camDummy.getZ() + 2:
            base.camera.setZ(self.camDummy.getZ() + 2)
        elif base.camera.getZ() < self.camDummy.getZ() + 1:
            base.camera.setZ(self.camDummy.getZ() + 1)

        self.camDummy.setPos(player.getPos())
        self.camDummy.setZ(player.getZ() + 2.0)
        base.camera.lookAt(self.camDummy)


