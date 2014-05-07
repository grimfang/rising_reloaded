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
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import ZUp
from panda3d.core import Vec3, BitMask32, NodePath, Point3, TransformState
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
        char.setCollideMask(BitMask32(0x5))

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
    def buildCharacterGhost(cls, _engine, _height, _radius, _bulletBody, _playerModel, _head):
        """Build a basic BulletGhost body for the player to be used for tracking eventObjects"""

        shape = BulletSphereShape(_radius*4)
        ghost = BulletGhostNode("player_ghost")
        ghost.addShape(shape)
        ghostNP = _engine.BulletObjects["player"].attachNewNode(ghost)
        newz = _playerModel.getPos()
        newz.z = newz.z# + 1.25
        #ghostNP.setPos(newz)
        ghostNP.setCollideMask(BitMask32(0xa))#.allOff())

        _engine.bulletWorld.attachGhost(ghost)
        ghostNP.reparentTo(_playerModel)

        return ghostNP



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
        if inputState.isSet('turnLeft'): omega =  player.turnSpeed
        if inputState.isSet('turnRight'): omega = -player.turnSpeed
        if inputState.isSet('space'): PlayerPhysics.doPlayerJump(player.bulletBody)
        if inputState.isSet('ctrl'): PlayerPhysics.doPlayerCrouch(player)

        if omega == 0:
            omega = _engine.inputHandler.getMouse(dt)
        player.bulletBody.setAngularMovement(omega)
        player.bulletBody.setLinearMovement(speed, True)
        player.bulletBody.update()


    # could do this better..
    @classmethod
    def onCollision(cls, _engine, _pBulletGhost, _pBulletBody, dt):
        """On a collision get the node and do something with it."""

        # OverLap test for ghosts
        ghost = _pBulletGhost.node()
        ghostContactTest = _engine.bulletWorld.contactTest(_pBulletGhost.node())
        for ghostContact in ghostContactTest.getContacts():
            contactNode = ghostContact.getNode1()
            contactNodeStr = str(ghostContact.getNode1())
            contactNodeList = contactNodeStr.split()

            contactNodeName = contactNodeList[1]

            avoidList = ["Ground_plane", "Capsule", "ItemSphere"]
            if contactNodeList[1] in avoidList:
                pass
                # While player on ground dont send msg for grab
                # only when the player left the ground = jump state, only then check 
                # for wall/ledges

            else:
                print contactNode
                """Tag gets set inside blender along with the isCollisionMesh tag, the tag for the climbeable should only be added to mesh that 
                are collideable, here we check for the tag, if climbeable, then check for the range if in range (which req a jump to the ledge) we attach the 
                player to the ledge. (lock the movement into the axis of the mesh.) left/right"""
                messenger.send("onGhostCollision", [ghostContact, contactNodeName])

        #for node in ghost.getOverlappingNodes():
        #    print "ghost collide:", node

        # Contact test for solids
        result = _engine.bulletWorld.contactTest(_pBulletBody.movementParent.node().getChild(0))

        for contact in result.getContacts():

            if contact.getNode1() in _engine.bulletWorld.getGhosts():

                # This works for Items only so far.
                if contact.getNode1().getNumChildren() >= 1:
                    pandaNode = str(contact.getNode1().getChild(0))
                    pandaNodeList = pandaNode.split()

                    # Find the correct Name for the item
                    renderPath = str(render.find('**/'+pandaNodeList[1]))
                    renderPathList = renderPath.split('/')

                    bulletType = renderPathList[2]
                    contactObjectName = renderPathList[4]

                    #eventType = contactObject.eventType
                    # We should check into this and make sure it doesnt spam the messenger to much
                    messenger.send("onItemCollision", [bulletType, contactObjectName])

                elif contact.getNode1():
                    ghostNode = str(contact.getNode1())
                    ghostNodeList = ghostNode.split()

                    sensorPath = str(render.find('**/'+ghostNodeList[1]))
                    sensorPathList = sensorPath.split('/')

                    if ghostNodeList[1] == 'player_ghost':
                        pass

                    elif _engine.GameObjects["sensor"][ghostNodeList[1]]:
                        #print sensorPathList
                        bulletType = sensorPathList[2]
                        contactObjectName = sensorPathList[3]
                        messenger.send("onSensorCollision", [bulletType, contactObjectName])

                    else:
                        print contact.getNode1(), "Not Setup"
                        break


            #># DT_EDGEGRAB ##
            elif contact.getNode1():

                print "On WallCollision: \n"
                node = contact
                bulletNP = str(contact.getNode1())
                bulletNPList = bulletNP.split()

                nodeName = bulletNPList[2]

                # Get some math shit
                mpoint = contact.getManifoldPoint()

                #print "WALL COLLISION"
                #print "Distance: ", mpoint.getDistance()
                #print "WorldPos(A): ", mpoint.getPositionWorldOnA()
                #print "WorldPos(B): ", mpoint.getPositionWorldOnB()
                #print "LocalPoint(A): ", mpoint.getLocalPointA()
                #print "LocalPoint(B): ", mpoint.getLocalPointB()

                # if "_col" in nodeName: do #Maybe slow??
                #messenger.send("onWallCollision", [node, nodeName])


        #># DT_EDGEGRAB ##
    @classmethod
    def doSweepTest(cls, _engine, _player, _node):
        print "####> doSweepTest() \n"

        #mpoint = _node.getManifoldPoint()
        playerPos = _player.bulletBody.getPos()

        tsFrom = TransformState.makePos(Point3(playerPos + (0, 0, _player.height + 8.0)))
        tsTo = TransformState.makePos(Point3(playerPos + (0, 0, _player.height + 0.25)))

        rad = 2.0
        height = 5.0
        mask = BitMask32(0x8)

        shape = BulletCylinderShape(rad, height, ZUp)
        penetration = 0.0

        result = _engine.bulletWorld.sweepTestClosest(shape, tsFrom, tsTo, mask, penetration)

        print "Sweep Node: ", result.getNode()
        print "Sweep HitPos: ", result.getHitPos()
        print "Sweep Normal: ", result.getHitNormal()
        print "Sweep Fraction: ", result.getHitFraction()
        hitPos = result.getHitPos()
        hitNode = result.getNode()
        hitNormal = result.getHitNormal()
        hitFraction = result.getHitFraction()

        # Create a node to attach to
        # if flying then be able to right click to attach/grab
        return hitPos, hitNode, hitNormal, hitFraction
