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
import math

# Panda Engine Imports
from panda3d.core import NodePath, Point3, BitMask32
from direct.actor.Actor import Actor

# MeoTech Imports
from engine.config import MODEL_DIR
from playerPhysics import PlayerPhysics
from playerFSM import PlayerFSM

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

        # [opt]
        # def checkTag() for tagName in tagNameList[]
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
        self.jumpHeight = float(_obj.getTag("jumpHeight"))
        self.isDynamic = _obj.getTag("isDynamic")
        self.script = _obj.getTag("script")

        self.animationNames = {
            "walk": MODEL_DIR + "Avatar1-Run",
            "run": MODEL_DIR + "Avatar1-Sprint",
            "back": MODEL_DIR + "Avatar1-Run",
            "jump": MODEL_DIR + "Avatar1-Jump",
            "climb": MODEL_DIR + "Avatar1-Climb",
            "idle": MODEL_DIR + "Avatar1-Idle"}
        self.playingAnim = "Idle"

        self.doEdgeGrab = False
        self.checkClimbable = False

        # EventTypes
        self.events = ["doEdgeGrab"]

        # States
        self.position = _obj.getPos(_levelEgg)
        self.lastGroundPos = self.position
        self.groundPosTestTick = 0
        self.heading = _obj.getH(_levelEgg)

        # Player Collision Body
        self.bulletBody = None
        self.ghostBody = None
        self.useBasicMovement = False

        # Run checkers
        self.setControlType()
        self.actor = self.setActor()
        # TODO: Load scripts for this object...

        # Set that we have a player active
        self.engine.hasPlayer = True
        # Since we have a player active setup a bag
        self.bag = []
        # Basic Player Stats
        self.health = 100
        self.stamina = 100

        # Check GrabMode
        self.inGrabMode = False

        self.fsm = PlayerFSM(self)

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

    def setActor(self):
        """Attach the given model to the player"""
        if self.model != "":
            # Setup the visual actor
            # Animated stuff should be added soon
            print MODEL_DIR + self.model
            #actor = loader.loadModel(MODEL_DIR + self.model)
            actor = Actor(
                MODEL_DIR + self.model,
                self.animationNames)
            actor.setH(180)
            actor.setScale(0.5)
            actor.reparentTo(self.bulletBody.movementParent)
            #print "ACTOR SIZE =", actor.getBounds().getRadius()
            #actor.setPos(self.bulletBody.movementParent.getPos())

            self.ghostBody = PlayerPhysics.buildCharacterGhost(
                self.engine, self.height, self.radius, self.bulletBody, actor, self.heading)

            return actor


    def setBasicMovement(self, dt):
        """Make use of the basic movement controls"""
        PlayerPhysics.useBasicPlayerMovement(self.engine, dt)

    def startContactTester(self, dt):
        """Start the onCollision() in PlayerPhysics"""
        PlayerPhysics.onCollision(self.engine, self.ghostBody, self.bulletBody, dt)

    def setLoop(self, animName, loop, frames=[], framerate=1.0):
        """play the given animation.
        The animation has to be a valid animation of this
        characters actor instance"""
        if animName != "none":
            if animName == "specialMove":
                self.actor.play(self.requestedMove)
            elif loop == "False":
                self.actor.setPlayRate(framerate, animName)
                self.actor.play(animName)
            else:
                self.actor.setPlayRate(framerate, animName)
                if frames != []:
                    self.actor.loop(animName, fromFrame = frames[0], toFrame = frames[1])
                else:
                    self.actor.loop(animName)
        else:
            self.actor.stop()

    def resetPosition(self):
        self.bulletBody.setPos(self.lastGroundPos)

    def die(self):
        base.messenger.send("healthChanged", [0])

    @classmethod
    def requestState(cls, _player, requestAnim, extraArgs=[]):
        """Request a specific Animation state of the Character"""
        if _player.playingAnim == requestAnim:
            # the animation is already running
            return

        print requestAnim
        if _player.fsm.state == None:
            log.error("FSM still switch to another State...")
            return

        print requestAnim
        if extraArgs != []:
            _player.fsm.request(requestAnim, extraArgs)
        else:
            _player.fsm.request(requestAnim)
        _player.playingAnim = requestAnim

    ### EVENTS ###
    @classmethod
    def doPickup(cls, _engine, _player, _node):
        """Handle a Basic Pickup
        @param: _player = ref to the GameObjects['player'] instance
        @param: _node = the node/item that the player collided with
        """
        print "####> PLAYER doPickup() \n"

        itemName = _engine.GameObjects["object"][_node.name].name
        #print itemName
        #_node.bulletBody.removeNode()
        render.find('**/'+_node.name).removeNode()
        _engine.bulletWorld.removeGhost(_node.bulletBody.node())
        print "ItemId: ", _node.id
        print "ItemName: ", itemName

        #TODO: This is just for testing the hud, need to be done better
        if "collectible" in itemName:
            messenger.send("collectableChanged")

        _player.bag.append(itemName)
        print "Player Bag: ", _player.bag

    #def calculatePlayerHeading(_engine, _player):


    #># DT_EDGEGRAB ##
    @classmethod
    def doEdgeGrab(cls, _sweepResult, _player, _engine): #_engine, _player, _node):
        """Handle a EdgeGrab"""

        if _player.doEdgeGrab: return
        _player.doEdgeGrab = True

        print "####> PLAYER doEdgeGrab() \n"

        #mpoint = _node.getManifoldPoint()

        #playerGroundPos = mpoint.getPositionWorldOnA()
        #playerGroundPosToWallDistance = mpoint.getDistance()

        # Do sweettest
        result = _sweepResult #PlayerPhysics.doSweepTest(_engine, _player, _node)

        tempX = result[0][0]
        tempY = result[0][1]
        tempZ = result[0][2]

        newTempNodePos = (tempX, tempY, tempZ)

        tempNodeM = loader.loadModel(MODEL_DIR + "hitPos")
        tempNodeM.setScale(0.3)
        tempNode = render.attachNewNode("HitPos")
        tempNode.setPos(newTempNodePos)
        tempNodeM.reparentTo(tempNode)

        #print "tempNodePos: ", tempNode.getPos()

        #rayHit = PlayerPhysics.doRayTest(_engine, _player.bulletBody)
        messenger.send("inGrabMode")

        _player.bulletBody.movementState = "flying"
        _player.bulletBody.setPos(tempNode.getX(), tempNode.getY(), tempZ-_player.height)
        print result[0]

        # Get the heading of the player.
        # Get the hitPos of the wall.
        # check for the highest Yaxis number and then set the player to that axis in the lock mode.(grabState)

        # Adjust player Heading
        # (ie  player.lookAt(player.get_pos() - entry.getSurfaceNormal(player.get_parent()))
        #if rayHit == None:
        #    pass
        #else:
            #_player.bulletBody.movementParent.lookAt(_player.bulletBody.getPos() - rayHit)
        #    pass




        #_player.bulletBody.movementParent.lookAt(_player.bulletBody.getPos() + rayHit)



        #print "This is player pos: ", _player.bulletBody.getPos()

        # Take the world position of the player and use that for the node to attach to..
        # just adjust the height value to that of the sweeptest Z
        # Should add a extra node for the camera when the player is in an active edge grab so that the turn of the mouse doesnt
        # affect the player axis in turning


        #
    @classmethod
    def checkClimbable(cls, _engine, _node, _nodeName, _player):

        # Add something to prevent Spam on the messenger
        # FInd the range. do a sweeptest
        # If in range then do the grab

        #if _player.checkClimbable: return
        #_player.checkClimbable = True

        #Check if player is in Air ## Could move this to the player physics so that
        # the check happens there and that the eventHandler isnt flooded with spam shit
        isPlayerOnGround = _player.bulletBody.isOnGround()
        playerState = _player.bulletBody.movementState
        if not playerState == "flying":
            if not isPlayerOnGround:
                print "Is Player on Ground?: ", _player.bulletBody.isOnGround()

                # Do sweep test
                # return: hitPos, hitNodem hitNormal, hitFraction
                result = PlayerPhysics.doSweepTest(_engine, _player, _node.getNode0())

                # find the range from the player to the sweepHitPos
                playerPos = _player.bulletBody.getPos()
                x1 = playerPos[0]
                x2 = result[0][0]
                y1 = playerPos[1]
                y2 = result[0][1]
                dist = math.hypot(x2 - x1, y2 - y1)
                print "Distance: ", dist

                tempNodeM = loader.loadModel(MODEL_DIR + "hitPos")
                tempNodeM.setScale(0.3)
                tempNode = render.attachNewNode("HitPos")
                tempNode.setPos(result[0])
                tempNodeM.reparentTo(tempNode)

                if dist < 0.2:

                    # Do the edgeGrab (temp)
                    Player.doEdgeGrab(result, _player, _engine)
                    # Set the player movement keys to grabMovement

                    # Maybe replace this with an Event rather. than having it run here.
                    _engine.inputHandler.grabMovement()
                    # Set temp flying. (since im unsure)
                    _player.bulletBody.startFly()
                else:
                    print "Player not in range!!!!"




