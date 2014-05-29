#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Documentation: .py
  Classes and functions:
    N.A.
  Description:
    This class handles all the menus for setting the options of the game
"""

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from menus.Menu import Menu
from direct.gui.DirectGui import DirectOptionMenu
from direct.gui.DirectGui import DirectSlider
from direct.gui.DirectCheckBox import DirectCheckBox
from direct.gui.DirectGui import DirectLabel
from direct.gui.DirectGui import DirectRadioButton
from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DirectScrolledList
from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import OkCancelDialog
from panda3d.core import TextNode


class MenuOptions(Menu):

    def __init__(self):
        """
        This function will initialise the main screen of the options
        and prepare the tabs with the various settings
        """
        Menu.__init__(self)

        self.initGeneralTab()
        self.initControlTab()

        self.currentTab = [0]

        self.tabGroup = [
            DirectRadioButton(
                text = _("General"),
                variable = self.currentTab,
                value = [0],
                scale = 0.05,
                pos = (-0.6, 0, 0.65),
                command = self.showGeneralTab),
            DirectRadioButton(
                text = _("Controls"),
                variable = self.currentTab,
                value = [1],
                scale = 0.05,
                pos = (0.6, 0, 0.65),
                command = self.showControlTab)
            ]

        for tab in self.tabGroup:
            tab.reparentTo(self.frameMain)
            tab.setOthers(self.tabGroup)

        # set the text of all GUI elements
        self.setText()

        self.hideBase()

    def initGeneralTab(self):
        """
        This function will set up the content of the
        general tab
        """
        self.frameGeneral = DirectFrame(
            # size of the frame
            frameSize = (base.a2dLeft, base.a2dRight,
                         -0.6, 0.6),
            # position of the frame
            pos = (0, 0, 0),
            # tramsparent bg color
            frameColor = (0, 0, 0, 0.5))

        yPos = 0.45
        shiftY = 0.25

        self.lblLanguage = DirectLabel(
            text = _("Language"),
            scale = 0.15,
            pos = (base.a2dLeft + 0.25, 0, yPos),
            frameColor = (0,0,0,0),
            text_fg = (1,1,1,1),
            text_font = self.defaultFont,
            text_align = TextNode.ALeft)

        self.cmbLanguage = DirectOptionMenu(
            text = "languages",
            scale = 0.15,
            pos = (base.a2dRight - 1.5, 0, 0.45),
            items = ["Deutsch","English","русский", "français"],
            initialitem = 0,
            highlightColor = (0.65,0.65,0.65,1),
            text_font = self.defaultFontRegular,
            item_text_font = self.defaultFontRegular,
            command = self.cmbLanguage_SelectionChanged)

        yPos -= shiftY

        self.lblResolution = DirectLabel(
            text = _("Screen resolution"),
            scale = 0.15,
            pos = (base.a2dLeft + 0.25, 0, yPos),
            frameColor = (0,0,0,0),
            text_fg = (1,1,1,1),
            text_font = self.defaultFont,
            text_align = TextNode.ALeft)

        # get the display resolutions
        di = base.pipe.getDisplayInformation()
        sizes = []
        for index in range(di.getTotalDisplayModes()):
            tmptext = "{0}x{1}".format(
                di.getDisplayModeWidth(index),
                di.getDisplayModeHeight(index))
            if not tmptext in sizes:
                sizes.append(tmptext)

        self.cmbResolution = DirectOptionMenu(
            text = "resolutions",
            scale = 0.15,
            pos = (base.a2dRight - 1.5, 0, yPos),
            items = sizes,
            initialitem = 0,
            highlightColor = (0.65, 0.65, 0.65, 1),
            text_font = self.defaultFontRegular,
            item_text_font = self.defaultFontRegular,
            command = self.cmbResolution_SelectionChanged)

        yPos -= shiftY

        self.lblGraphicQuality = DirectLabel(
            text = _("Graphic quality"),
            scale = 0.15,
            pos = (base.a2dLeft + 0.25, 0, yPos),
            frameColor = (0,0,0,0),
            text_fg = (1,1,1,1),
            text_font = self.defaultFont,
            text_align = TextNode.ALeft)

        self.graphicqualityTextMap = {
            0:_("Low"),
            1:_("Medium"),
            2:_("High")}
        self.sliderGraphicQuality = DirectSlider(
            scale = 0.5,
            pos = (base.a2dRight - 1, 0, yPos + 0.05),
            range = (0,2),
            scrollSize = 1,
            text = self.graphicqualityTextMap[settings.graphicquality],
            text_scale = 0.25,
            text_align = TextNode.ALeft,
            text_pos = (1.1, -0.1),
            text_fg = (1,1,1,1),
            text_font = self.defaultFont,
            value = settings.graphicquality,
            command = self.sliderGraphicQuality_ValueChanged)

        yPos -= shiftY

        self.lblVolume = DirectLabel(
            text = _("Volume"),
            scale = 0.15,
            pos = (base.a2dLeft + 0.25, 0, yPos),
            frameColor = (0,0,0,0),
            text_fg = (1,1,1,1),
            text_font = self.defaultFont,
            text_align = TextNode.ALeft)

        self.sliderVolume = DirectSlider(
            scale = 0.5,
            pos = (base.a2dRight - 1, 0, yPos + 0.05),
            range = (0,1),
            scrollSize = 0.01,
            text = str(int(settings.volume * 100)) + "%",
            text_scale = 0.25,
            text_align = TextNode.ALeft,
            text_pos = (1.1, -0.1),
            text_fg = (1,1,1,1),
            text_font = self.defaultFont,
            value = settings.volume,
            command = self.sliderVolume_ValueChanged)

        yPos -= shiftY

        self.lblVolumeMute = DirectLabel(
            text = _("Mute"),
            scale = 0.15,
            pos = (base.a2dLeft + 0.25, 0, yPos),
            frameColor = (0,0,0,0),
            text_fg = (1,1,1,1),
            text_font = self.defaultFont,
            text_align = TextNode.ALeft)

        self.cbVolumeMute = DirectCheckBox(
            text = "X",
            pos = (base.a2dRight - 1, 0, yPos),
            scale = (0.25, 0.25, 0.25),
            command = self.cbVolumeMute_CheckedChanged,
            rolloverSound = None,
            clickSound = None,
            relief = 0,
            pressEffect = False,
            #frameColor = (0,0,0,0),
            checkedImage = "gui/buttons/options/SoundSwitch_off.png",
            uncheckedImage = "gui/buttons/options/SoundSwitch_on.png"
            )
        self.cbVolumeMute.setTransparency(1)
        self.cbVolumeMute.setImage()
        self.cbVolumeMute["image_scale"] = 0.25
        self.cbVolumeMute["text"] = ""

        self.createBackButton(self.btnBack_Click)

        self.lblLanguage.reparentTo(self.frameGeneral)
        self.cmbLanguage.reparentTo(self.frameGeneral)
        self.lblResolution.reparentTo(self.frameGeneral)
        self.cmbResolution.reparentTo(self.frameGeneral)
        self.lblGraphicQuality.reparentTo(self.frameGeneral)
        self.sliderGraphicQuality.reparentTo(self.frameGeneral)
        self.lblVolume.reparentTo(self.frameGeneral)
        self.sliderVolume.reparentTo(self.frameGeneral)
        self.lblVolumeMute.reparentTo(self.frameGeneral)
        self.cbVolumeMute.reparentTo(self.frameGeneral)

        self.frameGeneral.reparentTo(self.frameMain)

        self.accept("LanguageChanged", self.setText)

    def initControlTab(self):
        """
        This function will set up the content of the
        control tab
        """
        self.frameControl = DirectFrame(
            # size of the frame
            frameSize = (base.a2dLeft, base.a2dRight,
                         -0.6, 0.6),
            # position of the frame
            pos = (0, 0, 0),
            # tramsparent bg color
            frameColor = (0, 0, 0, 0.5))

        numItemsVisible = 9
        itemHeight = 0.10

        # the list field for the keyboard maping to the actions
        self.controlsList = DirectScrolledList(
            decButton_pos= (0, 0, -0.05),
            decButton_text = _("up"),
            decButton_text_scale = 0.04,
            decButton_borderWidth = (0.005, 0.005),

            incButton_pos= (0, 0, -1.05),
            incButton_text = _("down"),
            incButton_text_scale = 0.04,
            incButton_borderWidth = (0.005, 0.005),

            frameSize = (-1, 1, -1.1, 0.0),
            frameColor = (0,0,0,0.5),
            pos = (0, 0, 0.6),
            numItemsVisible = numItemsVisible,
            forceHeight = itemHeight,
            itemFrame_frameSize = (-0.9, 0.9, -0.9, 0),
            itemFrame_pos = (0, 0, -0.1),
            )

        self.fillControlsList()

        self.controlsList.reparentTo(self.frameControl)
        self.frameControl.reparentTo(self.frameMain)

    def fillControlsList(self):
        for key, value in sorted(settings.playerKeys.items()):
            # the base frame of any item in the list
            itemFrame = DirectFrame(
                frameSize = (-0.9, 0.9, -0.09, 0),
                frameColor = (0, 1, 0, 0))

            def changeKey(key, value):
                # all possible keyboard keys to set for a specific action
                keyboard = [
                    "escape",
                    "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10",
                    "f11", "f12",

                    "print_screen", "scroll_lock", "pause", "num_lock",
                    "insert", "delete", "home", "end", "page_up", "page_down",

                    "tab", "caps_lock", "shift", "rcontrol", "lcontrol", "ralt",
                    "lalt", "space", "backspace", "enter",

                    "arrow_left", "arrow_up", "arrow_down", "arrow_right",

                    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
                    "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
                    "y", "z",

                    "ä", "ö", "ü",

                    ",", ";", ".", ":", "_", "-", "#", "'", "+", "*", "~", "'",
                    "`", "!", "\"", "§", "$", "%", "&", "/", "(", ")", "=", "?",
                    "{", "}", "[", "]", "\\", "^", "°"
                    ]

                def setKey(arg):
                    """
                    This function will set the chosen key for the given action
                    """
                    # ignore all keyboard inputs again
                    for keyboardKey in keyboard:
                        self.ignore(keyboardKey)
                    if arg == 1:
                        # if the dialog was closed with OK
                        # set the settings to the new value
                        settings.playerKeys[key][0] = self.selectedKey
                        if len(settings.playerKeys[key]) > 1:
                            # just set the run key value if it is possible
                            newKey = settings.playerKeys["run"][0] + "-" + self.selectedKey
                            settings.playerKeys[key][1] = newKey
                    # refresh the controls list
                    self.controlsList.removeAllItems()
                    self.fillControlsList()
                    # finaly close the dialog
                    self.keySelectDialog.hide()
                    self.keySelectDialog = None

                # this variable will store the selected key for the given action
                self.selectedKey = value[0]
                def setSelectedKey(selkey):
                    """
                    set the pressed key as the selected one and actualise the text
                    on the dialog
                    """
                    self.selectedKey = selkey
                    self.keySelectDialog["text"] = "{0}: {1}".format(key, self.selectedKey)

                # accept all keyboard keys
                for keyboardKey in keyboard:
                    self.accept(
                        keyboardKey,
                        setSelectedKey,
                        [keyboardKey])

                # set up a dialog wich will ask for the new key for the chosen action
                self.keySelectDialog = OkCancelDialog(
                    dialogName = "OkCancelDialog",
                    text = "{0}: {1}".format(key, value[0]),
                    fadeScreen = 1,
                    command = setKey
                    )
                # show the dialog
                self.keySelectDialog.show()

            # add the change button to change the key of the action
            itemBtnChange = DirectButton(
                text = _("change"),
                scale = 0.05,
                pos = (0.5, 0, -0.05),
                command = changeKey,
                extraArgs = [key, value]
                )
            itemBtnChange.reparentTo(itemFrame)
            # add the label wich will show the name and key of the action
            itemText = DirectLabel(
                text = "{0} - {1}".format(key, value[0]),
                text_scale = 0.06,
                text_align = TextNode.ALeft,
                pos = (-0.88, 0, -0.06))
            itemText.reparentTo(itemFrame)

            # finaly add the item to the list
            self.controlsList.addItem(itemFrame)


    def show(self):
        self.setText()
        self.showBase()

    def showGeneralTab(self):
        # set the selected language in the textbox
        if settings.selectedLanguage == "de-DE":
            self.cmbLanguage.set(0, False)
        elif settings.selectedLanguage == "ru-RU":
            self.cmbLanguage.set(2, False)
        elif settings.selectedLanguage == "fr-FR":
            self.cmbLanguage.set(3, False)
        else:
            self.cmbLanguage.set(1, False)


        res = str(settings.windowSize[0]) + "x" + str(settings.windowSize[1])
        i = 0
        for item in self.cmbResolution["items"]:
            if item == res:
                self.cmbResolution.set(i, False)
            i += 1

        self.sliderGraphicQuality["value"] = settings.graphicquality

        self.sliderVolume["value"] = settings.volume

        #self.cbVolumeMute["indicatorValue"] = settings.muted
        self.cbVolumeMute["isChecked"] = not settings.muted
        self.cbVolumeMute.commandFunc(None)
        #self.cbVolumeMute.setIndicatorValue()

        self.frameGeneral.show()
        self.hideControlTab()

    def showControlTab(self):
        self.frameControl.show()
        self.hideGeneralTab()

    def hide(self):
        self.hideBase()

    def hideGeneralTab(self):
        self.frameGeneral.hide()

    def hideControlTab(self):
        self.frameControl.hide()

    def setText(self):
        self.title["text"] = _("Options")
        self.btnBack["text"] = _("Back")
        self.lblLanguage["text"] = _("Language")
        self.lblResolution["text"] = _("Screen resolution")
        self.lblGraphicQuality["text"] = _("Graphic quality")
        self.graphicqualityTextMap = {
            0:_("Low"),
            1:_("Medium"),
            2:_("High")}
        self.sliderGraphicQuality["text"] = self.graphicqualityTextMap[
            settings.graphicquality]
        self.lblVolume["text"] = _("Volume")
        self.lblVolumeMute["text"] = _("Mute")


    def cmbLanguage_SelectionChanged(self, arg):
        # TODO: get available languages and maping from language class!
        if arg == "Deutsch":
            lng.changeLanguage("de-DE")
            settings.selectedLanguage = "de-DE"
        elif arg == "русский":
            lng.changeLanguage("ru-RU")
            settings.selectedLanguage = "ru-RU"
        elif arg == "français":
            lng.changeLanguage("fr-FR")
            settings.selectedLanguage = "fr-FR"
        else:
            lng.changeLanguage("en-US")
            settings.selectedLanguage = "en-US"

    def cmbResolution_SelectionChanged(self, arg):
        resx = int(arg.split("x")[0])
        resy = int(arg.split("x")[1])
        settings.windowSize = [resx, resy]
        camMgr.setCamAspectRatio(float(resx)/float(resy))

    def sliderGraphicQuality_ValueChanged(self):
        val = int(round(self.sliderGraphicQuality["value"], 0))
        self.sliderGraphicQuality["text"] = self.graphicqualityTextMap[val]
        if val != settings.graphicquality:
            settings.graphicquality = val
            graphicMgr.setGraphicQuality(settings.graphicquality)

    def sliderVolume_ValueChanged(self):
        val = round(self.sliderVolume["value"], 2)
        self.sliderVolume["text"] = str(int(val * 100)) + "%"
        settings.volume = val
        audioMgr.setVolume(settings.volume)

    def cbVolumeMute_CheckedChanged(self, checked):
        self.cbVolumeMute["image_scale"] = 0.35
        self.cbVolumeMute["image_pos"] = (0.05,0,0.25)
        settings.muted = bool(checked)
        audioMgr.mute(settings.muted)

    def btnBack_Click(self):
        base.messenger.send("OptMenu_back")
