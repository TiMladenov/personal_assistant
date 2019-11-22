import wx
from wx.adv import TimePickerCtrl as TimePickerCtrl
from wx.adv import CalendarCtrl as CalendarCtrl
import datetime
import sqlite3
from wx.media import MediaCtrl as MediaCtrl

class Alarm( wx.Frame ):
    """
    A wx.Frame class that enables the user to  set, stop and remove alarms from the application
    ...
    Attributes:
    parent : wx.Frame
        The parent object that this class inherits to store the alarm data.
    date : str
        Stores the selected alarm date when the user clicks on CalendarCtrl
    time : str
        Stores the selected alarm time when the user clicks on TimePickerCtrl
    db_conn : sqlite3
        Connection instance to the sqlite3 DB where the alarms are saved and kept
    m_alarm_choice_list : list
        A list that stores the created alarms by the user
    selected_alarm_choice : str
        Stores the alarm that the user clicked on from the wx.Choice object
    current_alarm : str
        Stores the current or active alarm that the user has set
    alarms : list
        A list used to store the alarms when they are fetched from the DB
    m_alarm_calendar : CalendarCtrl
        A calendar control that enables the user to pick a desired alarm date.
        The control takes an input after a double click
    m_static_pick_hour : TimePickerCtrl
        A time picker control that enables the user to pick a desired alarm time.
        The control takes an input after the user enters a number in it
    m_choice6 : wx.Choice
        A choice dropdown that stores the list of user alarms
    btn_alarm_set : wx.Button
        Used by the user to confirm and set a desired alarm.
        Calls the SetStoredDateAndTime(self, event) method
    btn_alarm_delete : wx.Button
        Used by the user to confirm the deleting of an alarm.
        The user must pick an alarm from the dropdown list.
        Calls the OnDelete(self, event) method
    btn_alarm_stop : wx.Button
        Used to hide the alarm frame and also to stop the alarm sound if it's on
        Calls the OnStop(self, event) method
    play : wx.media.Mediactrl
        Used to store the alarm sound
    timer : wx.Timer
        Used to run a check every second on current time and active alarm
    ...
    Methods:
    ConnectDb(self)
        Initiates a connection to the DB
    GetStoredDateAndTime(self)
        Returns the stored alarm date and time from the DB
    SetStoredDateAndTime(self, event)
        Sets the desired new date and time for a new alarm in the DB
        Returns True if successful
    OnDelete(self)
        Gets the date and time of the alarm to be deleted. 
        Stops it from playing if it is doing so at the time.
        Calls for DeleteStoredAlarms(self, date, time)
    DeleteStoredAlarms(self, date, time)
        Attempts to delete the selected alarm. Returns True if successful
    SetTime(self, event)
        Formats the value for time to ISO format and saves it in the time variable
    SetDate(self, event)
        Formats the value for date to ISO format and saves it in the date variable
    CheckTime(self, event)
        Gets the time active alarm time and compares it to current time, every second.
        If the alarm date hasn't passed and the alarm time matches the current time,
        the alarm will be actibated in OnRing(command)
    GetSelectedAlarm(self, event)
        Sets visible the current active alarm.
    OnClose(self, event)
        Hides the alarm window when closed
    OnStop(self, event)
        Stops the alarm if it is ringing
    OnRing(self, command)
        If the command is 'ring', the alarm will be activated.
        If the command is 'stop', the alarm will be stoped, if it is ringing.
    loadSound(self)
        Loads the ringtone for the alarm
    melodyLoaded(self, event)
        Plays the alarm
    updateAlarmList(self)
        Updates the choice dropdown alarm list
    """

    def __init__(self, parent):
        super(Alarm, self).__init__ ( parent = parent, id = wx.ID_ANY, title = u"Alarm settings", pos = wx.DefaultPosition, size = wx.Size( 305,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        self.date = None
        self.time = None
        self.db_conn = None
        self.m_alarm_choice_list = []
        self.selected_alarm_choice = None
        self.current_alarm = None
        self.alarms = None

        self.ConnectDb()

        self.alarms = self.GetStoredDateAndTime()

        if self.alarms:
            if len(self.alarms) > 0:
                for alarm in self.alarms:
                    tmp_alarm = alarm[0] + " " + alarm[1]
                    self.m_alarm_choice_list.append(tmp_alarm)

        ############################ STATIC UI #########################################################
        alarm_settings_sizer = wx.BoxSizer( wx.VERTICAL )

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.CheckTime, self.timer)
        self.timer.Start(1000)

        self.settings_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        settings_sizer = wx.BoxSizer( wx.VERTICAL )

        self.settings_options_sizer = wx.BoxSizer( wx.VERTICAL )

        self.m_static_date_pick = wx.StaticText( self.settings_panel, wx.ID_ANY, u"Pick a date [double click]:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_date_pick.Wrap( -1 )

        self.settings_options_sizer.Add( self.m_static_date_pick, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_alarm_calendar = CalendarCtrl( self.settings_panel, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.CAL_SHOW_HOLIDAYS )
        self.m_alarm_calendar.Bind(wx.adv.EVT_CALENDAR, self.SetDate)
        self.settings_options_sizer.Add( self.m_alarm_calendar, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_static_pick_hour = wx.StaticText( self.settings_panel, wx.ID_ANY, u"Pick an hour [enter a number]:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_pick_hour.Wrap( -1 )

        self.settings_options_sizer.Add( self.m_static_pick_hour, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_alarm_time = TimePickerCtrl( self.settings_panel, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.Size( 230,-1 ), wx.adv.DP_DEFAULT )
        self.m_alarm_time.Bind(wx.adv.EVT_TIME_CHANGED, self.SetTime)
        self.settings_options_sizer.Add( self.m_alarm_time, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_static_alarm_list = wx.StaticText( self.settings_panel, wx.ID_ANY, u"Alarms' list:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_alarm_list.Wrap( -1 )

        self.settings_options_sizer.Add( self.m_static_alarm_list, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_choice6 = wx.Choice( self.settings_panel, wx.ID_ANY, wx.DefaultPosition, wx.Size( 230,-1 ), self.m_alarm_choice_list, 0 )
        self.m_choice6.SetSelection( 0 )

        self.m_choice6.Bind(wx.EVT_CHOICE, self.GetSelectedAlarm)
        self.settings_options_sizer.Add( self.m_choice6, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_static_active_alarm = wx.StaticText( self.settings_panel, wx.ID_ANY, u"Active alarm:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_active_alarm.Wrap( -1 )

        self.settings_options_sizer.Add( self.m_static_active_alarm, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.var_active_alarm = wx.StaticText( self.settings_panel, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.var_active_alarm.Wrap( -1 )

        try:
            self.current_alarm = self.m_alarm_choice_list[0]
            self.var_active_alarm.SetLabel(self.current_alarm)
        except:
            self.current_alarm = ""

        self.settings_options_sizer.Add( self.var_active_alarm, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        settings_sizer.Add( self.settings_options_sizer, 1, wx.EXPAND, 5 )

        settings_buttons_sizer = wx.BoxSizer( wx.HORIZONTAL )

        self.btn_alarm_set = wx.Button( self.settings_panel, wx.ID_ANY, u"Set", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btn_alarm_set.Bind(wx.EVT_BUTTON, self.SetStoredDateAndTime)
        settings_buttons_sizer.Add( self.btn_alarm_set, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 5 )

        self.btn_alarm_delete = wx.Button( self.settings_panel, wx.ID_ANY, u"Delete alarm", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btn_alarm_delete.Bind(wx.EVT_BUTTON, self.OnDelete)
        settings_buttons_sizer.Add( self.btn_alarm_delete, 1, wx.ALIGN_CENTER|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 5 )

        self.btn_alarm_stop = wx.Button( self.settings_panel, wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btn_alarm_stop.Bind(wx.EVT_BUTTON, self.OnStop)
        settings_buttons_sizer.Add( self.btn_alarm_stop, 1, wx.ALIGN_CENTER|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 5 )

        self.play = MediaCtrl(self, szBackend=wx.media.MEDIABACKEND_GSTREAMER)
        self.play.Bind(wx.media.EVT_MEDIA_LOADED, self.melodyLoaded)

        settings_sizer.Add( settings_buttons_sizer, 0, wx.EXPAND, 5 )

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.settings_panel.SetSizer( settings_sizer )
        self.settings_panel.Layout()
        settings_sizer.Fit( self.settings_panel )
        alarm_settings_sizer.Add( self.settings_panel, 1, wx.EXPAND |wx.ALL, 5 )

        self.SetSizer( alarm_settings_sizer )
        self.Layout()

        self.Centre( wx.BOTH )
        ############################ STATIC UI #########################################################

    def ConnectDb(self):
        """Initiates a connection to the DB"""
        try:
            self.db_conn = sqlite3.connect('db/personal_assistant.db')
        except Exception as e:
            exc_text = str(e)
            msg_txt = "Could not connect to DB. Reason:\n" + exc_text
            wx.MessageBox(message = msg_txt, caption = "Error. No DB connection")

    def GetStoredDateAndTime(self):
        """Returns the stored alarm date and time from the DB"""
        try:
            db_cursor = self.db_conn.cursor()
            db_cursor.execute("SELECT date, time FROM alarm_table WHERE active = 1")
            fetched_alarms = db_cursor.fetchall()
            return fetched_alarms
        except Exception as e:
            wx.MessageBox('Failed to get stored date:\n' + str(e), 'Error getting saved alarm')
            return False

    def SetStoredDateAndTime(self, event):
        """
        Sets the desired new date and time for a new alarm in the DB
        Returns True if successful
        """
        try:
            _date = self.date
            _time = self.time
            if _date and _time:
                db_cursor = self.db_conn.cursor()
                db_cursor.execute("INSERT INTO alarm_table VALUES ('{}','{}', '{}')".format(_date, _time, 1))
                self.db_conn.commit()
                self.updateAlarmList()
                return True
            else:
                wx.MessageBox('Select date and time to save first.', 'Error')
                return False
        except Exception as e:
            wx.MessageBox('Failed to store date and time:\n' + str(e), 'Error saving alarm')
            return False

    def OnDelete(self, event):
        """
        Gets the date and time of the alarm to be deleted. 
        Stops it from playing if it is doing so at the time.
        Calls for DeleteStoredAlarms(self, date, time)
        """
        try:
            _alarm_propery = self.selected_alarm_choice.split(" ")
            _date = _alarm_propery[0]
            _time = _alarm_propery[1]

            self.play.Stop()

            self.DeleteStoredAlarms(_date, _time)
        except Exception as e:
            wx.MessageBox('Select an alarm to delete first.', 'Error')

    def DeleteStoredAlarms(self, _date, _time):
        """Attempts to delete the selected alarm. Returns True if successful"""
        try:
            db_cursor = self.db_conn.cursor()
            db_cursor.execute("DELETE FROM alarm_table WHERE date='{}' AND time='{}'".format(_date, _time))
            self.db_conn.commit()
            self.updateAlarmList()
            return True
        except Exception as e:
            wx.MessageBox('Failed to delete date and time:\n' + str(e), 'Error deleting alarm')
            return False

    def SetDate(self, event):
        """Formats the value for date to ISO format and saves it in the date variable"""
        _date = event.GetDate()
        _date = _date.FormatISODate()
        self.date = _date

    def SetTime(self, event):
        """Formats the value for time to ISO format and saves it in the time variable"""
        _time = self.m_alarm_time.GetValue()
        _time = _time.FormatISOTime()
        self.time = _time

    def CheckTime(self, event):
        """
        Gets the time active alarm time and compares it to current time, every second.
        If the alarm date hasn't passed and the alarm time matches the current time,
        the alarm will be actibated in OnRing(command)
        """
        try:
            _alarm = self.current_alarm.split(" ")
            _date = _alarm[0]
            _time = _alarm[1]

            timer_datetime = wx.DateTime.Now()
            timer_date = timer_datetime.FormatISODate()
            timer_time = timer_datetime.FormatISOTime()

            if _date >= timer_date:
                if _date == timer_date and _time == timer_time:
                    self.OnRing('ring')
        except:
            pass

    def GetSelectedAlarm(self, event):
        """Sets visible the current active alarm."""
        ind = event.GetSelection()
        self.selected_alarm_choice = self.m_alarm_choice_list[ind]
        self.current_alarm = self.selected_alarm_choice
        self.var_active_alarm.SetLabel(self.current_alarm)
        self.Layout()

    def OnClose(self, event):
        """Hides the alarm window when closed"""
        self.Hide()

    def OnStop(self, event):
        """Stops the alarm if it is ringing"""
        self.OnRing('stop')

    def OnRing(self, _command):
        """
        If the command is 'ring', the alarm will be activated.
        If the command is 'stop', the alarm will be stoped, if it is ringing.
        """
        if _command == 'ring':
            self.Show()
            self.loadSound()
        else:
            self.play.Stop()
            self.Hide()

    def loadSound(self):
        """Loads the ringtone for the alarm"""
        self.play.Load(r'/home/tmladenov/workspace/wxFormBuilder/smart_assistant_app_code/wxPythonApp/audio/imperial_alert.mp3')

    def melodyLoaded(self, event):
        """Plays the alarm"""
        self.play.Play()

    def updateAlarmList(self):
        """Updates the choice dropdown alarm list"""

        self.m_alarm_choice_list.clear()
        self.alarms = self.GetStoredDateAndTime()
        self.m_choice6.Clear()
        self.m_choice6.Layout()

        for alarm in self.alarms:
            tmp_alarm = alarm[0] + " " + alarm[1]
            self.m_alarm_choice_list.append(tmp_alarm)
            self.m_choice6.Append(tmp_alarm)

        self.m_choice6.SetSelection(0)

        self.current_alarm = ""
        self.var_active_alarm.SetLabel(self.current_alarm)

        self.m_choice6.Layout()
        self.Layout()