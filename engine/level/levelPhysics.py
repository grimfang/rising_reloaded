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
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletTriangleMesh, BulletTriangleMeshShape
from panda3d.core import Vec3, BitMask32

# MeoTech Imports

#----------------------------------------------------------------------#

class LevelPhysics():
    """Handles Physics related things for the levels"""

    # Build a basic ground plane
    @classmethod
    def buildGroundPlane(cls, _engine, _name='Ground_plane'):
        """Build a BulletPlane"""
        shape = BulletPlaneShape(Vec3(0, 0, 1), 0)
        np = _engine.BulletObjects["level"].attachNewNode(
                                    BulletRigidBodyNode(_name))
        np.node().addShape(shape)
        np.setPos(0, 0, 0) # This thing is usually infinite
        np.setCollideMask(BitMask32.allOn())

        _engine.bulletWorld.attachRigidBody(np.node())

        return np


    # build a more complicated triaglemesh
    @classmethod
    def buildTriangleMesh(cls, _engine, _obj, _levelEgg, _mass=0, _isDynamic=False):
        """Build a bullet TriangleMesh for objects"""

        mesh = BulletTriangleMesh()
        node = _obj.node()

        if node.isGeomNode():
            mesh.addGeom(node.getGeom(0))
        else:
            return

        body = BulletRigidBodyNode(_obj.getTag("level"))#+str(_obj.getTag("id")))
        body.addShape(BulletTriangleMeshShape(mesh, dynamic=_isDynamic))
        body.setMass(_mass)

        np = _engine.BulletObjects["level"].attachNewNode(body)
        #np.setCollideMask(BitMask32.allOn())
        np.setScale(_obj.getScale(_levelEgg))
        np.setPos(_obj.getPos(_levelEgg))
        np.setHpr(_obj.getHpr(_levelEgg))

        _engine.bulletWorld.attachRigidBody(body)

        return np
