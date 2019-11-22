import wx

class About( wx.Frame ):
    def __init__(self, parent):
        """
        A wx.Frame class used to store the About information for the application
        ...

        Attributes:
        parent : wx.Frame
            The parent object that we inherit from and create out own frame
        about_sizer : wx.BoxSizer
            The main sizer to align the content vertically
        about_panel : wx.Panel
            Main parent panel for the content
        about_content_sizer : wx.BoxSizer
            Vertical sizer used to store the information in the about_panel
        m_static_software : wx.StaticText
            Contains a static -Software- string
        m_var_product_name : wx.StaticText
            Contains a the product name -Personal Assistant - string
        m_static_version: wx.StaticText
            Contains a static -Version- string
        m_var_version_num: wx.StaticText
            Contains the version and release date of the app
        m_static_creator : wx.StaticText
            Stores tha label for the creator and rights owner
        var_creator_data : wx.StaticText
            Stores the names of the creator
        var_url : wx.adv.HyperLinkCtrl
            stores URL to creator's website
        var_email : wx.adv.HyperLinkCtrl
            Stores the email address of the creator
        ...
        Methods:
        OnClose(self, event)
            Hides the window when the Close button is pressed
        """

        super(About, self).__init__ ( parent = parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 300,400 ), style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER |wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        about_sizer = wx.BoxSizer( wx.VERTICAL )

        self.about_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        about_content_sizer = wx.BoxSizer( wx.VERTICAL )

        self.m_static_software = wx.StaticText( self.about_panel, wx.ID_ANY, u"Software:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_software.Wrap( -1 )
        self.m_static_software.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        about_content_sizer.Add( self.m_static_software, 0, wx.ALL, 5 )

        self.var_product_name = wx.StaticText( self.about_panel, wx.ID_ANY, u"Personal Assistant", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.var_product_name.Wrap( -1 )
        about_content_sizer.Add( self.var_product_name, 0, wx.ALL, 5 )

        self.m_static_version = wx.StaticText( self.about_panel, wx.ID_ANY, u"Version:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_version.Wrap( -1 )
        self.m_static_version.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        about_content_sizer.Add( self.m_static_version, 0, wx.ALL, 5 )

        self.var_version_num = wx.StaticText( self.about_panel, wx.ID_ANY, u"v 1.0\nJuly 2019", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.var_version_num.Wrap( -1 )
        about_content_sizer.Add( self.var_version_num, 0, wx.ALL, 5 )

        self.m_static_creator = wx.StaticText( self.about_panel, wx.ID_ANY, u"Creator and rights owner:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_creator.Wrap( -1 )
        self.m_static_creator.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        about_content_sizer.Add( self.m_static_creator, 0, wx.ALL, 5 )

        self.var_creator_data = wx.StaticText( self.about_panel, wx.ID_ANY, u"Tihomir Mladenov", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.var_creator_data.Wrap( -1 )
        about_content_sizer.Add( self.var_creator_data, 0, wx.ALL, 5 )

        self.var_url = wx.adv.HyperlinkCtrl( self.about_panel, wx.ID_ANY, u"https://www.tmladenov.tech/", r"https://www.tmladenov.tech/", wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE )
        about_content_sizer.Add( self.var_url, 0, wx.ALL, 5 )

        self.var_inquiries = wx.StaticText( self.about_panel, wx.ID_ANY, u"For any inquiries, please contact me at:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.var_inquiries.Wrap( -1 )
        self.var_inquiries.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        about_content_sizer.Add( self.var_inquiries, 0, wx.ALL, 5 )

        self.var_email = wx.adv.HyperlinkCtrl( self.about_panel, wx.ID_ANY, u"tihomir.mladenov777@gmail.com", r"tihomir.mladenov777@gmail.com", wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE )
        about_content_sizer.Add( self.var_email, 0, wx.ALL, 5 )

        self.about_panel.SetSizer( about_content_sizer )
        self.about_panel.Layout()
        about_content_sizer.Fit( self.about_panel )
        about_sizer.Add( self.about_panel, 1, wx.EXPAND |wx.ALL, 5 )

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.SetSizer( about_sizer )
        self.Layout()

        self.Centre( wx.BOTH )

    def OnClose(self, event):
        """Hides the window when the Close button is closed"""
        self.Hide()

    def __del__(self):
        """Deletes the instance when last reference is removed"""
        del self
