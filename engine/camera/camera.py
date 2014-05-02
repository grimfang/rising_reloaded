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
# MeoTech Imports

#----------------------------------------------------------------------#

# BaseCamera
class CameraHandler():
    """Hold the different cameras"""

    def __init__(self, _engine, _mode):
    	self.engine = _engine
    	player = self.engine.GameObjects["player"].bulletBody
        self.camDummy = self.engine.GameObjects["player"].bulletBody.movementParent.attachNewNode("camDummy")
        base.camLens.setFov(90)
        base.camLens.setNear(0.3)
        base.cam.setZ(0.8)
        #TODO: Check for selected _mode (currently TPA or TPS)
        self.initTPAMode(player)

    def update(self, dt):
        self.followPlayerTPA(dt)

    def initTPSMode(self):
        """Sets the cam mode to a third person shooter mode, so the
        cam will be up and behind the player as well as always look
        in the direction the player faces"""
        self.camP = 5
        # Setup the camera so that its on the player
        base.camera.reparentTo(self.camDummy)

        taskMgr.add(self.followPlayerTPS, "cam_follow", priority=35)

    def followPlayerTPS(self, task):
    	player = self.engine.GameObjects["player"].bulletBody
    	#base.camera.setPos(player.getX()-4, player.getY()-4, 5)
        self.camDummy.setPos(player.getX(), player.getY()-6, 3)
    	base.camera.lookAt(player.movementParent)

        ih = self.engine.inputHandler
        cam = base.cam.getP() - (ih.mouseY - ih.winYhalf) * ih.mouseSpeedY
        if cam <-80:
            cam = -80
        elif cam > 90:
            cam = 90
        base.cam.setP(cam)

    	return Task.cont

    def initTPAMode(self, player):
        """Sets the cam mode to a third person adventure mode, so the
        cam will be up and behind the player and will be lazily move
        behind the player."""
        # Setup the camera so that its on the player
        self.camDummy.setPos(player.getX(), player.getY(), 3)
        self.camDummy.reparentTo(player.movementParent)
        base.camera.lookAt(self.camDummy)

        self.smiley = loader.loadModel("smiley")
        self.smiley.setScale(0.5)
        self.smiley.reparentTo(render)
        self.smiley.setPos(self.camDummy.getPos())

    def followPlayerTPA(self, dt):
    	player = self.engine.GameObjects["player"].bulletBody
        self.camDummy.setPos(player.movementParent.getPos())
        self.camDummy.setZ(self.camDummy.getZ() + 3)

        base.camera.lookAt(self.camDummy.getPos())
        ih = self.engine.inputHandler
        if base.win.movePointer(0, ih.winXhalf, ih.winYhalf) \
               and base.mouseWatcherNode.hasMouse():
            omega = (ih.mouseX - ih.winXhalf)*-ih.mouseSpeedX * dt * 0.5
            if omega != 0.0:
                print omega
                base.camera.setX(base.camera, omega)

        if base.camera.getZ() > self.camDummy.getZ() + 1:
            base.camera.setZ(self.camDummy.getZ() + 1)
        elif base.camera.getZ() < self.camDummy.getZ() - 1:
            base.camera.setZ(self.camDummy.getZ() - 1)

        camvec = self.camDummy.getPos() - base.camera.getPos()
        camdist = camvec.length()
        camvec.normalize()
        if camdist > 4:
            base.camera.setPos(base.camera.getPos() + camvec*(camdist-4))


        base.camera.lookAt(self.camDummy)
        print base.camera.getPos()

        self.smiley.setPos(self.camDummy.getPos())
        self.smiley.setHpr(base.camera.getHpr())

