#!/usr/bin/python

#----------------------------------------------------------------------#
# The MIT License (MIT)
# See the license.txt for license information
#----------------------------------------------------------------------#


"""@ package MeoTech

Start the MeoTech Engine.
"""

# System Imports
import logging as log

# Panda Engine Imports
from panda3d.bullet import BulletWorld, BulletDebugNode
from panda3d.core import Vec3

# MeoTech Imports
from factory import Factory
from config import *
from input.input import InputHandler
from camera.camera import CameraHandler

#----------------------------------------------------------------------#

# Engine
class Engine():
    """The engine class sets up the holders for game GameObjects
    and starts the parser that runs through the [name].egg
    """
    def __init__(self, _main):

        print "Engine - init >>>"

        # Main ref
        self.main = _main

        ### Bools ###
        # Gets set if we have a player character to work with.
        self.havePlayer = False

        ### Bools END ###

        ### Setup Engine Holders ###

        # Create Game ObjectType Holders these hold the instances
        self.GameObjects = {}
        self.GameObjects["player"] = None
        self.GameObjects["level"] = {}
        self.GameObjects["object"] = {}
        self.GameObjects["light"] = {}
        self.GameObjects["sensor"] = {}

        # Create Render Object Holders for sorting stuff in sceneG.
        # nodepaths
        self.RenderObjects = {}
        self.BulletObjects = {}

        # none visual
        self.BulletObjects["main"] = render.attachNewNode("Bullet_main")
        self.BulletObjects["player"] = self.BulletObjects["main"].attachNewNode("Bullet_player")
        self.BulletObjects["level"] = self.BulletObjects["main"].attachNewNode("Bullet_level")
        self.BulletObjects["object"] = self.BulletObjects["main"].attachNewNode("Bullet_object")
        self.BulletObjects["sensor"] = self.BulletObjects["main"].attachNewNode("Bullet_sensor")

        # Visuals
        self.RenderObjects["player"] = render.attachNewNode("Render_player")
        self.RenderObjects["level"] = render.attachNewNode("Render_level")
        self.RenderObjects["object"] = render.attachNewNode("Render_object")
        self.RenderObjects["light"] = render.attachNewNode("Render_light")

        ### Engine Holders END ###

        # Setup Bullet Physics
        #? We could save this somewhere else i guess?
        self.bulletWorld = BulletWorld()
        self.bulletWorld.setGravity(Vec3(GRAVITY_X, GRAVITY_Y, GRAVITY_Z))

        # Init Factory
        self.factory = Factory(self)
        # Parse the .egg file
        self.factory.parseLevelFile("test")

        # Init Camera
        self.cameraHandler = CameraHandler(self)

        # Init Input
        self.inputHandler = InputHandler(self)

        # Start Engine Loop
        # Controls Physics and other engine related Things
        taskMgr.add(self.engineLoop, "Engine_Loop")

        print self.havePlayer


    def showBulletDebug(self):
        """Show bullet Debug"""
        # Bullet DEBUG
        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(False)
        debugNP = render.attachNewNode(debugNode)
        debugNP.show()

        self.bulletWorld.setDebugNode(debugNP.node())


    def engineLoop(self, task):
        """Handle Engine Related Tasks"""
        dt = globalClock.getDt()

        # Handle Physics
        self.bulletWorld.doPhysics(dt)
        #self.inputHandler.getMouse(dt)

        if self.havePlayer:
            self.GameObjects["player"].setBasicMovement(dt)


        return task.cont


















