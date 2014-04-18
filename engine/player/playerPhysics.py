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
from bulletCharacterController import PandaBulletCharacterController
from panda3d.core import Vec3, BitMask32
from direct.showbase.InputStateGlobal import inputState

# MeoTech Imports

#----------------------------------------------------------------------#

class PlayerPhysics():
    """Handle the player related physics"""

    # NOTE: I wonder if these are really a good idea? doing @classmethod....
    @classmethod
    def buildCharacterController(cls, _engine, _height, _radius, _pos, _head):
        """Build a basic BulletCharacter Controller"""
        np = _engine.BulletObjects["player"].attachNewNode("BCC")
        # initialise the Bullet character controller node
        char = PandaBulletCharacterController(
            _engine.bulletWorld,
            np,
            _height,
            _height * 0.35,
            0.02,
            _radius)
        # now make the character collideable with walls and ground
        char.setCollideMask(BitMask32.allOn())

        # reparent the actor to our character nodepath, so we don't
        # need to keep track of the actualisation ourselfe
        #self.character.actor.reparentTo(self.char.movementParent)

        # set the character to the start position of the actor,
        # as it will hold the startposition of the active level
        char.setPos(_pos)
        # and set the heading to those of the actor
        char.setH(_head)

        return char



    @classmethod
    def doPlayerJump(cls, player):
        """Allow the player to perform a jump"""
        player.startJump(5.0)

    @classmethod
    def doPlayerCrouch(cls, player, startCrouching):
        """Allow the player to perform crouch"""
        if startCrouching:
            player.startCrouch()
        else:
            player.stopCrouch()

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
        #if inputState.isSet('turnLeft'):  omega =  player.turnSpeed
        #if inputState.isSet('turnRight'): omega = -player.turnSpeed
        if inputState.isSet('space'): PlayerPhysics.doPlayerJump(player.bulletBody)
        if inputState.isSet('ctrl'): PlayerPhysics.doPlayerCrouch(player)

        omega = _engine.inputHandler.getMouse(dt)
        player.bulletBody.setAngularMovement(omega)
        player.bulletBody.setLinearMovement(speed, True)
        player.bulletBody.update()



    # could do this better..
    @classmethod
    def onCollision(cls, _engine, _player, dt):

        result = _engine.bulletWorld.contactTest(_player.movementParent.node())

        for contact in result.getContacts():
            
            node0 = contact.getNode0()
            node1 = contact.getNode1()
            print node0, node1
            #eventType = nodeInstance.getEventType() 
            #we will have to setup items so that we can use the name to search for the instance
            #_player.messenger.send("onCollision", [eventType, node])