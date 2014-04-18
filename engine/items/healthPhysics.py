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
from panda3d.bullet import BulletSphereShape
from panda3d.core import BitMask32

# MeoTech Imports

#----------------------------------------------------------------------#

class HealthPhysics():
    """Handle the health item related physics"""

    @classmethod
    def buildItemColSphereNP(cls, _engine, _radius, _pos, _head):
        """Build a basic BulletCharacter Controller"""
        sphere = BulletSphereShape(_radius)
        node = BulletGhostNode('ItemSphere')
        node.addShape(sphere)
        np = _engine.BulletObjects["object"].attachNewNode(node)
        np.setPos(_pos)
        np.setH(_head)
        np.setCollideMask(BitMask32(0xf))
        _engine.bulletWorld.attachGhost(node)

        return np

