#!/usr/bin/python

#----------------------------------------------------------------------#
# The MIT License (MIT)
# See the license.txt for license information
#----------------------------------------------------------------------#


"""@ package BasePhysics

All Physics setups and builders
"""

# System Imports
import logging as log

# Panda Engine Imports
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import BulletBoxShape
from panda3d.core import BitMask32, Vec3

# MeoTech Imports

#----------------------------------------------------------------------#

class SensorPhysics():
    """Handle the Sensor related physics"""

    @classmethod
    def buildItemColSphereNP(cls, _engine, _obj, _level, _pos, _head, _nameId):
        """Build a basic BulletCharacter Controller"""
        
        size = (_obj.getScale() + (0, 3, 0))
        print size
        shape = BulletBoxShape(Vec3(size))
        node = BulletGhostNode(_nameId)
        node.addShape(shape)
        np = _engine.BulletObjects["sensor"].attachNewNode(node)
        np.setPos(_pos)
        np.setH(_head)
        np.setCollideMask(BitMask32.allOff())
        _engine.bulletWorld.attachGhost(node)

        return np

