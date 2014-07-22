#!/usr/bin/python

#----------------------------------------------------------------------#
# The MIT License (MIT)
# See the license.txt for license information
#----------------------------------------------------------------------#

"""@ package MeoTech
Run the app
"""

# System Imports
import logging as log


# Panda Engine Imports
# win-size 1152 876
from pandac.PandaModules import loadPrcFileData
loadPrcFileData("",
"""
    window-title Rising Reloaded
    cursor-hidden 0
    show-frame-rate-meter 1
    #want-tk 1
    #want-directtools 1
    model-path $MAIN_DIR/game/assets/levels/
    model-path $MAIN_DIR/game/assets/models/
    model-path $MAIN_DIR/game/assets/textures/
    model-path $MAIN_DIR/game/assets/music/
    model-path $MAIN_DIR/game/assets/sfx/
"""
)

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject

# MeoTech Imports
from engine.engine import Engine
from game.game import Game
#----------------------------------------------------------------------#
# Info!

# Main
class Main(ShowBase):
    """Main Class
    Handles the setup of the whole app.
    """

    def __init__(self):

        # Create the main app Log file
        log.basicConfig(
                        filename="main.log",
                        level=log.DEBUG,
                        format="%(asctime)s %(levelname)s: %(message)s",
                        datafmt="%d-%m-%Y %H:%M:%S")


        # Init Panda
        ShowBase.__init__(self)
        self.disableMouse()

        # Init Engine
        self.engine = Engine(self)

        # Init Game
        self.game = Game(self)

        # Debug stuff
        wantDebug = False

        # Run the debug stuffww aswell.
        #? Setup a proper debug
        if wantDebug:
            #do = DirectObject()
            #do.accept("f11", self.engine.gm.setFullscreen, [True])
            #do.accept("f12", self.engine.gm.setFullscreen, [False])
            self.engine.showBulletDebug()
            print " "
            print "Panda Render.ls()"
            print "--------------------------------------------------------"
            print render.ls()
            print "--------------------------------------------------------"

    def quit(self):
        if self.appRunner:
            self.appRunner.stop()
        else:
            exit(0)

main = Main()
run()



