import wx
import wx.adv
from NewsApiCall import ReadNews
from ReadNewsFrame import ReadNewsFrame
import time
from wx.adv import EVT_DATE_CHANGED
import socket

class NewsPanel( wx.Panel ):
    """
    This class is used to fetch data from the RESTful service of the Guardian and visualize it
    ...
    Attributes:
    from_date : str
        Starting date to select news
    to_date : str
        End date to select news
    news_provider : str
        The news provider selected by the user
    query_txt : str
        The query entered by the user in the SearchCtrl box
    read_news_frame_title : str
        The title of a news article
    read_news_frame_source : str
        The source of a news article
    read_news_frame_published_on : str
        The publish date of a news article
    read_news_frame_img_src : str
        The URL of the image in the article
    read_news_frame_text : str
        The main text content of the article
    get_data_title : list
        Stores all article titles
    get_data_published_on : list
        Stores all article publish dates
    get_data_img : list
        Stores all article images
    get_data_text : list
        Stores the main content text of all articles
    news_rows : int
        Keeps track of the number of articles in the result
    ...
    Methods:
    OnDateFrom(self, event)
        Updates the from_date
    OnDateTo(self, event)
        Updates the to_date
    OnChoice(self, event)
        Updates the news_provider with the one being selected
    OnSearch(self, event)
        Makes a request to the news provider API with the request settings
        provided by the user.
        Displays an error if no news were fetched.
        If there is a result, the UI is cleared [if needed], the result is sent to
        FetchFields(self, data)
    FetchFields(self, data : JSON)
        Fetches the data from the JSON and fills it in the corresponding list.
        Calls LoadDataToUI(self, news_rows) when finished
    LoadDataToUI(self, news_rows)
        Goes through all the lists and fills the information from each list
        to the corresponding location in the news list item. Then adds the 
        news list item to the news list
    OnReadButtonClick(self, event):
        When the user clicks on an article button to read the article,
        all the information about it is selected and sent to a ReadNewsFrame object
        to be read
    HasInternet(self)
        Checks for an internet connection
        return : True - there's internet
        return : False - there's no internet

    """
    def __init__(self, parent):
        super(NewsPanel, self).__init__(parent = parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.TAB_TRAVERSAL)
        
        self.from_date = ""
        self.to_date = ""
        self.news_provider = ""
        self.query_txt = ""

        self.read_news_frame_title = ""
        self.read_news_frame_source = ""
        self.read_news_frame_published_on = ""
        self.read_news_frame_img_src = ""
        self.read_news_frame_text = ""
        
        self.get_data_title = []
        self.get_data_published_on = []
        self.get_data_img = []
        self.get_data_text = []
        self.news_rows = 0

        ##################################### STATIC UI ##################################### 
        self.NewsWindow = wx.BoxSizer(wx.VERTICAL)
        self.NewsWindow.SetMinSize(wx.Size(1920, 1080))

        NewsContainer1 = wx.BoxSizer(wx.VERTICAL)
        NewsContainer1.SetMinSize(wx.Size(1920, 1080))

        NewsWindowTools = wx.BoxSizer(wx.HORIZONTAL)
        self.m_datePicker1 = wx.adv.DatePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DROPDOWN)
        self.m_datePicker1.SetValue(wx.DateTime.Now())
        self.from_date = self.m_datePicker1.GetValue()
        self.from_date = self.from_date.FormatISODate()
        self.Bind(EVT_DATE_CHANGED, self.OnDateFrom, self.m_datePicker1)
        NewsWindowTools.Add(self.m_datePicker1, 0, wx.ALL, 5)

        self.m_datePicker2 = wx.adv.DatePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DROPDOWN)
        self.m_datePicker2.SetValue(wx.DateTime.Now())
        self.to_date = self.m_datePicker2.GetValue()
        self.to_date = self.to_date.FormatISODate()
        self.Bind(EVT_DATE_CHANGED, self.OnDateTo, self.m_datePicker2)
        NewsWindowTools.Add(self.m_datePicker2, 0, wx.ALL, 5)

        self.m_choice1Choices = ['The Guardian', 'Bloomberg']
        self.m_choice1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.m_choice1Choices, 0)
        self.m_choice1.SetSelection(0)
        self.news_provider = self.m_choice1Choices[0]
        self.m_choice1.Bind(wx.EVT_CHOICE, self.OnChoice)
        NewsWindowTools.Add(self.m_choice1, 0, wx.ALL, 5)

        self.m_searchCtrl2 = wx.SearchCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_searchCtrl2.ShowSearchButton(True)
        self.m_searchCtrl2.ShowCancelButton(False)
        self.m_searchCtrl2.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearch)
        self.m_searchCtrl2.SetMinSize(wx.Size(-1, 30))
        NewsWindowTools.Add(self.m_searchCtrl2, 0, wx.ALL, 5)


        NewsContainer1.Add(NewsWindowTools, 0, wx.ALL, 5)
        self.m_staticline51 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        NewsContainer1.Add(self.m_staticline51, 0, wx.EXPAND | wx.ALL, 5)

        NewsProperties = wx.BoxSizer(wx.HORIZONTAL)
        self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, u"Article ID:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)
        self.m_staticText6.SetMinSize(wx.Size(85, -1))
        NewsProperties.Add(self.m_staticText6, 0, wx.ALL, 5)

        self.m_staticline6 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        NewsProperties.Add(self.m_staticline6, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticText7 = wx.StaticText(self, wx.ID_ANY, u"Article title:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)
        self.m_staticText7.SetMinSize(wx.Size(420, -1))
        NewsProperties.Add(self.m_staticText7, 0, wx.ALL, 5)

        self.m_staticline7 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        NewsProperties.Add(self.m_staticline7, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticText8 = wx.StaticText(self, wx.ID_ANY, u"Publisher:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText8.Wrap(-1)
        self.m_staticText8.SetMinSize(wx.Size(100, -1))
        NewsProperties.Add(self.m_staticText8, 0, wx.ALL, 5)

        self.m_staticline8 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        NewsProperties.Add(self.m_staticline8, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticText9 = wx.StaticText(self, wx.ID_ANY, u"Published On:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)
        self.m_staticText9.SetMinSize(wx.Size(200, -1))
        NewsProperties.Add(self.m_staticText9, 0, wx.ALL, 5)

        self.m_staticline10 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        NewsProperties.Add(self.m_staticline10, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticline9 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        NewsProperties.Add(self.m_staticline9, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticText10 = wx.StaticText(self, wx.ID_ANY, u"Read article", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText10.Wrap(-1)
        self.m_staticText10.SetMinSize(wx.Size(100, -1))
        NewsProperties.Add(self.m_staticText10, 0, wx.ALL, 5)

        NewsContainer1.Add(NewsProperties, 0, wx.EXPAND, 5)

        self.m_staticline12 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        NewsContainer1.Add(self.m_staticline12, 0, wx.EXPAND | wx.ALL, 5)

        self.NewsContainer = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
        self.NewsContainer.SetScrollRate(5, 5)
        ##################################### STATIC UI ##################################### 

        self.NewsList = wx.BoxSizer(wx.VERTICAL)

        self.NewsContainer.SetSizer(self.NewsList)
        self.NewsContainer.Layout()
        self.NewsList.Fit(self.NewsContainer)
        NewsContainer1.Add(self.NewsContainer, 1, wx.EXPAND | wx.ALL, 5)
        self.NewsWindow.Add(NewsContainer1, 1, wx.ALL, 5)

    def OnDateFrom(self, event):
        """Updates the from_date"""
        self.from_date = event.GetDate()
        self.from_date = self.from_date.FormatISODate()

    def OnDateTo(self, event):
        """Updates the to_date"""
        self.to_date = event.GetDate()
        self.to_date = self.to_date.FormatISODate()

    def OnChoice(self, event):
        """Updates the news_provider with the one being selected"""
        ind = event.GetSelection()
        self.news_provider = self.m_choice1Choices[ind]

    def OnSearch(self, event):
        """
        Makes a request to the news provider API with the request settings
        provided by the user.
        Displays an error if no news were fetched.
        If there is a result, the UI is cleared [if needed], the result is sent to
        FetchFields(self, data)
        """
        if self.HasInternet():
            self.query_txt = event.GetString()
            if self.query_txt is not None and self.query_txt != "":
                send_qry = ReadNews(self, self.from_date, self.to_date, self.news_provider, self.query_txt)
                get_data = send_qry.GetQuery()
                if get_data['Error'] != "":
                    wx.MessageBox(get_data["Error"], caption="Error")
                elif get_data["Success"] != "":
                    get_data = get_data["Success"]
                    wx.MessageBox("Success! Fetching results...", caption="Success")

                    if self.NewsList.IsEmpty():
                        self.FetchFields(get_data)
                    else:
                        self.get_data_text.clear()
                        self.get_data_img.clear()
                        self.get_data_published_on.clear()
                        self.get_data_title.clear()

                        self.news_rows = 0

                        self.NewsList.Clear(delete_windows=True)
                        self.NewsList.Layout()
                        self.FetchFields(get_data)
                del send_qry
                del get_data
            else:
               wx.MessageBox("You need to enter text in the searh field!", parent = self, caption="Warning")
        else:
            wx.MessageBox("Please connect to Internet to complete the search.", caption="No Internet")

    def FetchFields(self, data):
        """
        Fetches the data from the JSON and fills it in the corresponding list.
        Calls LoadDataToUI(self, news_rows) when finished
        """
        _total_results = data['response']['total']
        _page_size = data['response']['pages']
        _data = data['response']['results']

        if _total_results == 0:
            wx.MessageBox("Uups, there seem to be no results matching the query.", caption="No Results")
        else:
            self.news_rows = 0
            for i in _data:

                if "webTitle" in i:
                    self.get_data_title.append(i["webTitle"])
                else:
                    self.get_data_title.append("N/A")
                
                if "webPublicationDate" in i:
                    tmp_date = i["webPublicationDate"]
                    convert_tmp_date = time.strptime(tmp_date, "%Y-%m-%dT%H:%M:%S%fZ")
                    self.get_data_published_on.append(time.strftime("%Y-%m-%d at %H:%Mh", convert_tmp_date))
                else:
                    self.get_data_published_on.append("N/A")

                if "thumbnail" in i["fields"]:
                    self.get_data_img.append(i["fields"]["thumbnail"])
                else:
                    self.get_data_img.append("img\placeholder300x202.jpg")
                
                if "bodyText" in i["fields"]:
                    self.get_data_text.append(i["fields"]["bodyText"])
                else:
                    self.get_data_text.append("N/A")

                self.news_rows  = self.news_rows + 1
            
            self.LoadDataToUI(self.news_rows)
                

    def LoadDataToUI(self, news_rows):
        """
        Goes through all the lists and fills the information from each list
        to the corresponding location in the news list item. Then adds the 
        news list item to the news list
        """
        for i in range(0, news_rows):

            self.NewsListPanel = wx.Panel( self.NewsContainer, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
            self.NewsListItem = wx.BoxSizer(wx.HORIZONTAL)

            self.NewsListItem_id = wx.StaticText(self.NewsListPanel, wx.ID_ANY, str(i + 1), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
            self.NewsListItem_id.Wrap(-1)
            self.NewsListItem_id.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
            self.NewsListItem_id.SetMinSize(wx.Size(75, -1))
            self.NewsListItem.Add(self.NewsListItem_id, 0, wx.ALIGN_CENTER | wx.ALL, 5)

            self.m_staticline11 = wx.StaticLine(self.NewsListPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
            self.NewsListItem.Add(self.m_staticline11, 0, wx.EXPAND | wx.ALL, 5)
            self.NewsListItem_Title = wx.StaticText(self.NewsListPanel, wx.ID_ANY, self.get_data_title[i], wx.DefaultPosition, wx.DefaultSize, 0)
            self.NewsListItem_Title.Wrap(-1)
            self.NewsListItem_Title.SetMinSize(wx.Size(420, -1))
            self.NewsListItem.Add(self.NewsListItem_Title, 0, wx.ALIGN_CENTER | wx.ALL, 5)

            self.m_staticline121 = wx.StaticLine(self.NewsListPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
            self.NewsListItem.Add(self.m_staticline121, 0, wx.EXPAND | wx.ALL, 5)
            self.NewsListItem_Publisher = wx.StaticText(self.NewsListPanel, wx.ID_ANY, self.news_provider, wx.DefaultPosition, wx.DefaultSize, 0)
            self.NewsListItem_Publisher.Wrap(-1)
            self.NewsListItem_Publisher.SetMinSize(wx.Size(100, -1))
            self.NewsListItem.Add(self.NewsListItem_Publisher, 0, wx.ALIGN_CENTER | wx.ALL, 5)

            self.m_staticline13 = wx.StaticLine(self.NewsListPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
            self.NewsListItem.Add(self.m_staticline13, 0, wx.EXPAND | wx.ALL, 5)

            self.NewsListItem_Published = wx.StaticText(self.NewsListPanel, wx.ID_ANY, self.get_data_published_on[i], wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
            self.NewsListItem_Published.Wrap(-1)
            self.NewsListItem_Published.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
            self.NewsListItem_Published.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
            self.NewsListItem_Published.SetMinSize(wx.Size(200, -1))
            self.NewsListItem.Add(self.NewsListItem_Published, 0, wx.ALIGN_CENTER | wx.ALL, 5)

            self.m_staticline14 = wx.StaticLine(self.NewsListPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
            self.NewsListItem.Add(self.m_staticline14, 0, wx.EXPAND | wx.ALL, 5)

            self.m_button9 = wx.Button(self.NewsListPanel, wx.ID_ANY, (u"Read {0}").format(i + 1), wx.DefaultPosition, wx.DefaultSize, 0)
            self.m_button9.Bind(wx.EVT_BUTTON, self.OnReadButtonClick)
            self.NewsListItem.Add(self.m_button9, 0, wx.ALL, 5)

            self.NewsListItem.Layout()
            self.NewsListPanel.SetSizer(self.NewsListItem)
            self.NewsListItem.Fit( self.NewsListPanel )
            self.NewsList.Add(self.NewsListPanel, 0, wx.EXPAND | wx.ALL, 5)
            self.Layout()

    def OnReadButtonClick(self, event):
        """
        When the user clicks on an article button to read the article,
        all the information about it is selected and sent to a ReadNewsFrame object
        to be read
        """
        btn = event.EventObject
        nr_btn_label = int(btn.GetLabel().split(" ")[1]) - 1
        
        self.read_news_frame_img_src = self.get_data_img[nr_btn_label]
        self.read_news_frame_text = self.get_data_text[nr_btn_label]
        self.read_news_frame_title = self.get_data_title[nr_btn_label]
        self.read_news_frame_source = self.news_provider
        self.read_news_frame_published_on = self.get_data_published_on[nr_btn_label]

        NewsFrame = ReadNewsFrame(self, self.read_news_frame_img_src, self.read_news_frame_text, self.read_news_frame_title, self.read_news_frame_source, self.read_news_frame_published_on)
           
    def HasInternet(self):
        """
        Checks for an internet connection
        return : True - there's internet
        return : False - there's no internet
        """
        try:
            socket.create_connection(("www.abv.bg", 80))
            return True
        except OSError:
            return False