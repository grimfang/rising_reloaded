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
            "walk": "avatar/Avatar1-Run",
            "run": "avatar/Avatar1-Sprint",
            "back": "avatar/Avatar1-Run",
            "jump": "avatar/Avatar1-Jump",
            "climb": "avatar/Avatar1-Climb",
            "idle": "avatar/Avatar1-Idle"}
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
        self.loadAudio()
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
        self.lastWallMask = None

        self.fsm = PlayerFSM(self)

        # Log
        log.debug("Player Builder build: %s" % (self.name))


    #@ Rename this setControlType to basic Control or something since its focused on Rising and not the meotech engine itself
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

    def setActor(self):
        """Attach the given model to the player"""
        if self.model != "":
            # Setup the visual actor
            actor = Actor(
                self.model,
                self.animationNames)
            actor.setH(180)
            actor.setScale(0.5)
            actor.reparentTo(self.bulletBody.movementParent)
            #print "ACTOR SIZE =", actor.getBounds().getRadius()
            #actor.setPos(self.bulletBody.movementParent.getPos())

            self.ghostBody = PlayerPhysics.buildCharacterGhost(
                self.engine, self.height, self.radius, self.bulletBody, actor, self.heading)

            return actor

    def loadAudio(self):
        self.engine.audioMgr.addSound("footstep", "footstep.ogg", volume=2.0)

    def setBasicMovement(self, dt):
        """Make use of the basic movement controls"""
        PlayerPhysics.useBasicPlayerMovement(self.engine, dt)

    def startContactTester(self, dt):
        """Start the onCollision() in PlayerPhysics"""
        PlayerPhysics.onCollision(self.engine, self.ghostBody, self.bulletBody, dt)

    def startGhostContactTester(self, dt):
        """This is only for the ghost contacts. instead of having both in one method"""
        PlayerPhysics.onGhostCollision(self.engine, self.ghostBody, dt)

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

        tempNodeM = loader.loadModel("hitPos2")
        #tempNodeM.setZ(5)
        tempNodeM.setScale(0.5)
        tempNode = render.attachNewNode("HitPos2")
        tempNode.setPos(newTempNodePos)
        tempNodeM.reparentTo(tempNode)

        #print "tempNodePos: ", tempNode.getPos()

        #rayHit = PlayerPhysics.doRayTest(_engine, _player.bulletBody)

        messenger.send("inGrabMode", [True])
        _player.bulletBody.movementState = "flying"
        #_player.bulletBody.clearForces()
        _player.bulletBody.setPos(tempNode.getX(), tempNode.getY(), tempZ-(_player.height+0.3))
        newResult = Player.doSweepTest(_engine, _player, Player.lastWallMask)
        #_player.bulletBody.movementParent.setTransform(tempNode.getX(), tempNode.getY(), tempZ-(_player.height+0.3))


    #@ Add a visual debug for the sweeptest
    #@ Add a fix to ignore low walls, so that the character only grabs onto high walls
    @classmethod
    def checkClimbable(cls, _engine, _node, _nodeName, _player, _wallMask):

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
                result = Player.doSweepTest(_engine, _player, _wallMask)

                if result != None:
                    # find the range from the player to the sweepHitPos
                    playerPos = _player.bulletBody.getPos()
                    x1 = playerPos[0]
                    x2 = result[0][0]
                    y1 = playerPos[1]
                    y2 = result[0][1]
                    dist = math.hypot(x2 - x1, y2 - y1)
                    print "Distance: ", dist

                    tempNodeM = loader.loadModel("hitPos")
                    tempNodeM.setScale(0.3)
                    tempNode = render.attachNewNode("HitPos")
                    tempNode.setPos(result[0])
                    tempNodeM.reparentTo(tempNode)

                    if dist < 1:

                        # Set the wallMask
                        Player.lastWallMask = _wallMask

                        # Do the edgeGrab (temp)
                        Player.doEdgeGrab(result, _player, _engine)
                        # Set the player movement keys to grabMovement

                        # Maybe replace this with an Event rather. than having it run here.
                        _engine.inputHandler.grabMovement()
                        # Set temp flying. (since im unsure)
                        _player.bulletBody.startFly()
                    else:
                        print "Player not in range!!!!"


    # If all went well.. we would like to get out of the grab mode..
    # So check for keypress w (UP/Forward)
    # if we get a keypress lets do another sweeptest to make sure we can climb up
    # if we can climb up, lets do it. remove from grabmode reset movement keys.

    def exitGrabMode(self, up=True):
        _player = self.engine.GameObjects["player"]

        if not up:
            print "FALLING DOWN"
            self.engine.inputHandler.isGrabMovement = False
            _player.bulletBody.stopFly()
            self.engine.inputHandler.generalMovement()
            print "Y BEFORE = ", _player.bulletBody.getY()
            _player.bulletBody.setY(_player.bulletBody.getY() - 10)
            print "Y AFTER = ", _player.bulletBody.getY()
            return

        result = Player.doSweepTest(self.engine, _player, Player.lastWallMask)
        print "Exit Grabmode"
        print result

        if result:
            self.engine.inputHandler.isGrabMovement = False
            _player.bulletBody.setPos(result[0])
            messenger.send("inGrabMode", [False])
            _player.bulletBody.movementState = "ground"
            _player.bulletBody.stopFly()
            self.engine.inputHandler.generalMovement()



    # Call this to-do a sweeptest
    @classmethod
    def doSweepTest(cls, _engine, _player, _wallMask, _extras=[]):
        """Use for sweepTest checks"""

        result = PlayerPhysics.doSweepTest(_engine, _player, _wallMask, _extras)

        return result



