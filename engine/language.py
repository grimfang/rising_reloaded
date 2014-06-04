#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Documentation: main.py
  Classes and functions:
    Language
  Description:
    This module provides and initialise the functions to
    internationalise (I18N) and localise (L10N) the application
"""

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

import gettext



class Language:
    def __init__(self, settings):
        #self.path = settings.tmpPath.getFullpath() + "/lng/"
        self.path = "game/assets/lng/"

    def setup(self, settings):
        """Initialise the possible languages of the application"""
        self.lang_de_DE = gettext.translation(
            appName, localedir=self.path, languages=["de_DE"], fallback=True)
        self.lang_en_US = gettext.translation(
            appName, localedir=self.path, languages=["en_US"], fallback=True)
        self.lang_ru_RU = gettext.translation(
            appName, localedir=self.path, languages=["ru_RU"], fallback=True)
        self.lang_fr_FR = gettext.translation(
            appName, localedir=self.path, languages=["fr_FR"], fallback=True)

        if settings.selectedLanguage == "de-DE" and self.lang_de_DE:
            # try to setup the german language
            self.lang_de_DE.install()
        elif settings.selectedLanguage == "ru-RU" and self.lang_ru_RU:
            # try to setup the russian language
            self.lang_ru_RU.install()
        elif settings.selectedLanguage == "fr-FR" and self.lang_fr_FR:
            self.lang_fr_FR.install()
        else:
            # if we don't want or can't use one of the above translations
            # we are going to use the english translation as default.
            # If that fails, the app should die with an exception!
            self.lang_en_US.install()

    def addTranslationFile(self, domain, path_en_EN,
                           path_de_DE=None, path_ru_RU=None, path_fr_FR=None):
        """Adds the given translation files as fallback for the
        general translation files. If the path to a language is None,
        then the path to the english fallback translation file will
        be used as a fallback. At least a path to an english translation
        has to be given."""
        fb_en = gettext.translation(
            domain, localedir=path_en_EN, languages=["en_US"], fallback=True)
        if path_de_DE != None:
            fb_de = gettext.translation(
                domain, localedir=path_de_DE, languages=["de_DE"], fallback=True)
        else:
            fb_de = gettext.translation(
                domain, localedir=path_en_EN, languages=["en_US"], fallback=True)

        if path_ru_RU != None:
            fb_ru = gettext.translation(
                domain, localedir=path_ru_RU, languages=["ru_RU"], fallback=True)
        else:
            fb_ru = gettext.translation(
                domain, localedir=path_en_EN, languages=["en_US"], fallback=True)

        if path_fr_FR != None:
            fb_fr = gettext.translation(
                domain, localedir=path_fr_FR, languages=["fr_FR"], fallback=True)
        else:
            fb_fr = gettext.translation(
                domain, localedir=path_en_EN, languages=["en_US"], fallback=True)

        self.lang_de_DE.add_fallback(fb_de)
        self.lang_en_US.add_fallback(fb_en)
        self.lang_ru_RU.add_fallback(fb_ru)
        self.lang_fr_FR.add_fallback(fb_fr)

    def changeLanguage(self, lng):
        """change the application language to the given
        language
        accepted languages:
        en-US (default if lng was not found),
        ru-RU
        de-DE
        fr-FR"""
        if lng == "de-DE":
            if self.lang_de_DE:
                self.lang_de_DE.install()
        elif lng == "ru-RU":
            if self.lang_ru_RU:
                self.lang_ru_RU.install()
        elif lng == "fr-FR":
            if self.lang_fr_FR:
                self.lang_fr_FR.install()
        else:
            if self.lang_en_US:
                self.lang_en_US.install()
        base.messenger.send("LanguageChanged")
