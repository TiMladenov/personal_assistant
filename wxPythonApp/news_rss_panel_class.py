import wx
import socket
import feedparser
import wx.lib.agw.hyperlink as hl
class UrlDialog(wx.Dialog):
    """
    A simple class that extends the wx.Dialog class. Its job is to display a hyperlinked URL to an article
    in a pop-up, which the user can then click on to open in their browser
    """
    def __init__(self, parent, link):
        super(UrlDialog, self).__init__(parent = parent, title = "Visit website", size = wx.Size(900, 100))
        self.SetMaxSize(wx.Size(900, 100))

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        hyperlink = hl.HyperLinkCtrl(self, -1, label = link, pos = wx.DefaultPosition, URL = link)
        sizer.SetMinSize(-1, -1)
        sizer.Add(hyperlink, 0, wx.ALL, 5)
        self.SetSizer(sizer)

        self.Show()

class NewsRss(wx.Panel):
    def __init__(self, parent):
        """
        The class inherits from wx.Panel and is customized to display news articles fetched from various RSS news providers
        that the user can chose from
        ...
        Attributes:
        rss_urls : list
            Stores the URLs [str] from currently loaded articles
        parent : wx.Window
            Reference to the parent window
        ind : int
            The index/count of all currently loaded articles
        rss_provider_comboChoices : list
            List with the names of the currently supported RSS news providers
        ...
        Methods:
        OnRssProvider(self, event)
            Gets the name of the selected RSS provider. If there's internet connection
            it checks if the UI needs to be cleared from old results, then calls on
            PopulateUI(provider) to fetch the RSS news
        PopulateUI(self, _provider)
            Makes a call depending on the selected RSS provider. Stores the fetched information in
            rssFeed and loops through it, filling the respective position in the list item.
            When finished, appends the list item to the list with all other list items.
            ...
            Attribute:
            rssFeed : list
            provider : str
        OnButtonClick(self, event)
            When the user clicks on a button in a list item, the URL for this item is fetched
            and an instance of UrlDialog is started where it is sent. The user can then access the link
            to read the article.
            ...
            Attribute:
            url_dialog : UrlDialog
        HasInternet(self)
            Checks if there's internet connection
            return True - there's internet
            return False - there's no internet
        """
        super(NewsRss, self).__init__(parent = parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.TAB_TRAVERSAL)

        self.rss_urls = []
        self.parent = parent
        self.ind = 0

        ##################################### STATIC UI #####################################

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        NewsRssPanelSizer = wx.BoxSizer(wx.VERTICAL)

        RssProviderSizer = wx.BoxSizer(wx.HORIZONTAL)

        m_static_provider = wx.StaticText(self, wx.ID_ANY, u"Select RSS provider:", wx.DefaultPosition, wx.Size(-1, -1), 0)
        RssProviderSizer.Add(m_static_provider, 0, wx.ALL | wx.CENTER, 5)

        rss_provider_comboChoices = [u"The Guardian", u"The Economist", u"Times Of India"]
        self.rss_provider_combo = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, rss_provider_comboChoices, 0)
        self.rss_provider_combo.Bind(wx.EVT_CHOICE, self.OnRssProvider)
        RssProviderSizer.Add(self.rss_provider_combo, 0, wx.ALL, 5)

        self.m_staticline120 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        RssProviderSizer.Add(self.m_staticline120, 0, wx.EXPAND | wx.ALL, 5)
        NewsRssPanelSizer.Add(RssProviderSizer, 0, wx.EXPAND, 5)

        NewsRssPanelProperties = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText_id = wx.StaticText(self, wx.ID_ANY, u"ID:", wx.DefaultPosition, wx.Size(30, -1), 0)
        self.m_staticText_id.Wrap(-1)
        NewsRssPanelProperties.Add(self.m_staticText_id, 0, wx.ALL, 5)

        self.m_staticline20 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        NewsRssPanelProperties.Add(self.m_staticline20, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticText_title = wx.StaticText(self, wx.ID_ANY, u"Title:", wx.DefaultPosition, wx.Size(300, -1), 0)
        self.m_staticText_title.Wrap(-1)
        NewsRssPanelProperties.Add(self.m_staticText_title, 0, wx.ALL, 5)

        self.m_staticline21 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        NewsRssPanelProperties.Add(self.m_staticline21, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticText_published = wx.StaticText(self, wx.ID_ANY, u"Published on:", wx.DefaultPosition, wx.Size(200, -1), 0)
        self.m_staticText_published.Wrap(-1)
        NewsRssPanelProperties.Add(self.m_staticText_published, 0, wx.ALL, 5)

        self.m_staticline22 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        NewsRssPanelProperties.Add(self.m_staticline22, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticText_author = wx.StaticText(self, wx.ID_ANY, u"Author:", wx.DefaultPosition, wx.Size(200, -1), 0)
        self.m_staticText_author.Wrap(-1)
        NewsRssPanelProperties.Add(self.m_staticText_author, 0, wx.ALL, 5)

        self.m_staticline23 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        NewsRssPanelProperties.Add(self.m_staticline23, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticText_browser = wx.StaticText(self, wx.ID_ANY, u"Open in browser:", wx.DefaultPosition, wx.Size(160, -1), 0)
        self.m_staticText_browser.Wrap(-1)
        NewsRssPanelProperties.Add(self.m_staticText_browser, 0, wx.ALL, 5)

        NewsRssPanelSizer.Add(NewsRssPanelProperties, 0, wx.EXPAND, 5)

        self.NewsRssPanelContainer = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.VSCROLL)
        self.NewsRssPanelContainer.SetScrollRate(5, 5)

        self.RssPanelList = wx.BoxSizer(wx.VERTICAL)

        self.NewsRssPanelContainer.SetSizer(self.RssPanelList)
        self.NewsRssPanelContainer.Layout()
        self.RssPanelList.Fit(self.NewsRssPanelContainer)
        NewsRssPanelSizer.Add(self.NewsRssPanelContainer, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(NewsRssPanelSizer)
        self.Layout()
        NewsRssPanelSizer.Fit(self)
        ##################################### STATIC UI #####################################

    def OnRssProvider(self, event):
        """
        Gets the name of the selected RSS provider. If there's internet connection
        it checks if the UI needs to be cleared from old results, then calls on
        PopulateUI(provider) to fetch the RSS news
        """
        provider = event.GetString()
        if self.HasInternet():
            
            if self.RssPanelList.GetItemCount() > 0:
                self.RssPanelList.Clear(delete_windows = True)

                if len(self.rss_urls) > 0:
                    self.rss_urls.clear()
                    
                self.PopulateUI(provider)
            else:
                if len(self.rss_urls) > 0:
                    self.rss_urls.clear()
                    
                self.PopulateUI(provider)
        else:
            wx.MessageBox("Uups, there's no internet connection.", caption="Error. No Internet connection")

    def PopulateUI(self, _provider):
        """
        Makes a call depending on the selected RSS provider. Stores the fetched information in
        rssFeed and loops through it, filling the respective position in the list item.
        When finished, appends the list item to the list with all other list items.
        ...
        Attribute:
        rssFeed : list
        provider : str
        """
        rssFeed = ""
        self.ind = 0

        if _provider == "The Guardian":
            rssFeed = feedparser.parse("https://www.theguardian.com/world/eu/rss").entries
        elif _provider == "The Economist":
            rssFeed = feedparser.parse("https://www.economist.com/europe/rss.xml").entries
        elif _provider == "Times Of India":
            rssFeed = feedparser.parse("https://timesofindia.indiatimes.com/rssfeedstopstories.cms").entries

        for i in rssFeed:

            self.rss_urls.append(i["link"])

            self.ind = self.ind + 1

            self.RssPanelListItem = wx.Panel(self.NewsRssPanelContainer, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
            self.ListItemSizer = wx.BoxSizer(wx.HORIZONTAL)

            self.ListItemSizer.SetMinSize(wx.Size(-1, 50))
            self.rss_id = wx.StaticText(self.RssPanelListItem, wx.ID_ANY, str(self.ind), wx.DefaultPosition, wx.Size(25, -1), 0)
            self.rss_id.Wrap(-1)

            self.ListItemSizer.Add(self.rss_id, 0, wx.ALIGN_CENTER | wx.ALL, 5)

            self.m_staticline26 = wx.StaticLine(self.RssPanelListItem, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
            self.ListItemSizer.Add(self.m_staticline26, 0, wx.EXPAND | wx.ALL, 5)

            self.m_scrolledWindow5 = wx.ScrolledWindow(self.RssPanelListItem, wx.ID_ANY, wx.DefaultPosition, wx.Size(300, -1), wx.HSCROLL)
            self.m_scrolledWindow5.SetScrollRate(5, 5)
            self.m_scrolledWindow5.SetMaxSize(wx.Size(300, -1))

            TitleSizer = wx.BoxSizer(wx.HORIZONTAL)

            self.m_staticText40 = wx.StaticText(self.m_scrolledWindow5, wx.ID_ANY, i["title"], wx.DefaultPosition, wx.Size(-1, -1), 0)
            self.m_staticText40.Wrap(-1)

            TitleSizer.Add(self.m_staticText40, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)

            self.m_scrolledWindow5.SetSizer(TitleSizer)
            self.m_scrolledWindow5.Layout()
            self.ListItemSizer.Add(self.m_scrolledWindow5, 0, wx.EXPAND | wx.ALL, 5)

            self.m_staticline28 = wx.StaticLine(self.RssPanelListItem, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
            self.ListItemSizer.Add(self.m_staticline28, 0, wx.EXPAND | wx.ALL, 5)

            self.rss_publish_date = wx.StaticText(self.RssPanelListItem, wx.ID_ANY, i["published"], wx.DefaultPosition, wx.Size(200, -1), 0)
            self.rss_publish_date.Wrap(-1)

            self.ListItemSizer.Add(self.rss_publish_date, 0, wx.ALIGN_CENTER | wx.ALL, 5)

            self.m_staticline29 = wx.StaticLine(self.RssPanelListItem, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
            self.ListItemSizer.Add(self.m_staticline29, 0, wx.EXPAND | wx.ALL, 5)

            self.rss_author = wx.StaticText(self.RssPanelListItem, wx.ID_ANY, u"N/A", wx.DefaultPosition, wx.Size(200, -1), 0)
            if _provider == "The Guardian" and i["author"] != "":
                self.rss_author.SetLabel(i["author"])
            self.rss_author.Wrap(-1)

            self.ListItemSizer.Add(self.rss_author, 0, wx.ALIGN_CENTER | wx.ALL, 5)

            self.m_staticline30 = wx.StaticLine(self.RssPanelListItem, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
            self.ListItemSizer.Add(self.m_staticline30, 0, wx.EXPAND | wx.ALL, 5)

            self.rss_button = wx.Button(self.RssPanelListItem, wx.ID_ANY, u"Open {0}".format(self.ind), wx.DefaultPosition, wx.DefaultSize, 0)
            self.rss_button.Bind(wx.EVT_BUTTON, self.OnButtonClick)

            self.ListItemSizer.Add(self.rss_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)

            self.RssPanelListItem.SetSizer(self.ListItemSizer)
            self.RssPanelListItem.Layout()
            self.ListItemSizer.Fit(self.RssPanelListItem)
            self.RssPanelList.Add(self.RssPanelListItem, 0, wx.EXPAND | wx.ALL, 5)
            self.RssPanelList.Layout()
        self.Layout()

    def OnButtonClick(self, event):
        """
        When the user clicks on a button in a list item, the URL for this item is fetched
        and an instance of UrlDialog is started where it is sent. The user can then access the link
        to read the article.
        ...
        Attribute:
        url_dialog : UrlDialog
        """
        btn_number = int(event.EventObject.GetLabel().split(" ")[1]) - 1
        link = self.rss_urls[btn_number]

        url_dialog = UrlDialog(self, link)

    def HasInternet(self):
        """
        Checks if there's internet connection
        return True - there's internet
        return False - there's no internet
        """
        try:
            socket.create_connection(("www.abv.bg", 80))
            return True
        except OSError:
            return False
