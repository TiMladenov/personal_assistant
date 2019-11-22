# -*- coding: utf-8 -*-

import re
import pyttsx3 as pyttsx
import wx

class TextToSpeech(object):
    """
    A class to create Text-to-Speech for main modules in the app
    ...
    Attributes:
    parent : wx.Window
        The parent window that instantiated this class
    str : str
        The text that is to be read by the TTS. It must pass a REGEX
        cleanup before running, because special symbols crash the TTS
    ...
    Methods:
    Play(self)
        Initiates the TTS engine, sets its rate and passes the text to it
    Stop(self)
        Stops the TTS. Deletes its reference.
        [If not done, TTS won't run properly next time its used]
    """
    def __init__(self, _parent, _text):
        self.parent = _parent
        self.str = _text

        self.str = re.sub(r'[^A-Za-z0-9,.!?£]', ' ', self.str)
        self.str = self.str.replace('£', ' british pounds ')
        self.str = self.str.replace('$', ' US dollars ')
        self.str = self.str.replace('€', ' euros ')

    def Play(self):
        """Initiates the TTS engine, sets its rate and passes the text to it"""
        self.engine = pyttsx.init()
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate-25)
        #self.engine.connect('started-utterance', self.ReadStart)
        #self.engine.connect('finished-utterance', self.ReadFinish)
        self.engine.say(self.str)
        
        try:
            self.engine.runAndWait()
        except:
            wx.MessageBox(message = 'The TTS engine is already running', caption = 'Warning', parent = self.parent)

    #def ReadStart(self, name):
    #    self.parent.ReadNewsButtonToggleReader.Disable(True)
    #def ReadFinish(self, name, completed):
    #    self.parent.ReadNewsButtonToggleReader.Enable(True)

    def Stop(self):
        """
        Stops the TTS. Deletes its reference.
        [If not done, TTS won't run properly next time its used]
        """
        self.engine.stop()
        del self

    def __del__(self):
        del self