#!/usr/bin/python

#----------------------------------------------------------------------#
# The MIT License (MIT)
# See the license.txt for license information
#----------------------------------------------------------------------#


"""@ package Level

This should build a playable level
"""

# System Imports
import logging as log

# Panda Engine Imports
from panda3d.core import BitMask32

# MeoTech Imports
from levelPhysics import LevelPhysics


#----------------------------------------------------------------------#

# BaseLevel
class Level():
    """THis builds the level parts, floor, walls
    TODO: add water functionality with shaders"""
    def __init__(self, _engine, _type, _obj, _levelEgg):
        """BaseLevel Constructor"""
        print "start building: ", _obj, " Type: ", _type

        # Engine
        self.engine = _engine
        self.factory = self.engine.factory
        self.renderObjectsLevel = self.engine.RenderObjects["level"]
        self.levelEgg = _levelEgg

        # Object
        self.object = _obj

        def getBool(text):
            return text.lower() in ("true", "t")

        # Get the tags from the object
        self.name = _obj.getTag("level")
        self.id = int(_obj.getTag("id"))
        self.subType = _obj.getTag("subType")
        self.isDynamic = getBool(_obj.getTag("isDynamic"))
        self.isCollisionMesh = getBool(_obj.getTag("isCollisionMesh"))
        self.isClimbable = getBool(_obj.getTag("isClimbable"))
        self.useBulletPlane = getBool(_obj.getTag("useBulletPlane"))
        self.script = _obj.getTag("script")
        #@ Add a mask getter for the blenderTool Script
        self.wallMask = BitMask32.allOn()

        # States
        self.position = _obj.getPos(_levelEgg)
        self.hpr = _obj.getHpr(_levelEgg)
        self.scale = _obj.getScale(_levelEgg)

        # CollisionBody
        self.bulletBody = None
        self.groundPlane = None

        # Run Checkers
        self.buildSubType()

        # Log
        log.debug("Level Builder build: %s" % (self.name))

    def remove(self):
        self.object.remove()

    #? This needs a re-write
    def buildSubType(self):
        """Build the subType that being either wall or ground"""

        if self.subType == "wallType":
            """Build a wall"""

            if "col" in self.name or self.isCollisionMesh:
                """Build the collision body for this wall"""
                self.bulletBody = LevelPhysics.buildTriangleMesh(self.engine,
                            self.object, self.levelEgg, 0, self.isDynamic)
                self.bulletBody.setCollideMask(self.wallMask)
                self.bulletBody.setTag("Test", "TestingTag")

            else:
                self.object.reparentTo(self.renderObjectsLevel)

        elif self.subType == "groundType":
            """Build the ground with either custom Mesh or use the plane"""
            if self.useBulletPlane is True:
                self.groundPlane = LevelPhysics.buildGroundPlane(self.engine)

                self.object.reparentTo(self.renderObjectsLevel)
                self.object.setPos(self.position)
                self.object.setHpr(self.hpr)

            else:
                if "col" in self.name or self.isCollisionMesh:
                    self.bulletBody = LevelPhysics.buildTriangleMesh(self.engine,
                            self.object, self.levelEgg, 0, self.isDynamic)
                    self.bulletBody.setCollideMask(BitMask32.allOn())

                else:
                    self.object.reparentTo(self.renderObjectsLevel)
                    self.object.setPos(self.position)
                    self.object.setHpr(self.hpr)
