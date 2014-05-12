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

        self.accept("onItemCollision", self.onItemCollision)
        #self.acceptOnce("onSensorCollision", self.onSensorCollision)
        #self.accept("onWallCollision", self.onWallCollision)
        self.accept("onGhostCollision", self.onGhostCollision)

    def onGhostCollision(self, _node, _nodeName):

        playerInstance = self.engine.GameObjects['player']
        
        eventType = "checkClimbable"

        call = getattr(Player, eventType)(self.engine, _node, _nodeName, playerInstance)

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

        print "onWallCollision()"
        call = getattr(Player, eventType)(self.engine, playerInstance, _node)
        

        