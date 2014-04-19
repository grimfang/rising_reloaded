"""
Documentation: CharPlayer.py
  Classes and functions:
    ItemHealth
  Description:
    This is the main class for all health items like medipacks
    or other items which heals the player.
"""

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

# System Imports
import logging as log

from engine.config import MODEL_DIR

from healthPhysics import HealthPhysics



class Health():
    """The ItemHealth class set up the model and effects
    of the item types which will heal the player if they
    are collected by him."""

    def __init__(self, _engine, _type, _obj, _levelEgg):
        """MediKit Contructor"""
        print "start buidling: ", _obj, " Type: ", _type

        # Engine
        self.engine = _engine
        self.factory = self.engine.factory

        # Object
        self.object = _obj

        # Get the tags from the object
        self.name = _obj.getTag("object")
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

        self.bulletBody = HealthPhysics.buildItemColSphereNP(
            self.engine, 0.5, self.position, self.heading)
        self.setModel()

        # Log
        log.debug("Health Builder build: %s" % (self.name))


    def setModel(self):
        """Attach the given model to the player"""
        if self.model != "":
            # Setup the visual model
            self.model = loader.loadModel(MODEL_DIR + self.model)
            np = self.engine.RenderObjects["object"].attachNewNode(self.name)
            self.model.reparentTo(np)
            np.reparentTo(self.bulletBody)
