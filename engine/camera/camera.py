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

    def __init__(self, _engine):

    	self.engine = _engine


    	# Setup the camera so that its on the player
    	player = self.engine.GameObjects["player"].bulletBody
        self.camDummy = self.engine.GameObjects["player"].bulletBody.movementParent.attachNewNode("camDummy")
        self.camDummy.setPos(player.getX(), player.getY()-6, 3)
        base.camera.reparentTo(self.camDummy)
        base.camLens.setFov(90)
        base.camLens.setNear(0.3)
        base.cam.setZ(0.8)

        taskMgr.add(self.followPlayer, "cam_follow", priority=35)

    def followPlayer(self, task):
    	player = self.engine.GameObjects["player"].bulletBody
    	#base.camera.setPos(player.getX()-4, player.getY()-4, 5)
    	base.camera.lookAt(player.movementParent)
    	return Task.cont

        

    
