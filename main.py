#!/usr/bin/python

#----------------------------------------------------------------------#
# The MIT License (MIT)
# See the license.txt for license information
#----------------------------------------------------------------------#

"""@ package MeoTech

Run the app
"""

# System Imports
import sys
import os
import logging as log

# Panda Engine Imports
from pandac.PandaModules import loadPrcFileData
loadPrcFileData("",
"""
    window-title Rising Reloaded
    cursor-hidden 0
    show-frame-rate-meter 1
    #want-tk 1
    #want-directtools 1
"""
)

from direct.showbase.ShowBase import ShowBase

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

        # Init Engine
        self.engine = Engine(self)

        # Init Gamewwwwwwwwww
        self.game = Game(self)

        # Debug stuff
        wantDebug = True

        # Run the debug stuff aswell.
        #? Setup a proper debug
        if wantDebug:
            self.engine.showBulletDebug()
            print " "
            print "Panda Render.ls()"
            print "------wwwww--------------------------------------------------"
            print render.ls()
            print "--------------------------------------------------------"


main = Main()
run()



