#!/usr/bin/python

#----------------------------------------------------------------------#
# The MIT License (MIT)
# See the license.txt for license information
#----------------------------------------------------------------------#


"""@ package BasePhysics

All Physics setups and builders
"""

# System Imports
import logging as log

# Panda Engine Imports
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import ZUp
from panda3d.core import Vec3, BitMask32
from direct.showbase.InputStateGlobal import inputState

# MeoTech Imports

#----------------------------------------------------------------------#

class PlayerPhysics():
    """Handle the player related physics"""

    @classmethod
    def buildCharacterController(cls, _engine, _height, _radius, _pos, _head):
        """Build a basic BulletCharacter Controller"""
        shape = BulletCapsuleShape(_radius, _height-2 * _radius, ZUp)
        
        charNode = BulletCharacterControllerNode(shape, _radius, "Player")
        np = _engine.BulletObjects["player"].attachNewNode(charNode)
        np.setPos(_pos)
        np.setH(_head)
        np.setCollideMask(BitMask32.allOn())
        
        _engine.bulletWorld.attachCharacter(np.node())
        return np
    
    @classmethod
    def doPlayerJump(cls, player):
        """Allow the player to perform a jump"""
        
        # set jump height, speed
        player.setMaxJumpHeight(5.0)
        player.setJumpSpeed(8.0)
        player.doJump()
        
    @classmethod
    def doPlayerCrouch(cls, player):
        """Allow the player to perform crouch"""
        self.crouching = not self.crouching
        
        sz = self.crouching and 0.6 or 1.0
        #player.bulletBody.node().getShape().setLocalScale(Vec3(1, 1, sz))
        
        # Get the player nodepath
        player.bulletBody.setScale(Vec3(1, 1, sz))# * 0.3048)
        #player.setPos(0, 0, -1 * sz)
    
    @classmethod
    def useBasicPlayerMovement(cls, _engine, dt):
        """This sets up a basic movement for the playercontroller"""
        
        # get the player
        player = _engine.GameObjects["player"]
        speed = Vec3(0, 0, 0)
        omega = 0.0
        
        if inputState.isSet('forward'): speed.setY(player.runSpeed)
        if inputState.isSet('reverse'): speed.setY(-player.runSpeed)
        if inputState.isSet('left'): speed.setX(-player.runSpeed)
        if inputState.isSet('right'): speed.setX(player.runSpeed)
        if inputState.isSet('turnLeft'):  omega =  player.turnSpeed
        if inputState.isSet('turnRight'): omega = -player.turnSpeed
        if inputState.isSet('space'): PlayerPhysics.doPlayerJump(player.bulletBody.node())
        if inputState.isSet('ctrl'): PlayerPhysics.doPlayerCrouch(player)
        
        #player.bulletBody.node().setAngularMovement(omega)
        player.bulletBody.node().setLinearMovement(speed, True)
        
 