#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Documentation: .py
  Classes and functions:
    N.A.
  Description:
    the audio Manager handles everything about sound and audio, playing sounds
    and music and everything else about that.
"""

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.showbase import Audio3DManager
from panda3d.core import AudioSound

# Audio file paths

class AudioManager:
    """The AduioManager class handles all audio out and input.
    It's caled, when an audio file should be played, or to set
    audio options, like all sounds should be muted."""

    def __init__(self):

        self.__soundList = {}
        self.__musicList = {}

        self.sfxMgr = base.sfxManagerList[0]
        self.audio3d = Audio3DManager.Audio3DManager(
            self.sfxMgr,
            base.camera)
        self.musicMgr = base.musicManager

    def loadCoreAudio(self, settings):
        """This function should be called at the very beginning of the
        game, as it will load all the default audio files from the Music
        and SFX list modules"""
        from media import MusicList
        from media import SFXList

        for sfx, path in SFXList.sfxList.items():
            self.addSound(sfx, path)

        for track, path in MusicList.musicList.items():
            self.addMusic(track, path)

        self.mute(settings.muted)
        self.setVolume(settings.volume)

    def attachSound(self, sndName, obj):
        """Attach the given sound to the object for 3D effect"""
        sound = self.__soundList[sndName]
        self.audio3d.attachSoundToObject(sound, obj)

    def addSound(self, sndName, path, loop=True, volume=1.0):
        """Add a new sound to the sound list. The name should always be an
        enum value of AudioManager.Sounds"""
        self.__soundList[sndName] = self.audio3d.loadSfx(path)
        self.__soundList[sndName].setVolume(volume)
        self.__soundList[sndName].setLoop(loop)

    def playSFX(self, sound=""):
        """Play the given audio"""
        if self.__soundList[sound] != None:
            self.__soundList[sound].play()

    def stopSFX(self, sound=""):
        """stops the playing of a given audio"""
        if self.__soundList[sound] != None:
            self.__soundList[sound].stop()

    def isSFXPlaying(self, sound):
        """check if the given sound is already playing"""
        if self.__soundList[sound] == None: return False
        return self.__soundList[sound].status() == AudioSound.PLAYING

    def addMusic(self, track, path, loop=True, volume=1.0):
        self.__musicList[track] = base.loadMusic(path)
        self.__musicList[track].setVolume(volume)
        self.__musicList[track].setLoop(loop)

    def playMusic(self, track=""):
        """Play the given music track"""
        if self.__musicList[track] != None:
            self.__musicList[track].play()

    def stopMusic(self, track=""):
        """Stops the playing of a given music track"""
        if self.__musicList[track] != None:
            self.__musicList[track].stop()

    def isMusicPlaying(self, track):
        if self.__musicList[track] == None: return False
        return self.__musicList[track].status() == AudioSound.PLAYING

    def mute(self, mute):
        if mute:
            base.disableAllAudio()
        else:
            base.enableAllAudio()

    def muteSFX(self, mute):
        base.enableSoundEffects(mute)

    def muteMusic(self, mute):
        base.enableMusic(mute)

    def setVolume(self, volume):
        self.sfxMgr.setVolume(volume)
        self.musicMgr.setVolume(volume)
