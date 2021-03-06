#!/usr/bin/python

#----------------------------------------------------------------------#
# The MIT License (MIT)
# See the license.txt for license information
#----------------------------------------------------------------------#


"""@ package EventHandler

Handle Events.
"""

# System Imports
import logging as log

# Panda Engine Imports
from direct.showbase.DirectObject import DirectObject

# MeoTech Imports
from player.player import Player

#----------------------------------------------------------------------#

# EventHandler
class EventHandler(DirectObject):
    """EventHandler
    """
    def __init__(self, _engine):

        print "Engine - init >>>"

        self.engine = _engine

    def start(self):
        self.accept("onItemCollision", self.onItemCollision)
        #self.acceptOnce("onSensorCollision", self.onSensorCollision)
        #self.accept("onWallCollision", self.onWallCollision)
        self.accept("onGhostCollision", self.onGhostCollision)
        self.accept("inGrabMode", self.setGrabMode)
        self.accept("left_mouse", self.leftMouse)
        self.accept("right_mouse", self.rightMouse)

    def stop(self):
        self.ignore("onItemCollision")
        self.ignore("onGhostCollision")
        self.ignore("inGrabMode")

    #-----------------------------------------------------------------------------------#
    # COLLISIONS
    #-----------------------------------------------------------------------------------#
    def setGrabMode(self, _boolState):
        self.engine.GameObjects['player'].inGrabMode = _boolState

    def onGhostCollision(self, _node, _nodeName, _wallMask):

        playerInstance = self.engine.GameObjects['player']

        eventType = "checkClimbable"

        call = getattr(Player, eventType)(self.engine, _node, _nodeName, playerInstance, _wallMask)

    def onItemCollision(self, _bulletType, _nodeName):

        playerInstance = self.engine.GameObjects['player']

        if _bulletType == "Bullet_object":
            itemInstance = self.engine.GameObjects["object"][_nodeName]
            eventType = itemInstance.eventType
            call = getattr(Player, eventType)(self.engine, playerInstance, itemInstance)

    def onSensorCollision(self, _bulletType, _nodeName):

        playerInstance = self.engine.GameObjects["player"]

        if _bulletType == "Bullet_sensor":
            sensorInstance = self.engine.GameObjects["sensor"][_nodeName]
            eventType = sensorInstance.eventType
            call = getattr(Player, eventType)(self.engine, playerInstance, sensorInstance)


    #># DT_EDGEGRAB ##
    def onWallCollision(self, _node, _nodeName):
        """_node = contact.getNode1()"""

        playerInstance = self.engine.GameObjects["player"]

        # do sweeptest get object height
        #wallInstance
        # Do the sweep test
        eventType = playerInstance.events[0]

        call = getattr(Player, eventType)(self.engine, playerInstance, _node)

    #-----------------------------------------------------------------------------------#
    # END COLLISIONS
    #-----------------------------------------------------------------------------------#

    #-----------------------------------------------------------------------------------#
    # INPUTS
    #-----------------------------------------------------------------------------------#

    def onInputStateChange(self, _node, _nodeName):
        pass

    def leftMouse(self):
        print "PRESSED LEFT MOUSE"

    def rightMouse(self):
        print "PRESSED RIGHT MOUSE"
