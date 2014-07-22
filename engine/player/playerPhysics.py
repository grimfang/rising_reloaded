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
    #@ Fix the player capsule size so that it fits around the player model
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

    #@ Fix the size and position of the player ghost
    @classmethod
    def buildCharacterGhost(cls, _engine, _height, _radius, _bulletBody, _playerModel, _head):
        """Build a basic BulletGhost body for the player to be used for tracking eventObjects"""

        shape = BulletSphereShape(_radius*4)
        ghost = BulletGhostNode("player_ghost")
        ghost.addShape(shape)
        ghostNP = _engine.BulletObjects["player"].attachNewNode(ghost)
        newz = _playerModel.getPos()
        newz.z = newz.z + 2.5
        ghostNP.setPos(newz)
        ghostNP.setCollideMask(BitMask32.allOff())

        _engine.bulletWorld.attachGhost(ghost)
        ghostNP.reparentTo(_playerModel)

        return ghostNP



    @classmethod
    def doPlayerJump(cls, player, jumpHeight):
        """Allow the player to perform a jump"""
        player.startJump(jumpHeight)

    @classmethod
    def doPlayerCrouch(cls, player, startCrouching):
        """Allow the player to perform crouch"""
        if startCrouching:
            player.startCrouch()
        else:
            player.stopCrouch()

    #@ useBasicPlayerMovement: needs cleaning, maybe this causes the movement bug
    #@ when you enter the grabMode
    @classmethod
    def useBasicPlayerMovement(cls, _engine, dt):
        """This sets up a basic movement for the playercontroller"""

        # get the player
        player = _engine.GameObjects["player"]
        speed = Vec3(0, 0, 0)
        omega = 0.0
        requestAnim = "Idle"
        if not player.bulletBody.isOnGround() and player.bulletBody.movementState != "flying":
            requestAnim = "Fall"
        elif player.groundPosTestTick >= 10:
            player.lastGroundPos = player.bulletBody.getPos()
            player.groundPosTestTick = 0
        else:
            player.groundPosTestTick += 1

        if inputState.isSet('forward'): speed.setY(player.runSpeed); requestAnim="Run"
        if inputState.isSet('reverse'): speed.setY(-player.runSpeed); requestAnim="Walk"
        if inputState.isSet('left'): speed.setX(-player.runSpeed); requestAnim="Walk"
        if inputState.isSet('right'): speed.setX(player.runSpeed); requestAnim="Walk"
        if inputState.isSet('turnLeft'): omega =  player.turnSpeed; requestAnim="Walk"
        if inputState.isSet('turnRight'): omega = -player.turnSpeed; requestAnim="Walk"
        if inputState.isSet('space'): PlayerPhysics.doPlayerJump(player.bulletBody, player.jumpHeight); requestAnim="Jump"
        if inputState.isSet('ctrl'): PlayerPhysics.doPlayerCrouch(player)

        ## In grabState
        if player.inGrabMode:
            if inputState.isSet('climb'): player.exitGrabMode()
            elif inputState.isSet('fall'): player.exitGrabMode(False)

        if not player.bulletBody.isOnGround() and player.bulletBody.movementState != "flying":
            # as we fall, set the fall animation
            if not player.actor.getAnimControl("jump").isPlaying() \
                or (player.actor.getAnimControl("jump").isPlaying()
                and player.playingAnim == "Fall"):
                requestAnim = "Fall"
            else:
                requestAnim = "Jump"

        if omega == 0:
            omega = _engine.inputHandler.getMouse(dt)
        player.bulletBody.setAngularMovement(omega)
        player.bulletBody.setLinearMovement(speed, True)
        player.bulletBody.update()
        player.requestState(player, requestAnim)

        if player.inGrabMode:
            rayHit = PlayerPhysics.doRayTest(_engine, player.bulletBody)
            if rayHit != None:
                speed.setY(0)
                player.bulletBody.movementParent.lookAt(player.bulletBody.getPos() - rayHit)
                return



    @classmethod
    def onGhostCollision(cls, _engine, _pBulletGhost, dt):
        """Checks only player ghost contacts"""

        # OverLap test for ghosts
        ghost = _pBulletGhost.node()
        ghostContactTest = _engine.bulletWorld.contactTest(_pBulletGhost.node())
        for ghostContact in ghostContactTest.getContacts():
            contactNode = ghostContact.getNode1()
            contactNodeName = contactNode.getName()
            #contactNodeStr = str(ghostContact.getNode1())
            #contactNodeList = contactNodeStr.split()

            avoidList = ["Ground_plane", "Capsule", "ItemSphere"]
            if contactNodeName in avoidList:
                if contactNodeName == "Ground_plane":
                    player = _engine.GameObjects["player"]
                    player.die()
                    player.resetPosition()
                pass
                # While player on ground dont send msg for grab
                # only when the player left the ground = jump state, only then check
                # for wall/ledges

            else:
                #print contactNode
                """Tag gets set inside blender along with the isCollisionMesh tag, the tag for the climbeable should only be added to mesh that
                are collideable, here we check for the tag, if climbeable, then check for the range if in range (which req a jump to the ledge) we attach the
                player to the ledge. (lock the movement into the axis of the mesh.) left/right"""
                # For that idea to return the contact object/wall mask
                # Get the object/level maybe this is only for the wall masks atm
                wallMask = BitMask32(0x8) #_engine.GameObjects["level"][contactNodeName].wallMask
                messenger.send("onGhostCollision", [ghostContact, contactNodeName, wallMask])


    @classmethod
    def onCollision(cls, _engine, _pBulletGhost, _pBulletBody, dt):
        """On a collision get the node and do something with it."""

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

                    elif ghostNodeList[1] in _engine.GameObjects["sensor"]:
                        #print sensorPathList
                        bulletType = sensorPathList[2]
                        contactObjectName = sensorPathList[3]
                        messenger.send("onSensorCollision", [bulletType, contactObjectName])

                    else:
                        print contact.getNode1(), "Not Setup"
                        break


            #># DT_EDGEGRAB ##
            elif contact.getNode1():

                #print "On WallCollision: \n"
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
    #@ As mentioned: Add a visual object for debugging the sweeptest movements inside the world
    @classmethod
    def doSweepTest(cls, _engine, _player, _wallMask, _extras):
        print "####> doSweepTest()\n"

        #mpoint = _node.getManifoldPoint()
        playerPos = _player.bulletBody.getPos()

        tsFrom = TransformState.makePos(Point3(playerPos + (0, 0.2, _player.height + 5.0)))
        tsTo = TransformState.makePos(Point3(playerPos + (0, 0.2, 0)))
        #print "THIS IS THE PLAYER Z:", playerPos.getZ()

        rad = 1.5
        height = 4.0
        mask = BitMask32(0x8) #_wallMask

        #shape = BulletCylinderShape(rad, height, ZUp)
        penetration = 0.0
        shape = BulletSphereShape(rad)

        result = _engine.bulletWorld.sweepTestClosest(shape, tsFrom, tsTo, mask, penetration)

        #print "Sweep Node: ", result.getNode()
        #print "Sweep HitPos: ", result.getHitPos()
        #print "Sweep Normal: ", result.getHitNormal()
        #print "Sweep Fraction: ", result.getHitFraction()
        hitPos = result.getHitPos()
        hitNode = result.getNode()
        hitNormal = result.getHitNormal()
        hitFraction = result.getHitFraction()

        # Create a node to attach to
        # if flying then be able to right click to attach/grab
        avoidList = ["player_ghost", "Capsule"]
        #print "THIS IS THE FKING HIT NODE!!! : ", hitNode.getName()
        if hitNode.getName() not in avoidList:
            return hitPos, hitNode, hitNormal, hitFraction
        else:
            return None

    #@ Fix player heading Ray and Ray height sometimes it misses
    @classmethod
    def doRayTest(cls, _engine, _player):

        #oldTo = _node
        #oldTo.setZ(_player.getZ())

        pFrom = Point3(_player.getPos(render))
        pTo = pFrom + Vec3(0, 1, 0) * 10

        result = _engine.bulletWorld.rayTestAll(pFrom, pTo)

        for hit in result.getHits():
            hitNode = hit.getNode()
            hitNormal = hit.getHitNormal()

            if hitNode.getName() != "Ground_plane" and hitNode != None:
                #print "THIS IS THE RAY NODE: ", hitNode.getName()
                return hitNormal
            else:
                pass







