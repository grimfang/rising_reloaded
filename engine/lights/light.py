#!/usr/bin/python

#----------------------------------------------------------------------#
# The MIT License (MIT)
# See the license.txt for license information
#----------------------------------------------------------------------#


"""@ package BaseObject

Classes for the BaseObjects types.
Each type of object from the level.egg file will be build from these.
"""

# System Imports
import logging as log

# Panda Engine Imports
from panda3d.core import PointLight, DirectionalLight, Spotlight, AmbientLight
from panda3d.core import VBase4, PerspectiveLens

# MeoTech Imports
from config import *

#----------------------------------------------------------------------#

# BaseLight
class Light():
    """Light:
    Make some lights :)
    """
    def __init__(self, _engine, _type, _obj, _levelEgg):
        """BaseLights Constructor"""
        print "start building: ", _obj, " Type: ", _type
        
        # Engine
        self.engine = _engine
        self.factory = self.engine.factory
        self.renderObjectsLight = self.engine.RenderObjects["light"]
        
        # Object
        self.object = _obj
        
        # get the tags from the object
        self.name = _obj.getTag("light")
        self.id = int(_obj.getTag("id"))
        self.subType = _obj.getTag("subType")
        self.model = _obj.getTag("model")
        self.isDynamic = _obj.getTag("isDynamic")
        self.script = _obj.getTag("script")
        self.color = self.getColor(_obj.getTag("color"))
        self.lookAt = _obj.getTag("lookAt")
        
        # NodePath
        self.lightNP = None
        
        # States
        self.position = _obj.getPos(_levelEgg)
        self.hpr = _obj.getHpr(_levelEgg)
        self.h = _obj.getH(_levelEgg)
        
        # Run Checkers
        self.buildSubType()
        # Log
    
    def buildSubType(self):
        """Build the light with the given subType"""
        
        if self.subType == "pointType":
            # make a point light
            c = self.color
            pointLight = PointLight(self.name)
            pointLight.setColor(VBase4(c[0], c[1], c[2], c[3]))
            plnp = self.renderObjectsLight.attachNewNode(pointLight)
            plnp.setPos(self.position)
            self.lightNP = plnp
            self.setLightSwitch(True)
            
        if self.subType == "directType":
            # make a directional light
            c = self.color
            directLight = DirectionalLight(self.name)
            directLight.setColor(VBase4(c[0], c[1], c[2], c[3]))
            dlnp = self.renderObjectsLight.attachNewNode(directLight)
            dlnp.setHpr(0, -60, 0) # no idea why its like that.. but it works
            self.lightNP = dlnp
            self.setLightSwitch(True)
            
            
        if self.subType == "ambientType":
            # make a ambient light
            c = self.color
            ambientLight = AmbientLight(self.name)
            ambientLight.setColor(VBase4(c[0], c[1],c[2], c[3]))
            alnp = self.renderObjectsLight.attachNewNode(ambientLight)
            self.lightNP = alnp
            self.setLightSwitch(True)
            
        if self.subType == "spotType":
            # make a spot light
            # lookAtObj = _object.getTag("lookAt") get rid of this.
            c = self.color
            spotLight = Spotlight(self.name)
            spotLight.setColor(VBase4(c[0], c[1], c[2], c[3]))
            lens = PerspectiveLens()
            spotLight.setLens(lens)
            slnp = self.renderObjectsLight.attachNewNode(spotLight)
            slnp.setPos(self.position)
            slnp.setHpr(self.hpr)
            # Find out if this is really the only option
            # because setHpr doesnt seem to have any effect.
            # lookAt would be okay but that means adding anothe type
            #slnp.lookAt(self.main.GameObjects["player"].collisionBody)
            self.lightNP = slnp
            self.setLightSwitch(True)
    
    def getColor(self, _color):
        """Get the color and convert it from the string tag"""
        c = _color.split()
        
        for n in range(len(c)):
            c[n] = float(c[n])
        
        return c
        
    def setLightSwitch(self, _state=False):
        """Set the light on or off."""
        if _state == True:
            render.setLight(self.lightNP)
        elif _state == False:
            render.clearLight(self.lightNP)
