#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Documentation: CharPlayerFSM.py
  Classes and functions:
    CharPlayerFSM
  Description:
    This modul contains the FSM class for the player characters
    and will handle all the possible states of the character.
    As this Class doesn't raly know anything about the player
    all it does is sending events, which then should be cought
    in the CharPlayer Class.
"""

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.fsm.FSM import FSM

class PlayerFSM(FSM):
    """Char Finit State Machine handles all animations and audio
    which is going to be played while the avatar is moving or doing
    anything else"""
    def __init__(self, charClass):
        self.char = charClass
        FSM.__init__(self, "player" + str(self.char.id) + "FSM")

    def enterWalk(self):
        """Char enter walking stage so animate the characters
        walkcycle and play some walking sounds"""
        self.char.setLoop("walk", "True")

    def exitWalk(self):
        """Char stops walking so stop to
        animate and stop the walking sound"""
        self.char.setLoop("none", "True")

    def enterRun(self):
        """Char enter walking stage so animate the characters
        walkcycle and play some walking sounds"""
        self.char.setLoop("run", "True")

    def exitRun(self):
        """Char stops walking so stop to
        animate and stop the walking sound"""
        self.char.setLoop("none", "True")

    def enterBackward(self):
        """Char walk backward play walkcycle
        animation and walking sound"""
        self.char.setLoop("back", "True")

    def exitBackward(self):
        """Char stop to walk backward,
        so stop animation and sound"""
        self.char.setLoop("none", "True")

    def enterIdle(self):
        """Char stands still on the place,
        start the idle animation"""
        self.char.setLoop("idle", "True")

    def exitIdle(self):
        """The char is doing something now...
        so stop the idle animation"""
        self.char.setLoop("none", "True")

    def enterJump(self):
        """Start the Jumping"""
        self.char.setLoop("jump", "False")

    def exitJump(self):
        """The character is back on the ground
        or something else hapend"""
        self.char.setLoop("none", "True")

    def enterClimb(self):
        """Start the climbing"""
        self.char.setLoop("climb", "True")

    def exitClimb(self):
        """The character is off of the climbeable
        object"""
        self.char.setLoop("none", "True")

    def enterWallRun(self, direction):
        """Start a wall run on the given side
        possible directions are left, right and up"""
        if direction == "left":
            self.char.setLoop("wallRun_l", "True")
        elif direction == "right":
            self.char.setLoop("wallRun_r", "True")
        elif direction == "up":
            self.char.setLoop("wallRun_up", "True")

    def exitWallRun(self):
        """The character stopped the wall run"""
        self.char.setLoop("none", "True")

    def enterFall(self):
        """The character falls down"""
        self.char.setLoop("jump", "True", [9,11], 0.5)

    def exitFall(self):
        """The character falls down"""
        self.char.setLoop("none", "True")

    def enterStopAnim(self):
        """Just stops the current animation at the
        aktive frame"""
        self.char.setLoop("none", "True")

    def exitStopAnim(self):
        pass

