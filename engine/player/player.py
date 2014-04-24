#!/usr/bin/python

#----------------------------------------------------------------------#
# The MIT License (MIT)
# See the license.txt for license information
#----------------------------------------------------------------------#


"""@ package Player

This should build a playable player character
"""

# System Imports
import logging as log

# Panda Engine Imports
from panda3d.core import NodePath, Point3

# MeoTech Imports
from engine.config import MODEL_DIR
from playerPhysics import PlayerPhysics

#----------------------------------------------------------------------#

# BasePlayer
class Player():
    """
    Player:
    This builds a player character.
    """
    def __init__(self, _engine, _type, _obj, _levelEgg):
        """Player Contructor"""
        print "start buidling: ", _obj, " Type: ", _type

        # Engine
        self.engine = _engine
        self.factory = self.engine.factory

        # Object
        self.object = _obj

        # Get the tags from the object
        self.name = _obj.getTag("player")
        self.id = int(_obj.getTag("id"))
        self.control = _obj.getTag("controlType")
        self.model = _obj.getTag("model")
        self.height = float(_obj.getTag("height"))
        self.radius = float(_obj.getTag("radius"))
        self.runSpeed = float(_obj.getTag("runSpeed"))
        self.walkSpeed = float(_obj.getTag("walkSpeed"))
        self.turnSpeed = float(_obj.getTag("turnSpeed"))
        #self.jumpHeight = float(_obj.getTag("jumpHeight"))
        self.isDynamic = _obj.getTag("isDynamic")
        self.script = _obj.getTag("script")

        self.doEdgeGrab = False

        # EventTypes
        self.events = ["doEdgeGrab"]

        # States
        self.position = _obj.getPos(_levelEgg)
        self.heading = _obj.getH(_levelEgg)

        # Player Collision Body
        self.bulletBody = None
        self.ghostBody = None
        self.useBasicMovement = False

        # Run checkers
        self.setControlType()
        self.playerModel = self.setModel()
        # TODO: Load scripts for this object...

        # Set that we have a player active
        self.engine.hasPlayer = True
        # Since we have a player active setup a bag
        self.bag = []

        # Log
        log.debug("Player Builder build: %s" % (self.name))

    #? Needs a re-write
    def setControlType(self):

        # Check Fps Style
        if self.control == "controlType0":
            """Add a Fps Type cam and controller"""
            # Add character controler from bullet
            # Add the fps style camera
            self.bulletBody = PlayerPhysics.buildCharacterController(
                self.engine, self.height, self.radius, self.position, self.heading)



            self.useBasicMovement = True
            # camera go here..

        # Check 3rd Person Style
        if self.control == "controlType1":
            """Add a 3rd Person view cam and controller"""
            # Add Character controller from bullet
            # Add the 3rd Person view Camera
            pass

        # Check rpg style camera
        if self.control == "controlType2":
            """Add a rpg top down style camera"""
            # Add camera
            # add the basic controller same as fps
            # replace this style with more options to support
            # point and click style movement aswell.
            pass

        # Check side scroller type camera
        if self.control == "controlType3":
            """Add a side scroller style camera"""
            # Add a side scroller type camera
            pass

    def setModel(self):
        """Attach the given model to the player"""
        if self.model != "":
            # Setup the visual model
            # Animated stuff should be added soon
            print MODEL_DIR
            print self.model
            model = loader.loadModel(MODEL_DIR + self.model)
            model.reparentTo(self.bulletBody.movementParent)
            model.setPos(self.bulletBody.movementParent.getPos())

            #self.ghostBody = PlayerPhysics.buildCharacterGhost(
                #self.engine, self.height, self.radius, self.bulletBody, model, self.heading)

            return model


    def setBasicMovement(self, dt):
        """Make use of the basic movement controls"""
        PlayerPhysics.useBasicPlayerMovement(self.engine, dt)

    def startContactTester(self, dt):
        """Start the onCollision() in PlayerPhysics"""
        PlayerPhysics.onCollision(self.engine, self.bulletBody, dt)


    ### EVENTS ###
    @classmethod
    def doPickup(cls, _engine, _player, _node):
        """Handle a Basic Pickup
        @param: _player = ref to the GameObjects['player'] instance
        @param: _node = the node/item that the player collided with
        """
        #print _node
        #print _engine.GameObjects["object"][_node.name].name

        itemName = _engine.GameObjects["object"][_node.name].name
        #print itemName
        #_node.bulletBody.removeNode()
        render.find('**/'+_node.name).removeNode()
        _engine.bulletWorld.removeGhost(_node.bulletBody.node())
        print "ItemId: ", _node.id
        print itemName

        _player.bag.append(itemName)
        print _player.bag

        # Remove the item From the world
        #
        #del _engine.GameObjects["object"][_node.name]
        #render.removeNode(_engine.BulletObjects["object"][_node.name])

    #># DT_EDGEGRAB ##
    @classmethod
    def doEdgeGrab(cls, _engine, _player, _node):
        """Handle a EdgeGrab"""

        if _player.doEdgeGrab: return
        _player.doEdgeGrab = True

        mpoint = _node.getManifoldPoint()

        playerGroundPos = mpoint.getPositionWorldOnA()
        playerGroundPosToWallDistance = mpoint.getDistance()
        print playerGroundPosToWallDistance

        # Do sweettest
        dt = globalClock.getDt()
        result = PlayerPhysics.doSweepTest(_engine, _player, _node, dt)

        tempX = result[0][0]
        tempY = result[0][1]
        tempZ = result[0][2]

        #tempX = playerGroundPos.getX() + playerGroundPosToWallDistance
        #tempY = playerGroundPos.getY() + playerGroundPosToWallDistance
        #tempZ = result[0][2]

        newTempNodePos = (tempX, tempY, tempZ)

        tempNodeM = loader.loadModel(MODEL_DIR + "hitPos")
        tempNodeM.setScale(0.1)
        tempNode = render.attachNewNode("HitPos")
        tempNode.setPos(newTempNodePos)
        tempNodeM.reparentTo(tempNode)

        print "tempNodePos: ", tempNode.getPos()
        print "tempNodeModel: ", tempNodeM.getPos()

        _player.bulletBody.movementState = "flying"
        #curX = _player.bulletBody.movementParent.getX()
        #_player.bulletBody.setY(curX - 10)
        #curY = _player.bulletBody.movementParent.getY()
        #_player.bulletBody.setY(curY - 10)
        #_player.bulletBody.movementParent.wrtReparentTo(tempNode)
        #_player.bulletBody.movementParent.reparentTo(tempNode)
        #_player.bulletBody.movementParent.setPos(tempNode.getPos())
        #_player.bulletBody.movementParent.setPos(0,0,0)
        print "#####################################", tempNode.getPos()
        _player.bulletBody.setPos(tempNode.getX(), tempNode.getY(), 7)
        print "#######################", playerGroundPosToWallDistance
        #_player.bulletBody.movementParent.setY(_player.bulletBody.getY() - 5)
        #print render.ls()
        #_player.bulletBody.movementParent.setX(playerGroundPos.getX() - playerGroundPosToWallDistance)
        #_player.bulletBody.movementParent.setY(playerGroundPos.getY() - playerGroundPosToWallDistance)
        #_player.bulletBody.movementParent.setPos(tempNode.getPos())
        #_player.bulletBody.movementParent.setX(0.0)
        #_player.bulletBody.movementParent.setY(-3)
        #_player.bulletBody.movementParent.setZ(tempNode.getZ())
        #_player.bulletBody.movementParent.setPos(_player.bulletBody.movementParent, 10)


        #print "PlayerNew Pos: ", _player.bulletBody.movementParent.getPos()

        # Take the world position of the player and use that for the node to attach to..
        # just adjust the height value to that of the sweeptest Z


        #
