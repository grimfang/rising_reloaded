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
from direct.controls.InputState import InputStateTokenGroup
from panda3d.core import WindowProperties
from direct.showbase.DirectObject import DirectObject

# MeoTech imports


#----------------------------------------------------------------------#

class InputHandler(DirectObject):
    """InputHandler.
    Keyboard stuff
    """
    def __init__(self, _engine):
        """InputHandler INIT"""

        # Game
        self.engine = _engine


        # Set Movement Keys for state = start
        self.tokenGroup = InputStateTokenGroup()
        self.generalMovement()

        # screen size for mouse
        self.winXhalf = base.win.getXSize()/2
        self.winYhalf = base.win.getYSize()/2

        self.mouseSpeedX = 7
        self.mouseSpeedY = 0.1
        self.mouseX = 0
        self.mouseY = 0

        # Set the grabMovement state check
        self.isGrabMovement = False

    def start(self):
        # For now hide the mouseCursor
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)

        # App exit temp
        base.accept("escape", self.engine.stop)
        self.setMouseButtons()

    def stop(self):
        # For now show the mouseCursor
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        self.ignoreMouseButtons()

        # App exit temp
        base.ignore("escape")


    # Player Temp movement key states?
    def generalMovement(self):
        # Keyboard
        self.tokenGroup.release()
        self.tokenGroup.addToken(inputState.watchWithModifiers('forward', 'w', inputSource=inputState.WASD))
        self.tokenGroup.addToken(inputState.watchWithModifiers('left', 'a', inputSource=inputState.WASD))
        self.tokenGroup.addToken(inputState.watchWithModifiers('reverse', 's', inputSource=inputState.WASD))
        self.tokenGroup.addToken(inputState.watchWithModifiers('right', 'd', inputSource=inputState.WASD))
        self.tokenGroup.addToken(inputState.watchWithModifiers('turnLeft', 'q', inputSource=inputState.QE))
        self.tokenGroup.addToken(inputState.watchWithModifiers('turnRight', 'e', inputSource=inputState.QE))
        self.tokenGroup.addToken(inputState.watchWithModifiers('space', 'space', inputSource=inputState.Keyboard))
        self.tokenGroup.addToken(inputState.watch('ctrl', 'lcontrol_down', 'lcontrol-up', inputSource=inputState.Keyboard))
        self.isGrabMovement = False

    def grabMovement(self):
        # Keyboard
        self.tokenGroup.release()
        # This is used to climbUp
        self.tokenGroup.addToken(inputState.watchWithModifiers('climb', 'q', inputSource=inputState.WASD))
        self.tokenGroup.addToken(inputState.watchWithModifiers('left', 'a', inputSource=inputState.WASD))
        self.tokenGroup.addToken(inputState.watchWithModifiers('right', 'd', inputSource=inputState.WASD))
        self.tokenGroup.addToken(inputState.watchWithModifiers('fall', 's', inputSource=inputState.WASD))
        for item in ['forward', 'left', 'reverse', 'right']:
            inputState.set(item, False, inputSource=inputState.WASD)
        self.isGrabMovement = True


    def setMouseButtons(self):
        self.accept('mouse1', self.leftMouseBtn)
        self.accept('mouse3', self.rightMouseBtn)

    def ignoreMouseButtons(self):
        self.ignore('mouse1')
        self.ignore('mouse3')

    def leftMouseBtn(self):
        messenger.send("left_mouse")

    def rightMouseBtn(self):
        messenger.send("right_mouse")

    def update(self, dt):
        md = base.win.getPointer(0)
        self.mouseX = md.getX()
        self.mouseY = md.getY()


    def getMouse(self, dt):

        # Handle mouse
        omega = 0.0

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




























