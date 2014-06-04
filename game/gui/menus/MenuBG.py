#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Documentation: .py
  Classes and functions:
    N.A.
  Description:
    this class handles the main menu seen on startup.
"""

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from math import pi, sin, cos
from panda3d.core import PointLight
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import PerspectiveLens
from panda3d.core import VBase4, VBase3

class MenuBG():
    def __init__(self):
        self.hotelModel = loader.loadModel("menuBG/menuback")
        self.hotelModel.reparentTo(render)
        self.hotelModel.stash()

        # setup some lights
        plight = PointLight("mapgen_plight")
        plight.setColor(VBase4(0.45, 0.35, 0.35, 1))
        self.plnp = self.hotelModel.attachNewNode(plight)
        self.plnp.setPos(-3, 3, 5)
        base.render.setLight(self.plnp)

        # setup a default ambient light
        alight = AmbientLight("mapgen_alight")
        alight.setColor(VBase4(0.20, 0.20, 0.28, 1))
        self.alnp = self.hotelModel.attachNewNode(alight)
        base.render.setLight(self.alnp)

        sun = DirectionalLight('sun')
        sun.setColor(VBase4(0.8, 0.8, 0.8, 1))
        lens = PerspectiveLens()
        lens.setFar(50)
        lens.setFov(80, 80)
        sun.setLens(lens)
        ms = 1024 #graphicMgr.shadowMapSize
        sun.setShadowCaster(True, ms, ms)
        self.sunnp = self.hotelModel.attachNewNode(sun)
        self.sunnp.setHpr(85, -50, 0)
        self.sunnp.setPos(12, 0, 10)
        base.render.setLight(self.sunnp)

        #testmodel = loader.loadModel("misc/Spotlight")
        #testmodel.reparentTo(self.sunnp)

    def startBGLoop(self):
        if not taskMgr.hasTaskNamed("MenuCameraFly"):
            self.hotelModel.unstash()
            base.render.setLight(self.plnp)
            base.render.setLight(self.alnp)
            base.render.setLight(self.sunnp)
            taskMgr.add(self.bgLoop, "MenuCameraFly")

    def stopBGLoop(self):
        if taskMgr.hasTaskNamed("MenuCameraFly"):
            taskMgr.remove("MenuCameraFly")
            self.hotelModel.stash()
            base.render.clearLight(self.plnp)
            base.render.clearLight(self.alnp)
            base.render.clearLight(self.sunnp)

    def bgLoop(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        base.camera.setPos(
                         VBase3(18 * sin(angleRadians),
                                -18.0 * cos(angleRadians),
                                10))
        base.camera.setHpr(
                         VBase3(angleDegrees,
                                -25,
                                0))

        base.camera.lookAt(self.hotelModel)
        return task.cont
