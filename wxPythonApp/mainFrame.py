import wx
import wx.adv
import wx.xrc
from news_panel_class import NewsPanel
from news_rss_panel_class import NewsRss
from email_panel_class import EmailPanel
from social_panel_class import SocialPanel
from about_frame import About
from alarm_frame import Alarm
from datetime import datetime
from weather_location_class import WeatherLocation
import socket

class MainFrame(wx.Frame):
    """
    MainFrame class inherits wx.Frame and is the main frame for the application. All other modules are children to this module
    and remain loaded in memory for the whole runtime of the app.
    ...
    Attributes:
    timer : wx.Timer
        Runs the clock of the application on the top right corner
        Calls UpdateUI(self, event)
    settings_set_alarm : wx.MenuItem
        When clicked, this menu item calls the AlarmSettings(self, event) method.
        It is used to control the alarm properties
    help_about : wx. MenuItem
        When clicked, this menu item calls the ShowAbout(self, event) method.
        It is used to display the About frame with information on the app.
    btn_news : wx.Button
        This button displays the News (Rest API) panel.
        When pressed, it calls the OnNavBtnPress(self, event) method.
    btn_news_rss : wx.Button
        This button displays the News (RSS) panel.
        When pressed, it calls the OnNavBtnPress(self, event) method.
    btn_email : wx.Button
        This button displays the Email panel.
        When pressed, it calls the OnNavBtnPress(self, event) method.
    btn_social : wx.Button
        This button displays the Social panel.
        When pressed, it calls the OnNavBtnPress(self, event) method
    nav_location : wx.StaticText
        When there's internet and location information is fetched, this
        text displays the location of the user
    nav_time : wx.StaticText
        Displays the time fetched from the operating system of the user
    nav_weather : wx.StaticText
        When there's internet and weather information is fetched, this
        text displays the weather in user's location
    alarm_frame : wx.Frame
        This is the frame used by the user to set up or control his alarms
    about_frame : wx.Frame
        This is the frame containing meta information on the app and creator
    NewsPanel : wx.Panel
        This panel is used to display the news fetched by the RESTful service
        of The Guardian [for now]
    NewsRssPanel : wx.Panel
        This panel is used to display the news fetched by the RSS services of
        various news providers
    EmailPanel : wx.Panel
        This panel is used to display the emails of the user, fetched from
        Gmail API
    SocialPanel : wx.Panel
        This panel is used to display the panels of social media, i.e.
        Twitter and Facebook [for now]
    ...
    Methods:
    OnClose(self, event)
        Asks the user to confirm his intention to close the application.
        Closes the application if the user confirms
    OnNavBtnPress(self, event)
        Only one child panel of MainFrame must be visible at a time. This method
        hides all other child panels and leaves only the one selected by the user
        to be shown
    UpdateUI(self, event)
        Updates the clock that is shown on the top right corner of the application
    HasInternet(self)
        Checks if there's internet
        return True - there's internet
        return False - there's no internet
    UpdateTime(self, event)
        Initiates the calls to get user's location and the weather information for it
        If there's fetched data, the UI is updated with this information
    AlarmSettings(self, event)
        Shows the alarm frame
    ShowAbout(self, event)
        Shows the about frame
    """

    def __init__(self, title = u"Personal Assistant", id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size(1100, 800), style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER | wx.TAB_TRAVERSAL):
        wx.Frame.__init__(self, None, id = wx.ID_ANY, title = title, pos = pos, size = size, style = style)

        ######## ADDING MAIN FRAME MENUBAR AND TOOLBAR ################################
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.MainMenuBar = wx.MenuBar(0)
        self.MainMenuBar.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )
        self.MainMenuBar_Settings = wx.Menu()

        self.settings_set_alarm = wx.MenuItem(self.MainMenuBar_Settings, wx.ID_ANY, u"Set Alarm", wx.EmptyString, wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.AlarmSettings, self.settings_set_alarm)
        self.MainMenuBar_Settings.Append(self.settings_set_alarm)

        self.MainMenuBar.Append(self.MainMenuBar_Settings, u"Alarm")

        self.MainMenuBar_Help = wx.Menu()
        self.help_about = wx.MenuItem(self.MainMenuBar_Help, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.ShowAbout, self.help_about)
        self.MainMenuBar_Help.Append(self.help_about)

        self.MainMenuBar.Append(self.MainMenuBar_Help, u"Help")

        self.SetMenuBar(self.MainMenuBar)

        RootWindow = wx.BoxSizer(wx.VERTICAL)

        NavToolBar = wx.BoxSizer(wx.HORIZONTAL)

        NavToolBar_Buttons = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_news = wx.Button(self, wx.ID_ANY, u"News", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, self.OnNavBtnPress, self.btn_news)
        NavToolBar_Buttons.Add(self.btn_news, 0, wx.ALL, 5)

        self.btn_news_rss = wx.Button(self, wx.ID_ANY, u"News RSS", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, self.OnNavBtnPress, self.btn_news_rss)
        NavToolBar_Buttons.Add(self.btn_news_rss, 0, wx.ALL, 5)

        self.btn_email = wx.Button(self, wx.ID_ANY, u"Email", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, self.OnNavBtnPress, self.btn_email)
        NavToolBar_Buttons.Add(self.btn_email, 0, wx.ALL, 5)

        self.btn_social = wx.Button(self, wx.ID_ANY, u"Social", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, self.OnNavBtnPress, self.btn_social)
        NavToolBar_Buttons.Add(self.btn_social, 0, wx.ALL, 5)

        NavToolBar.Add(NavToolBar_Buttons, 1, 0, 5)

        NavToolBar_Location = wx.BoxSizer(wx.HORIZONTAL)

        if self.HasInternet():
            GetWeatherAndLocation = WeatherLocation()
            city = GetWeatherAndLocation.GetCity()
            country = GetWeatherAndLocation.GetCountry()

        self.nav_location = wx.StaticText(self, wx.ID_ANY, u"N/A", wx.DefaultPosition, wx.DefaultSize, 0)

        if self.HasInternet():
            if city != "N/A":
                self.nav_location.SetLabel(city)
                if country != "N/A":
                    self.nav_location.SetLabel(city + ", " + country)
        self.nav_location.Wrap(-1)

        NavToolBar_Location.Add(self.nav_location, 1, wx.ALL, 5)

        self.m_staticline4 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        NavToolBar_Location.Add(self.m_staticline4, 0, wx.EXPAND | wx.ALL, 5)

        self.nav_time = wx.StaticText(self, wx.ID_ANY, u"N/A h, N/A", wx.DefaultPosition, (120, -1), 0)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.UpdateUI, self.timer)
        self.timer.Start(1000)
        self.nav_time.Wrap(-1)

        NavToolBar_Location.Add(self.nav_time, 1, wx.ALL, 5)

        self.m_staticline5 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        NavToolBar_Location.Add(self.m_staticline5, 1, wx.EXPAND | wx.ALL, 5)

        if self.HasInternet():
            weather = GetWeatherAndLocation.GetWeather()
            temp = GetWeatherAndLocation.GetTemp()

        self.nav_weather = wx.StaticText(self, wx.ID_ANY, u"N/A C, N/A", wx.DefaultPosition, wx.DefaultSize, 0)
        if self.HasInternet():
            if weather != "N/A" and temp != None:
                self.nav_weather.SetLabel(str(temp) + "C, " + weather)
        self.nav_weather.Wrap(-1)

        self.time_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.UpdateTime, self.time_timer)
        self.time_timer.Start(900000)

        NavToolBar_Location.Add(self.nav_weather, 1, wx.ALL, 5)

        NavToolBar.Add(NavToolBar_Location, 0, wx.ALL, 5)

        RootWindow.Add(NavToolBar, 0, wx.EXPAND, 5)

        self.nav_cont_spacer = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        RootWindow.Add(self.nav_cont_spacer, 0, wx.EXPAND | wx.ALL, 5)

        ######## ADDING THE ALARM FRAME ######################################################
        self.alarm_frame = Alarm(self)
        ######## ADDING THE ALARM FRAME ######################################################

        ######## ADDING THE ABOUT FRAME ######################################################
        self.about_frame = About(self)
        ######## ADDING THE ABOUT FRAME ######################################################

        ######## ADDING THE NEWS_API NEWSPANEL ###############################################
        self.NewsPanel = NewsPanel(self)
        self.NewsPanel.SetSizer(self.NewsPanel.NewsWindow)
        self.NewsPanel.Layout()
        self.NewsPanel.NewsWindow.Fit(self.NewsPanel)
        RootWindow.Add(self.NewsPanel, 1, wx.EXPAND | wx.ALL, 5)
        ######## ADDING THE NEWS_API NEWSPANEL ###############################################

        ######## ADDING THE NEWS_RSS NEWSPANEL ###############################################
        self.NewsRssPanel = NewsRss(self)
        RootWindow.Add(self.NewsRssPanel, 1, wx.EXPAND | wx.ALL, 5)
        ######## ADDING THE NEWS_RSS NEWSPANEL ###############################################

        ######## ADDING THE EmailPanel NEWSPANEL #############################################
        self.EmailPanel = EmailPanel(self)
        RootWindow.Add(self.EmailPanel, 1, wx.EXPAND | wx.ALL, 5)
        ######## ADDING THE EmailPanel NEWSPANEL #############################################

        ######## ADDING THE EmailPanel NEWSPANEL #############################################
        self.SocialPanel = SocialPanel(self)
        RootWindow.Add(self.SocialPanel, 1, wx.EXPAND | wx.ALL, 5)
        ######## ADDING THE EmailPanel NEWSPANEL #############################################

        ######## ADDING MAIN FRAME MENUBAR AND TOOLBAR ################################

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.SetSizer(RootWindow)
        self.Layout()

        self.Centre(wx.BOTH)

        def __del__(self):
            pass

    def OnClose(self, event):
        """
        Asks the user to confirm his intention to close the application.
        Closes the application if the user confirms
        """
        qtn = "Do you really want to close the application?"
        actn = "Warning"
        dialog = wx.MessageDialog(self, qtn, actn, wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        result = dialog.ShowModal()
        dialog.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    def OnNavBtnPress(self, event):
        """
        Only one child panel of MainFrame must be visible at a time. This method
        hides all other child panels and leaves only the one selected by the user
        to be shown
        """
        btn = event.EventObject
        if btn is self.btn_news_rss:
            self.NewsPanel.Hide()
            self.NewsRssPanel.Show()
            self.EmailPanel.Hide()
            self.SocialPanel.Hide()
        elif btn is self.btn_news:
            self.NewsPanel.Show()
            self.NewsRssPanel.Hide()
            self.EmailPanel.Hide()
            self.SocialPanel.Hide()
        elif btn is self.btn_email:
            self.NewsPanel.Hide()
            self.NewsRssPanel.Hide()
            self.EmailPanel.Show()
            self.SocialPanel.Hide()
        elif btn is self.btn_social:
            self.NewsPanel.Hide()
            self.NewsRssPanel.Hide()
            self.EmailPanel.Hide()
            self.SocialPanel.Show()
        self.Layout()

    def UpdateUI(self, event):
        """
        Updates the clock that is shown on the top right corner of the application
        """
        time = wx.DateTime.Now()
        time = time.Format("%d-%b-%Y, %a, %H:%M")
        self.nav_time.SetLabel(time)

    def HasInternet(self):
        """
        Checks if there's internet
        return True - there's internet
        return False - there's no internet
        """
        try:
            socket.create_connection(("www.abv.bg", 80))
            return True
        except OSError:
            return False

    def UpdateTime(self, event):
        """
        Initiates the calls to get user's location and the weather information for it
        If there's fetched data, the UI is updated with this information
        """
        if self.HasInternet():
            GetWeatherAndLocation = WeatherLocation()
            city = GetWeatherAndLocation.GetCity()
            country = GetWeatherAndLocation.GetCountry()
            if city != "N/A":
                self.nav_location.SetLabel(city)
                if country != "N/A":
                    self.nav_location.SetLabel(city + ", " + country)

            weather = GetWeatherAndLocation.GetWeather()
            temp = GetWeatherAndLocation.GetTemp()
            if weather != "N/A" and temp != None:
                self.nav_weather.SetLabel(str(temp) + "C, " + weather)

            self.Layout()

        else:
            self.nav_location.SetLabel("N/A" + ", " + "N/A")
            self.nav_weather.SetLabel("N/A" + "C, " + "N/A")

    def AlarmSettings(self, event):
        """Shows the alarm frame"""
        self.alarm_frame.Show()

    def ShowAbout(self, event):
        """Shows the about frame"""
        self.about_frame.Show()