#!/usr/bin/python

#----------------------------------------------------------------------#
# The MIT License (MIT)
# See the license.txt for license information
#----------------------------------------------------------------------#

"""@ package MeoTech

Start the Engine Factory.
"""

# System Imports
import logging as log

# Panda Engine Imports
from panda3d.core import NodePath

# MeoTech Imports
from config import *
#? Redo imports for each type of object

#----------------------------------------------------------------------#

# Factory
class Factory():
    """The factory handles the building of levels and all the objects,
    lights, sensors... in them.
    """
    def __init__(self, _engine):
        
        print "Factory - init >>>"
        
        # Engine
        self.engine = _engine
        

    def parseLevelFile(self, _eggPath):
        
        # Egg file
        levelEgg = loader.loadModel(LEVEL_DIR + _eggPath)
        
        # Find objects in levelEgg
        levelObjects = levelEgg.findAllMatches('**')
        
        for obj in levelObjects:
            for type in OBJECT_TYPES:
                if obj.hasTag(type):
                    self.build(type, obj, levelEgg)
                    
    
    #? This will need a re-write
    def build(self, _type, _obj, _levelEgg):
        
        # Build Object with _type
        
        # Player Type
        if _type == "player":
            self.engine.GameObjects["player"] = BasePlayer(self.engine,
                            _type, _obj, _levelEgg)
        
        # Level Type
        if _type == "level":
            self.engine.GameObjects["level"][_obj.getTag("level")] = BaseLevel(self.engine, 
                            _type, _obj, _levelEgg)
            
        ## Object Type
        #if _type == "object":
        #    self.engine.GameObjects["object"][_obj.getTag("object")] = bObject(self.engine, 
        #                    _type, _obj, _levelEgg)
            
        # Light Type
        if _type == "light":
            self.engine.GameObjects["light"][_obj.getTag("light")] = BaseLight(
                            self.engine, _type, _obj, _levelEgg)
            
        # Sensor Type
        if _type == "sensor":
            self.engine.GameObjects["sensor"][_obj.getTag("sensor")] = BaseSensor()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
