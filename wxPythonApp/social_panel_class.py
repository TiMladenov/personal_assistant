import wx
from social_panel_m_facebook import FB_panel
from social_panel_m_twitter import Twitter_panel

class SocialPanel( wx.Panel ):
    """
    This class extends the wx.Panel class and serves as the parent class to all social media modules / classes
    ...
    Attributes:
    btn_facebook : wx.Button
        This button displays Facebook's panel.
        Calls on method OnSocialButton(self, event)
    btn_twitter : wx.Button
        This button displays Twitters's panel.
        Calls on method OnSocialButton(self, event)
    FB_panel : wx.Panel
        This is the panel for Facebook
    Twitter_panel : wx.Panel
        This is the panel for Twitter
    ...
    Methods:
    FB_panel(self, event)
        Hides all social media panels, but the one selected by the user
    """
    def __init__(self, parent):
        super(SocialPanel, self).__init__(parent = parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL)

        ############################## STATIC UI ##############################
        social_panel_sizer = wx.BoxSizer( wx.VERTICAL )

        self.social_options = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
        social_options_sizer = wx.BoxSizer( wx.HORIZONTAL )

        self.btn_facebook = wx.BitmapButton( self.social_options, wx.ID_ANY, wx.Bitmap( u"img/fb_logo.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.Bind(wx.EVT_BUTTON, self.OnSocialButton, self.btn_facebook)
        self.btn_facebook.SetMaxSize( wx.Size( 35,35 ) )
        social_options_sizer.Add( self.btn_facebook, 0, wx.ALL, 5 )

        self.btn_twitter = wx.BitmapButton( self.social_options, wx.ID_ANY, wx.Bitmap( u"img/twitter_logo.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.Bind(wx.EVT_BUTTON, self.OnSocialButton, self.btn_twitter)
        self.btn_twitter.SetMaxSize( wx.Size( 35,35 ) )
        social_options_sizer.Add( self.btn_twitter, 0, wx.ALL, 5 )

        self.social_options.SetSizer( social_options_sizer )
        self.social_options.Layout()
        social_options_sizer.Fit( self.social_options )
        social_panel_sizer.Add( self.social_options, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticline43 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        social_panel_sizer.Add( self.m_staticline43, 0, wx.EXPAND |wx.ALL, 0 )

        self.FB_Panel = FB_panel(self)
        social_panel_sizer.Add( self.FB_Panel, 1, wx.EXPAND |wx.ALL, 5 )

        self.Twitter_Panel = Twitter_panel(self)
        self.Twitter_Panel.Hide()
        social_panel_sizer.Add( self.Twitter_Panel, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer( social_panel_sizer )
        self.Layout()
        social_panel_sizer.Fit( self )
        ############################## STATIC UI ##############################

    def OnSocialButton(self, event):
        """Hides all social media panels, but the one selected by the user"""
        btn = event.EventObject

        if btn is self.btn_facebook:
            self.FB_Panel.Show()
            self.Twitter_Panel.Hide()
            self.Layout()
        elif btn is self.btn_twitter:
            self.FB_Panel.Hide()
            self.Twitter_Panel.Show()
            self.Layout()
