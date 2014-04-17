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

# MeoTech Imports

#----------------------------------------------------------------------#

# BaseCamera
class CameraHandler():
    """Hold the different cameras"""

    def __init__(self, _engine):

    	self.engine = _engine


    	# Setup the camera so that its on the player
        base.camera.reparentTo(self.engine.GameObjects["player"].bulletBody.movementParent)
        base.camLens.setFov(90)
        base.camLens.setNear(0.5)

    
