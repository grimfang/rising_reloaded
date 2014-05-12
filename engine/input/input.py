#!/usr/bin/python

#----------------------------------------------------------------------#
# The MIT License (MIT)
# See the license.txt for license information
#----------------------------------------------------------------------#

"""@ package Input

Keep all inputs here.
"""

# System imports
import logging as log
import sys

# Panda imports
from direct.showbase.InputStateGlobal import inputState
from panda3d.core import WindowProperties

# MeoTech imports


#----------------------------------------------------------------------#

class InputHandler():
    """InputHandler.
    Keyboard stuff
    """
    def __init__(self, _engine):
        """InputHandler INIT"""

        # Game
        self.engine = _engine

        # For now hide the mouseCursor
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)

        # Set Movement Keys for state = start
        self.generalMovement()

        # App exit temp
        base.accept("escape", sys.exit)

        # screen size for mouse
        self.winXhalf = base.win.getXSize()/2
        self.winYhalf = base.win.getYSize()/2

        self.mouseSpeedX = 7
        self.mouseSpeedY = 0.1
        self.mouseX = 0
        self.mouseY = 0

    # Player Temp movement key states?
    def generalMovement(self):
        # Keyboard
        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('left', 'a')
        inputState.watchWithModifiers('reverse', 's')
        inputState.watchWithModifiers('right', 'd')
        inputState.watchWithModifiers('turnLeft', 'q')
        inputState.watchWithModifiers('turnRight', 'e')
        inputState.watchWithModifiers('space', 'space')
        inputState.watchWithModifiers('ctrl', 'lcontrol_down')

    def grabMovement(self):
        # Keyboard
        inputState.watchWithModifiers('left', 'a')
        inputState.watchWithModifiers('right', 'd')
        inputState.watchWithModifiers('space', 'space')
        inputState.watchWithModifiers('ctrl', 'lcontrol_down')

    def update(self, dt):
        md = base.win.getPointer(0)
        self.mouseX = md.getX()
        self.mouseY = md.getY()


    def getMouse(self, dt):

        # Handle mouse
        omega = 0

        if base.win.movePointer(0, self.winXhalf, self.winYhalf) \
               and base.mouseWatcherNode.hasMouse():
            omega = (self.mouseX - self.winXhalf)*-self.mouseSpeedX
            self.engine.GameObjects["player"].bulletBody.setAngularMovement(omega)
        return omega




























