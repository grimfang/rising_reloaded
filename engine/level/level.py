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

# MeoTech Imports
from engine.config import *
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
        
        # Get the tags from the object
        self.name = _obj.getTag("level")
        self.id = int(_obj.getTag("id"))
        self.subType = _obj.getTag("subType")
        self.isDynamic = _obj.getTag("isDynamic")
        self.isCollisionMesh = _obj.getTag("isCollisionMesh")
        self.isClimbable = _obj.getTag("isClimbable")
        self.useBulletPlane = _obj.getTag("useBulletPlane")
        self.script = _obj.getTag("script")
        
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
        
    #? This needs a re-write    
    def buildSubType(self):
        """Build the subType that being either wall or ground"""
        
        if self.subType == "wallType":
            """Build a wall"""
            
            if "col" in self.name:
                """Build the collision body for this wall"""
                self.bulletBody = LevelPhysics.buildTriangleMesh(self.engine,
                            self.object, self.levelEgg, 0, self.isDynamic)
                self.bulletBody.setTag("Test", "TestingTag")
            
            else:
                self.object.reparentTo(self.renderObjectsLevel)
        
        elif self.subType == "groundType":
            """Build the ground with either custom Mesh or use the plane"""
            if self.useBulletPlane:
                self.groundPlane = LevelPhysics.buildGroundPlane(self.engine)
                
                self.object.reparentTo(self.renderObjectsLevel)
                self.object.setPos(self.position)
                self.object.setHpr(self.hpr)
            
            else:
                
                if "col" in self.name:
                    self.bulletBody = LevelPhysics.buildTriangleMesh(self.engine,
                            self.object, self.levelEgg, 0, self.isDynamic)
                
                else:
                    self.object.reparentTo(self.renderObjectsLevel)
                    self.object.setPos(self.position)
                    self.object.setHpr(self.hpr)
