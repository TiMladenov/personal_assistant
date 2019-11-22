import wx
import wx.xrc
import threading
import urllib.request as urllib2
from io import BytesIO
from TTS_Reader import TextToSpeech

class ReadNewsFrame(wx.Frame):
    """
    This class extends wx.Frame, meaning it won't be a part of the main app frame, and
    is used by News (API) Panel to display a whole article with the resources that are provided to it
    ...
    Attributes:
    img : wx.Image
        The image in the article to be displayed
    text : str
        The complete main content text of the article
    tts : TextToSpeech
        References an instance of TextToSpeech for a Text-to-Speech reader
    _read_news_img_src : str
        URL to the news article image
    _read_news_title : str
        Title to the news article
    _read_news_source : str
        Source / provider of the news article
    _read_news_published_on : str
        Date of publishing of the article
    ReadNewsButtonToggleReader : wx.Button
        This button is clicked when there's need for a T-T-S
        to be created. It calls on method OnToggleBtnPress(self, event)
    ...
    Methods:
        OnToggleBtnPress(self, event)
            Creates an instance of TextToSpeech and provides it with the
            text of the article, then plays the TTS
        OnClose(self, event)
            Tries to destroy the tts object if it's running, closes and
            destroys the ReadNewsFrame
    """
    
    def __init__(self, parent, _read_news_img_src, _read_news_text, _read_news_title, _read_news_source, _read_news_published_on):
        super(ReadNewsFrame, self).__init__(parent = parent, id = wx.ID_ANY, title = u"Read News", pos = wx.DefaultPosition, size = wx.Size(900, 700), style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER | wx.TAB_TRAVERSAL)

        self.img = None
        self.text = _read_news_text
        self.tts = None

        ################################ STATIC UI ################################
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        ReadNewsRootWindow = wx.BoxSizer(wx.VERTICAL)

        self.ReadNewsImagePanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 300), wx.TAB_TRAVERSAL)
        ReadNewsImageSizer = wx.BoxSizer(wx.VERTICAL)

        try:
            """Tries to open the URL of the article image, download the image, parse it to wx.Image"""
            file_url = urllib2.urlopen(_read_news_img_src).read()
            stream = BytesIO(file_url)
            self.img = wx.Image(stream)
        except:
            wx.MessageBox(message = 'There was an error while processing the image loading call.', caption = 'Error. Could not load the news.', parent = self)

        ReadNewsImageSizer.SetMinSize(wx.Size(-1, 300))
        self.ReadNewsImage = wx.StaticBitmap(self.ReadNewsImagePanel, wx.ID_ANY, wx.Bitmap(r"img/placeholder300x202.jpg", wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.Size(600, 290), 0)
        if self.img != None:
            self.ReadNewsImage.SetBitmap(wx.Bitmap(self.img))
        ReadNewsImageSizer.Add(self.ReadNewsImage, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.ReadNewsImagePanel.SetSizer(ReadNewsImageSizer)
        self.ReadNewsImagePanel.Layout()
        ReadNewsRootWindow.Add(self.ReadNewsImagePanel, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticline23 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        ReadNewsRootWindow.Add(self.m_staticline23, 0, wx.EXPAND | wx.ALL, 5)

        ReadNewsTextWindow = wx.BoxSizer(wx.VERTICAL)

        ReadNewsTextWindow.SetMinSize(wx.Size(-1, 400))
        ReadNewsProperties = wx.BoxSizer(wx.HORIZONTAL)

        self.static_news_title = wx.StaticText(self, wx.ID_ANY, u"Title:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_news_title.Wrap(-1)
        ReadNewsProperties.Add(self.static_news_title, 0, wx.ALL, 5)

        self.read_news_title_text = wx.StaticText(self, wx.ID_ANY, _read_news_title, wx.DefaultPosition, wx.Size(300, -1), 0)
        self.read_news_title_text.Wrap(300)
        ReadNewsProperties.Add(self.read_news_title_text, 0, wx.ALL, 5)

        self.static_news_author = wx.StaticText(self, wx.ID_ANY, u"Source:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_news_author.Wrap(-1)
        ReadNewsProperties.Add(self.static_news_author, 0, wx.ALL, 5)

        self.read_news_source = wx.StaticText(self, wx.ID_ANY, _read_news_source, wx.DefaultPosition, wx.Size(150, -1), 0)
        self.read_news_source.Wrap(-1)
        ReadNewsProperties.Add(self.read_news_source, 0, wx.ALL, 5)

        self.static_news_date = wx.StaticText(self, wx.ID_ANY, u"Published on:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_news_date.Wrap(-1)
        ReadNewsProperties.Add(self.static_news_date, 0, wx.ALL, 5)

        self.read_news_publish_date = wx.StaticText(self, wx.ID_ANY, _read_news_published_on, wx.DefaultPosition, wx.DefaultSize, 0)
        self.read_news_publish_date.Wrap(-1)
        ReadNewsProperties.Add(self.read_news_publish_date, 0, wx.ALL, 5)

        ReadNewsTextWindow.Add(ReadNewsProperties, 0, wx.EXPAND, 5)

        self.m_staticline17 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        ReadNewsTextWindow.Add(self.m_staticline17, 0, wx.EXPAND | wx.ALL, 5)

        self.ReadNewsTextScrollWindow = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 400), wx.HSCROLL | wx.VSCROLL)
        self.ReadNewsTextScrollWindow.SetScrollRate(5, 5)
        ReadNewsTextSizer = wx.BoxSizer(wx.VERTICAL)

        ReadNewsTextSizer.SetMinSize(wx.Size(-1, 400))
        self.read_news_main_content = wx.StaticText(self.ReadNewsTextScrollWindow, wx.ID_ANY, _read_news_text, wx.DefaultPosition, wx.Size(875, -1), 0)
        self.read_news_main_content.Wrap(875)
        ReadNewsTextSizer.Add(self.read_news_main_content, 1, wx.ALL, 5)

        self.ReadNewsTextScrollWindow.SetSizer(ReadNewsTextSizer)
        self.ReadNewsTextScrollWindow.Layout()
        ReadNewsTextWindow.Add(self.ReadNewsTextScrollWindow, 1, wx.EXPAND | wx.ALL, 5)

        self.m_staticline21 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        ReadNewsTextWindow.Add(self.m_staticline21, 0, wx.EXPAND | wx.ALL, 5)

        ReadNewsTextWindowButtons = wx.BoxSizer(wx.HORIZONTAL)

        self.ReadNewsButtonToggleReader = wx.Button(self, wx.ID_ANY, u"TTS Reader", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, self.OnToggleBtnPress, self.ReadNewsButtonToggleReader)
        ReadNewsTextWindowButtons.Add(self.ReadNewsButtonToggleReader, 0, wx.ALL, 5)
        ReadNewsTextWindow.Add(ReadNewsTextWindowButtons, 0, wx.EXPAND, 5)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.m_staticline22 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        ReadNewsTextWindow.Add(self.m_staticline22, 0, wx.EXPAND | wx.ALL, 5)
        ReadNewsRootWindow.Add(ReadNewsTextWindow, 0, wx.EXPAND, 5)

        self.SetSizer(ReadNewsRootWindow)
        self.Layout()
        ################################ STATIC UI ################################

        self.Show()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass

    def OnToggleBtnPress(self, event):
        """
        Creates an instance of TextToSpeech and provides it with the
        text of the article, then plays the TTS
        """
        self.tts = TextToSpeech(self, self.text)
        self.tts.Play()

    def OnClose(self, event):
        """
        Tries to destroy the tts object if it's running, closes and
        destroys the ReadNewsFrame
        """
        try:
            self.tts.Stop()
            del self.tts
        except:
            pass
        self.Destroy()