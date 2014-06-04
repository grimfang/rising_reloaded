#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Documentation: logomanager.py
  Classes and functions:
    N.A.
  Description:
    this class handles all around the intro Outro and Logo Videos
"""

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

import sys
import logging

from pandac.PandaModules import MovieTexture
from panda3d.core import CardMaker
from panda3d.core import NodePath
from panda3d.core import TextureStage
from panda3d.core import AudioSound

class MovieManager():

    def __init__(self):
        self.vidFinEvt = "videoabFinished"
        self.sound = None
        self.card = None

    def showVideo(self, video, eventName):
        # check if a video run
        if taskMgr.hasTaskNamed("task_isVideoFinised"):
            # if so, stop that video
            self.stopVideo()
        self.vidFinEvt = eventName
        # play the new video
        self.playVideo(video)

    def setVideoFinishEvent(self, eventName):
        self.vidFinEvt = eventName

    def playVideo(self, video):
        # check if it is loadable
        try:
            # load the video texture
            self.tex = MovieTexture("MovieTexture")
            #print video
            self.tex.read(video)
            # Set up a fullscreen card to set the video texture on it.
            cm = CardMaker("Movie Card")
            cm.setFrameFullscreenQuad()
            cm.setUvRange(self.tex)
            self.card = NodePath(cm.generate())
            self.card.reparentTo(base.render2d)
            self.card.setTexture(self.tex)
            self.card.setTexScale(TextureStage.getDefault(),
                                  self.tex.getTexScale())

            # load the video
            self.sound = loader.loadSfx(video)

            # Synchronize the video to the sound.
            self.tex.synchronizeTo(self.sound)

            # play the video and audio
            self.sound.play()
            # start the task which checks if the video is finished
            taskMgr.add(self.isVideoFinish, "task_isVideoFinised")
        except:
            logging.error("Failed to load video: %s %s", video, sys.exc_info())
            self.stopVideo()
            base.messenger.send(self.vidFinEvt)

    def stopVideo(self):
        if self.card != None:
            self.card.remove()
        if self.sound != None:
            self.sound.stop()

    def isVideoFinish(self, task):
        if(self.sound.status() != AudioSound.PLAYING):
            logging.debug("video finished")
            self.stopVideo()
            base.messenger.send(self.vidFinEvt)
            return task.done
        return task.cont
