#!/usr/bin/python

#----------------------------------------------------------------------#
# The MIT License (MIT)
# See the license.txt for license information
#----------------------------------------------------------------------#

"""@ package MeoTech

Build a basic Sensor.
"""

# System Imports
import logging as log

# Panda Imports

# Meotech Imports
from sensorPhysics import SensorPhysics

#----------------------------------------------------------------------#

# Sensor
class Sensor():
    """Build a sensor bullet type for different actions"""

    def __init__(self, _engine, _type, _obj, _levelEgg):
        """Sensor Contructor"""
        print "start buidling: ", _obj, " Type: ", _type

        # Engine
        self.engine = _engine

        # Object
        self.object = _obj

        # Get the tags from the object
        self.name = _obj.getTag("sensor")
        self.id = int(_obj.getTag("id"))
        self.model = _obj.getTag("model")
        self.isDynamic = _obj.getTag("isDynamic")
        self.script = _obj.getTag("script")
        self.eventType = _obj.getTag("eventType")
        self.name = self.name+str(self.id)

        # could make custom script act like a instance in here with the self.script as an instance var
        # and when making a custom script for an object/item it must have a class with the same name of the item like
        # Custom script:
        # class MedKit:
        #       def __init__()....

        # States
        self.position = _obj.getPos(_levelEgg)
        self.heading = _obj.getH(_levelEgg)

        self.bulletBody = SensorPhysics.buildItemColSphereNP(
            self.engine, self.object, _levelEgg, self.position, self.heading, self.name)

        # Log
        log.debug("Sensor Builder build: %s" % (self.name))
