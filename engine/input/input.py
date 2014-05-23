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

        # Set the grabMovement state check
        self.isGrabMovement = False

    # Player Temp movement key states?
    def generalMovement(self):
        # Keyboard
        self.forwardToken = inputState.watch('forward', 'w', 'w-up', inputSource=inputState.WASD)#inputState.watchWithModifiers('forward', 'w')
        self.leftToken = inputState.watch('left', 'a', 'a-up', inputSource=inputState.WASD)
        self.reverseToken = inputState.watch('reverse', 's', 's-up', inputSource=inputState.WASD)
        self.rightToken = inputState.watch('right', 'd', 'd-up', inputSource=inputState.WASD)
        #self.turnLToken = inputState.watch('turnLeft', 'q', 'q-up', wasdInputs)
        #self.turnRToken = inputState.watch('turnRight', 'e', 'e-up', wasdInputs)
        self.spaceToken = inputState.watch('space', 'space', 'space-up', inputSource=inputState.WASD)
        #self.forwardToken = inputState.watch('ctrl', 'lcontrol_down', 'lcontrol-up', wasdInputs)

    def grabMovement(self):
        # Keyboard
        self.forwardToken.release()
        self.reverseToken.release()
        self.isGrabMovement = True

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

            if self.isGrabMovement:
                #print "Lock the camera on the omega"
                #print omega
                omega = 0.0
                self.engine.GameObjects["player"].bulletBody.setAngularMovement(omega)


            else:
                self.engine.GameObjects["player"].bulletBody.setAngularMovement(omega)
        return omega




























