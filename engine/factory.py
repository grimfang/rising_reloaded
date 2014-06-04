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
#from panda3d.core import NodePath

# MeoTech Imports
#from config import *
from player.player import Player
from level.level import Level
from lights.light import Light
from items.health import Health
from sensors.sensor import Sensor

#----------------------------------------------------------------------#

## Types
OBJECT_TYPES = ["player", "level", "object", "light", "sensor"]


# Factory
class Factory():
    """The factory handles the building of levels and all the objects,
    lights, sensors... in them.
    """
    def __init__(self, _engine):

        print "Factory - init >>>"
        log.info("Factory - init >>>")

        # Engine
        self.engine = _engine


    def parseLevelFile(self, _eggPath):

        # Egg file
        levelEgg = loader.loadModel(_eggPath)

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
            self.engine.GameObjects["player"] = Player(self.engine,
                            _type, _obj, _levelEgg)

        # Level Type
        if _type == "level":
            self.engine.GameObjects["level"][_obj.getTag("level")] = Level(self.engine,
                            _type, _obj, _levelEgg)

        # Object Type
        if _type == "object":
            #TODO: need differentiation between objects
            self.engine.GameObjects["object"][_obj.getTag("object")+_obj.getTag("id")] = Health(self.engine,
                            _type, _obj, _levelEgg)

        # Sensor Type
        if _type == "sensor":
            self.engine.GameObjects["sensor"][_obj.getTag("sensor")+_obj.getTag("id")] = Sensor(self.engine,
                            _type, _obj, _levelEgg)

        # Light Type
        if _type == "light":
            self.engine.GameObjects["light"][_obj.getTag("light")] = Light(
                            self.engine, _type, _obj, _levelEgg)






































