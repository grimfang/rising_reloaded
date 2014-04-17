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


#----------------------------------------------------------------------#

# Game
class Game():
    """The Game handles the actual game and custom scripts.
    """
    def __init__(self, _main):
        
        print "Game - init >>>"
        
        # Meotech
        self.main = _main
        
        # Add GameLoop Task
        taskMgr.add(self.gameLoop, "Game_loop")
        
        
    def gameLoop(self, task):
        
        dt = globalClock.getDt()
        
        return task.cont
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
