#!/usr/bin/python

#----------------------------------------------------------------------#
# The MIT License (MIT)
# See the license.txt for license information
#----------------------------------------------------------------------#

"""@ package Game

Start the Game.
"""

# System Imports
import logging as log

# Panda Engine Imports

# MeoTech Imports
from input import InputHandler

#----------------------------------------------------------------------#

# Game
class Game():
    """The Game handles the actual game and custom scripts.
    """
    def __init__(self, _meotech):
        
        print "Game - init >>>"
        
        # Meotech
        self.meotech = _meotech
        
        # Load Inputs
        self.inputs = InputHandler(self)
        
        # Add GameLoop Task
        taskMgr.add(self.gameLoop, "Game_loop")

        # Check the engine if we have a player.
        if self.meotech.engine.GameObjects["player"]:
            if self.meotech.engine.GameObjects["player"].useBasicMovement:
                self.hasPlayer = True

        else:
            self.hasPlayer = False

        
        
    def gameLoop(self, task):
        
        dt = globalClock.getDt()
        # Add player movement
        # Check this if its slow change it...
        if self.hasPlayer:
            self.meotech.engine.factory.basePhysics.useBasicPlayerMovement(dt)
            self.inputs.getMouse(dt)
        # Add Player camera handler
        
        return task.cont
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
