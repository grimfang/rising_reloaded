#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Documentation: GraphicManager.py
  Classes and functions:
    GraphicManager
  Description:
    The graphic manager handles everything around the graphic of the game
    it will be able to set filters (like bloom), shaders and graphic quality
    settings as well as window settings like fullscreen and screen resolution.
"""

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

import logging

from panda3d.core import AntialiasAttrib
from pandac.PandaModules import WindowProperties

class GraphicManager():
    """
    The graphic manager will handle all things around the graphics of the game.
    It will be able to set the graphics quality, an handle pre- and
    postprocessing like shaders.
    """
    def __init__(self, settings):
        logging.debug("load graphic manager")
        self.setGraphicQuality(settings.graphicquality)

    def loadCoreGraphic(self, settings):
        """
        This function should be called at the very beginning of the
        game, as it will load and set all the default graphic settings
        """
        self.setGraphicQuality(settings.graphicquality)
        self.setFullscreen(settings.fullscreen)

    def setGraphicQuality(self, quality):
        """
        This function will set a given preset of quality settings dependend
        on the given quality value, the higher the value, the better the
        resulting graphics.
        quality = int
        """
        self.setAntialias(quality > 1)
        self.setShaderGenerator(quality > 0)
        if quality > 1: self.shadowMapSize = 1024
        else: self.shadowMapSize = 512

    def setResolution(self, resx, resy):
        props = WindowProperties()
        props.setSize(resx, resy)
        base.win.requestProperties(props)
        base.camLens.setAspectRatio(float(resx)/float(resy))
        base.taskMgr.step()

    def setAntialias(self, active):
        """
        de-/activate antialiasing
        """
        if active:
            #base.render.setAntialias(AntialiasAttrib.MAuto)
            base.render.setAntialias(AntialiasAttrib.MMultisample)
        else:
            base.render.setAntialias(AntialiasAttrib.MNone)

    def setShaderGenerator(self, active):
        """
        de-/activate pandas shader generater, which handle things like
        perpixel lighting and other shader related settings
        """
        if active:
            base.render.setShaderAuto()
        else:
            base.render.clearShader()

    def setFullscreen(self, settings):
        """Set the window to fullscreen or windowed mode depending on the
        configuration in the settings variable"""
        props = WindowProperties()
        props.setFullscreen(settings.fullscreen)
        props.setUndecorated(settings.fullscreen)
        if settings.fullscreen:
            props.setSize(settings.windowSize[0], settings.windowSize[1])
        base.win.requestProperties(props)
        base.taskMgr.step()
