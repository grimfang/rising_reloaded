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
from direct.showbase.DirectObject import DirectObject

# MeoTech Imports
from factory import Factory
#from config import *
from settings import Settings
from input.input import InputHandler
from camera.camera import CameraHandler
from eventHandler import EventHandler
from graphic.graphicManager import GraphicManager
from media.audioManager import AudioManager
from language import Language

#----------------------------------------------------------------------#

# Engine
class Engine(DirectObject):
    """The engine class sets up the holders for game GameObjects
    and starts the parser that runs through the [name].egg
    """
    def __init__(self, _main):

        print "Engine - init >>>"
        log.info("Engine - init >>>")


        # Main ref
        self.main = _main
        self.settings = Settings()
        self.graphicMgr = GraphicManager(self.settings)
        self.audioMgr = AudioManager()
        self.lng = Language(self.settings)
        self.lng.setup(self.settings)

        ### Bools ###
        # Gets set if we have a player character to work with.
        self.hasPlayer = False
        ### Bools END ###

        ### Setup Engine Holders ###
        self.__resetObjects()
        ### Engine Holders END ###

        # Setup Bullet Physics
        #? We could save this somewhere else i guess?
        self.bulletWorld = BulletWorld()
        self.bulletWorld.setGravity(
            Vec3(self.settings.gravity_x,
                 self.settings.gravity_y,
                 self.settings.gravity_z))

        # Init Factory
        self.factory = Factory(self)

        # Debug node
        self.debugNP = None

    def start(self):
        # Controls Physics and other engine related Things
        # Init Camera
        self.cameraHandler = CameraHandler(self, "TPA")

        # Init Input
        self.inputHandler = InputHandler(self)

        # Event HAndler
        self.eventHandler = EventHandler(self)

        # Start Engine Loop
        taskMgr.add(self.engineLoop, "Engine_Loop")

    def unloadLevel(self):
        self.__removeObjects()

    def loadLevel(self, levelName):
        # Parse the .egg file
        self.factory.parseLevelFile(levelName)

    def __resetObjects(self):
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

    def __removeObjects(self):
        for name, objects in self.GameObjects:
            if name == "player":
                objects.remove()
                continue
            for name, obj in objects:
                obj.remove()


    def showBulletDebug(self):
        """Show bullet Debug"""
        # Bullet DEBUG
        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(False)
        self.debugNP = render.attachNewNode(debugNode)
        self.debugNP.show()

        self.bulletWorld.setDebugNode(self.debugNP.node())

    def hideBulletDebug(self):
        """Hide the debug stuff"""

        self.debugNP.hide()


    def engineLoop(self, task):
        """Handle Engine Related Tasks"""
        dt = globalClock.getDt()

        # Handle Physics
        self.bulletWorld.doPhysics(dt)

        if self.hasPlayer:
            self.inputHandler.update(dt)
            self.cameraHandler.update(dt)
            self.GameObjects["player"].setBasicMovement(dt)
            self.GameObjects["player"].startContactTester(dt)



        return task.cont


















