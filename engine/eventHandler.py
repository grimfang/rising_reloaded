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

    def onCollision(self, _eventType, _node):

        playerInstance = self.engine.GameObjects['player']
        call = getattr(Player, _eventType)(self.engine, playerInstance, _node)
        

        