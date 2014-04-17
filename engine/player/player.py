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

# MeoTech Imports
from config import *

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
        
        # States
        self.position = _obj.getPos(_levelEgg)
        self.heading = _obj.getH(_levelEgg)
        
        # Player Collision Body
        self.bulletBody = None
        self.useBasicMovement = False
        
        # Run checkers
        self.setControlType()
        self.setModel()
        # TODO: Load scripts for this object...
        
        # Log
        log.debug("Player Builder build: %s" % (self.name))
    
    #? Needs a re-write
    def setControlType(self):
        
        # Check Fps Style
        if self.control == "controlType0":
            """Add a Fps Type cam and controller"""
            # Add character controler from bullet
            # Add the fps style camera
            self.bulletBody = self.factory.basePhysics.buildCharacterController(
                        self.height, self.radius, self.position, self.heading)
            
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
            model.reparentTo(self.bulletBody)

