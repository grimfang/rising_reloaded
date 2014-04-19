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

        self.accept("onCollision", self.onCollision)

    def onCollision(self, _bulletType, _nodeName):

        playerInstance = self.engine.GameObjects['player']

        if _bulletType == "Bullet_object":
            itemInstance = self.engine.GameObjects["object"][_nodeName]
            eventType = itemInstance.eventType
            call = getattr(Player, eventType)(self.engine, playerInstance, itemInstance)

        if _bulletType == "Bullet_sensor":
            sensorInstance = self.engine.GameObjects["sensor"][_nodeName]
            eventType = sensorInstance.eventType
            call = getattr(Player, eventType)(self.engine, playerInstance, sensorInstance)
        

        