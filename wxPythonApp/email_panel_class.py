import wx
from GmailApiCall import GmailApi
from TTS_Reader import TextToSpeech
import socket
import base64
import sqlite3

class EmailData (object) :
    """
    A class to store the date for each email
    ...
    Attributes:
    sent_from : str
        The email and name of the account who sent the email
    sent_to : str
        The email and name of the account who received the email
    sent_date : str
        The date the email was sent
    subject : str
        The subject of the email
    mail_text : str
        The main content of the email
    file_name : str
        The name of the attached file (if there's one in the email)
    last_msg_text : str
        The text of the last read email
    ...
    Methods:
    set_sent_from(self, sent_from : str)
        Sets the sender of the email
    get_sent_from(self)
        Returns the sender of the email
        return : str
    set_sent_to(self, sent_to : str)
        Sets the receiver of the email
    get_sent_to(self)
        Returns the receiver of the email
        return : str
    set_subject(self, subject : str)
        Sets the email subject
    get_subject(self)
        Returns the subject of the email
        return : str
    set_file_name(self, name : str)
        Sets the name of the attached file (if there's one)
    set_sent_date(self, date : str)
        Sets the date of email sending
    get_sent_date(self)
        Returns the sent date of the email
        return : str
    set_mail_text(self, text : str)
        Sets the text of the email
    get_main_text(self)
        Returns the text of the email
        return : str
    get_file_name(self):
        Returns the name of the attached file (if there's one)
        return : str
    """

    def __init__(self):
        self.sent_from = ""
        self.sent_to = ""
        self.sent_date = ""
        self.subject = ""
        self.mail_text = ""
        self.file_name = ""
        self.last_msg_text = ""

    def __del__(self):
        pass

    def set_sent_from(self, _sent_from):
        """Sets the sender of the email"""
        self.sent_from = _sent_from

    def get_sent_from(self):
        """
        Returns the sender of the email
        return : str
        """
        return self.sent_from

    def set_sent_to(self, _sent_to):
        """Sets the receiver of the email"""
        self.sent_to = _sent_to

    def get_sent_to(self):
        """
        Returns the receiver of the email
        return : str
        """
        return self.sent_to

    def set_subject(self, _subject):
        """
        Sets the email subject
        """
        self.subject = _subject

    def get_subject(self):
        """
        Returns the subject of the email
        return : str
        """
        return self.subject

    def set_file_name(self, _name):
        """Sets the name of the attached file (if there's one)"""
        self.file_name = _name

    def set_sent_date(self, _date):
        """Sets the date of email sending"""
        self.sent_date = _date

    def get_sent_date(self):
        """
        Returns the sent date of the email
        return : str
        """
        return self.sent_date

    def set_mail_text(self, _text):
        """Sets the text of the email"""
        self.mail_text = _text

    def get_mail_text(self):
        """
        Returns the text of the email
        return : str
        """
        return self.mail_text

    def get_file_name(self):
        """
        Returns the name of the attached file (if there's one)
        return : str
        """
        return self.file_name

class EmailPanel ( wx.Panel ):
    """
    EmalPanel inherits from wx.Panel class to store visualize the emails to the user
    ...
    Attributes:
    selected_labels : list
        Keeps the selected [str] labels by the user from the label combo box
    QUERY_OPTION : str
        A constant to be added to the query to inform Gmail API that the user
        wants the emails from the primary emailbox
    max_count : int
        Stores the user's wish for max count of emails to be returned by Gmail API
    query : str
        Optional. If the user desires to search for a specific content in the email
    email_data : str
        Stores the retured [JSON] data from the Gmail API call
    email_obj_list : list
        Stores all the EmailData objects, which are used to populate the UI
    tts : TTS_Reader
        An instance for Text-To-Speech audio for the main content of the email
    db_conn : sqlite3
        Connector to the DB where the history_id of the mailbox is stored, updated
        and retrieved periodically for sync / new email check
    email_labelsChoices : list
        Stores [str] email labels currently supported by GmailAPI
    email_results_countChoices : list
        Stores [str] options for max_count emails in the API response
    var_email_read_title : str
        The title of the detailed email view
    var_email_read_sender : str
        The email and name of the email sender.
        Used for the detailed email view
    var_email_read_sent_on : str
        The date of sending for the detailed email view
    var_email_file_count : str
        The number of attached files in the email. For the detailed email view
    var_read_email_content : str
        The main email content for the detailed email view
    button_email_close : wx.Button
        Clears the detailed email view
        Calls OnEmailButton(self, event)
    button_email_read : wx.Button
        Starts an instance of TextToSpeech for a Text-To-Speach reader
        of the main content
        Calls OnEmailButton(self, event)
    ...
    Methods:
    OnSearch(self, event)
        Initiates a full_text call to Gmail API to get the emails in JSON format
        Then calls FetchEmailData(email_data)
    OnUpdate(self, event)
        Used by the timer object to periodically make a minimal_text call to
        GmailAPI and compares the local history_id state to the one in the reply.
        Informs the user if there's a new email or a need to resync.
        After user's consent updates the UI and local history_id
    HasInternet(self)
        Checks for an Internet connection
        return : True - If there's internet connection
        return : False - If there's no internet connection
    FetchEmailData(self, data : JSON)
        Receives its data from OnSearch(self, event).
        Fetches the data from the JSON and updates
        all email objects and stored history_id
        Calls populateUi(self, email_objects)
    populateUi(self, email_objects : list)
        Goes through the list of EmailData objects and their properties
        and updates the UI by adding list item for each email
    OnReadButton(self, event)
        When a read button from an email list item is clicked,
        all the data for this email is fetched from the app runtime memory
        to populate the detailed email read window.
    OnEmailButton(self, event)
        Called by detailed email button controls. Either clears the email window
        or calls for a TTS object. Depending on the pressed button
    truncate_db_email_table(self, table_name : str)
        Method to clear the history_id DB table when needed
    update_db_email_table(self, history_id : str)
        Method to update the email table. Primarily when the 
        local history_id is to be updated
    get_history_id_db_email_table(self)
        Method to retrieve the stored history_id
        return : str - Success
        return : false - Fail
    OnClose(self, event)
        Destroys the window on its closing and stops the TTS reader if it's running
    """

    def __init__(self, parent):
        super(EmailPanel, self).__init__(parent = parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.TAB_TRAVERSAL)

        self.selected_labels = []
        self.QUERY_OPTION = "category:primary"
        self.max_count = 0
        self.query = ""
        self.email_data = ""
        self.email_obj_list = []
        self.tts = ""
        self.db_conn = None

        try:
            self.db_conn = sqlite3.connect('db/personal_assistant.db')
        except Exception as e:
            exc_text = str(e)
            msg_txt = "Could not connect to DB. Reason:\n" + exc_text
            wx.MessageBox(message = msg_txt, caption = "Error. No DB connection")

        ######################################### STATIC UI #####################################

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnUpdate, self.timer)

        EmailPanelSizer = wx.BoxSizer(wx.VERTICAL)

        EmailTools = wx.BoxSizer( wx.HORIZONTAL )

        self.m_static_search = wx.StaticText( self, wx.ID_ANY, u"Search mails:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_search.Wrap( -1 )
        EmailTools.Add( self.m_static_search, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.email_search = wx.SearchCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.email_search.ShowSearchButton( True )
        self.email_search.ShowCancelButton( False )
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearch, self.email_search)
        EmailTools.Add( self.email_search, 0, wx.ALIGN_CENTER | wx.ALL, 5 )

        self.m_static_labels = wx.StaticText( self, wx.ID_ANY, u"Email labels:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_labels.Wrap( -1 )
        EmailTools.Add( self.m_static_labels, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.email_labelsChoices = [ u"INBOX", u"UNREAD", u"STARRED", u"IMPORTANT", u"CATEGORY_PERSONAL", u"CATEGORY_SOCIAL", u"CATEGORY_PROMOTIONS", u"CATEGORY_UPDATE", u"CATEGORY_FORUMS", u"CATEGORY_UPDATES" ]
        self.email_labels = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size(160, 60), self.email_labelsChoices, wx.LB_MULTIPLE )
        self.email_labels.SetSelection(0)
        EmailTools.Add( self.email_labels, 0, wx.ALL, 5 )

        self.m_static_max_results = wx.StaticText( self, wx.ID_ANY, u"Max Results per page:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_max_results.Wrap( -1 )
        EmailTools.Add( self.m_static_max_results, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        email_results_countChoices = [ u"5", u"10", u"15", u"20", u"50" ]
        self.email_results_count = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, email_results_countChoices, 0 )
        self.email_results_count.SetSelection( 0 )
        EmailTools.Add( self.email_results_count, 0, wx.ALIGN_CENTER | wx.ALL, 5 )

        EmailPanelSizer.Add( EmailTools, 0, wx.EXPAND, 5 )

        self.m_staticline43 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        EmailPanelSizer.Add( self.m_staticline43, 0, wx.EXPAND |wx.ALL, 5 )

        self.EmailProperties = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        EmailPropertiesSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.m_static_sent_from = wx.StaticText(self.EmailProperties, wx.ID_ANY, u"Sent from:", wx.DefaultPosition, wx.Size(200, -1), 0)
        self.m_static_sent_from.Wrap(-1)

        EmailPropertiesSizer.Add(self.m_static_sent_from, 0, wx.ALL, 5)

        self.m_staticline32 = wx.StaticLine(self.EmailProperties, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        EmailPropertiesSizer.Add(self.m_staticline32, 0, wx.EXPAND | wx.ALL, 5)

        self.m_static_sent_to = wx.StaticText(self.EmailProperties, wx.ID_ANY, u"Sent to:", wx.DefaultPosition, wx.Size(200, -1), 0)
        self.m_static_sent_to.Wrap(-1)
        EmailPropertiesSizer.Add(self.m_static_sent_to, 0, wx.ALL, 5)

        self.m_staticline33 = wx.StaticLine(self.EmailProperties, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        EmailPropertiesSizer.Add(self.m_staticline33, 0, wx.EXPAND | wx.ALL, 5)

        self.m_static_subject = wx.StaticText(self.EmailProperties, wx.ID_ANY, u"Subject:", wx.DefaultPosition, wx.Size(200, -1), 0)
        self.m_static_subject.Wrap(-1)
        EmailPropertiesSizer.Add(self.m_static_subject, 0, wx.ALL, 5)

        self.m_staticline34 = wx.StaticLine(self.EmailProperties, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        EmailPropertiesSizer.Add(self.m_staticline34, 0, wx.EXPAND | wx.ALL, 5)

        self.m_static_date = wx.StaticText(self.EmailProperties, wx.ID_ANY, u"Sent on:", wx.DefaultPosition, wx.Size(150, -1), 0)
        self.m_static_date.Wrap(-1)

        EmailPropertiesSizer.Add(self.m_static_date, 0, wx.ALL, 5)

        self.m_staticline35 = wx.StaticLine(self.EmailProperties, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        EmailPropertiesSizer.Add(self.m_staticline35, 0, wx.EXPAND | wx.ALL, 5)

        self.m_static_read = wx.StaticText(self.EmailProperties, wx.ID_ANY, u"Read:", wx.DefaultPosition, wx.Size(120, -1), 0)
        self.m_static_read.Wrap(-1)
        EmailPropertiesSizer.Add(self.m_static_read, 0, wx.ALL, 5)

        self.EmailProperties.SetSizer(EmailPropertiesSizer)
        self.EmailProperties.Layout()
        EmailPropertiesSizer.Fit(self.EmailProperties)
        EmailPanelSizer.Add(self.EmailProperties, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticline39 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        EmailPanelSizer.Add(self.m_staticline39, 0, wx.EXPAND | wx.ALL, 0)

        self.EmailList = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 300), wx.HSCROLL | wx.VSCROLL)
        self.EmailList.SetScrollRate(5, 5)
        self.EmailList.SetMinSize(wx.Size(-1, 300))
        self.EmailList.SetMaxSize(wx.Size(-1, 300))

        self.EmailListSizer = wx.BoxSizer(wx.VERTICAL)

        self.EmailList.SetSizer(self.EmailListSizer)
        self.EmailList.Layout()
        EmailPanelSizer.Add(self.EmailList, 1, wx.EXPAND | wx.ALL, 5)

        self.m_staticline73 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        EmailPanelSizer.Add(self.m_staticline73, 0, wx.EXPAND | wx.ALL, 5)

        self.EmailRead = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 375), wx.TAB_TRAVERSAL)
        self.EmailRead.SetMinSize(wx.Size(975, 375))

        EmailReadSizer = wx.BoxSizer(wx.VERTICAL)

        EmailReadSizer.SetMinSize(wx.Size(975, 375))
        EmailReadProperties = wx.BoxSizer(wx.HORIZONTAL)

        self.m_static_subject = wx.StaticText(self.EmailRead, wx.ID_ANY, u"Subject:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_static_subject.Wrap(-1)
        EmailReadProperties.Add(self.m_static_subject, 0, wx.ALL, 5)

        self.var_email_read_title = wx.StaticText(self.EmailRead, wx.ID_ANY, u"", wx.DefaultPosition, wx.Size(300, -1), 0)
        self.var_email_read_title.Wrap(300)
        EmailReadProperties.Add(self.var_email_read_title, 0, wx.ALL, 5)

        self.m_static_sender = wx.StaticText(self.EmailRead, wx.ID_ANY, u"Sent from:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_static_sender.Wrap(-1)

        EmailReadProperties.Add(self.m_static_sender, 0, wx.ALL, 5)

        self.var_email_read_sender = wx.StaticText(self.EmailRead, wx.ID_ANY, u"", wx.DefaultPosition, wx.Size(150, -1), 0)
        self.var_email_read_sender.Wrap(-1)
        EmailReadProperties.Add(self.var_email_read_sender, 0, wx.ALL, 5)

        self.m_static_send_date = wx.StaticText(self.EmailRead, wx.ID_ANY, u"Sent on:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_static_send_date.Wrap(-1)
        EmailReadProperties.Add(self.m_static_send_date, 0, wx.ALL, 5)

        self.var_email_read_sent_on = wx.StaticText(self.EmailRead, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0)
        self.var_email_read_sent_on.Wrap(-1)
        EmailReadProperties.Add(self.var_email_read_sent_on, 0, wx.ALL, 5)

        self.m_static_files = wx.StaticText( self.EmailRead, wx.ID_ANY, u"Attached files:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_files.Wrap( -1 )
        EmailReadProperties.Add( self.m_static_files, 0, wx.ALL, 5 )

        self.var_email_file_count = wx.StaticText( self.EmailRead, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.var_email_file_count.Wrap( -1 )
        EmailReadProperties.Add( self.var_email_file_count, 0, wx.ALL, 5 )

        EmailReadSizer.Add(EmailReadProperties, 0, wx.EXPAND, 5)

        self.m_staticline17 = wx.StaticLine(self.EmailRead, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        EmailReadSizer.Add(self.m_staticline17, 0, wx.EXPAND | wx.ALL, 5)

        self.EmailReadScroll = wx.ScrolledWindow(self.EmailRead, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 400), wx.HSCROLL | wx.VSCROLL)
        self.EmailReadScroll.SetScrollRate(5, 5)
        EmailContentSizer = wx.BoxSizer( wx.VERTICAL )

        EmailContentSizer.SetMinSize( wx.Size( -1,400 ) ) 
        self.var_read_email_content = wx.StaticText( self.EmailReadScroll, wx.ID_ANY, u"", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.var_read_email_content.Wrap( 930 )
        EmailContentSizer.Add( self.var_read_email_content, 1, wx.ALL, 5 )

        self.EmailReadScroll.SetSizer( EmailContentSizer )
        self.EmailReadScroll.Layout()
        EmailReadSizer.Add( self.EmailReadScroll, 1, wx.EXPAND |wx.ALL, 5 )

        self.m_staticline21 = wx.StaticLine( self.EmailRead, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        EmailReadSizer.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )

        EmailReadButtonSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.button_email_close = wx.Button( self.EmailRead, wx.ID_ANY, u"Close email", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Bind(wx.EVT_BUTTON, self.OnEmailButton, self.button_email_close)
        EmailReadButtonSizer.Add( self.button_email_close, 0, wx.ALL, 5 )

        self.button_email_read = wx.Button( self.EmailRead, wx.ID_ANY, u"TTS Reader", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Bind(wx.EVT_BUTTON, self.OnEmailButton, self.button_email_read)
        EmailReadButtonSizer.Add( self.button_email_read, 0, wx.ALL, 5 )
        
        EmailReadSizer.Add( EmailReadButtonSizer, 0, wx.EXPAND, 5 )

        self.m_staticline22 = wx.StaticLine( self.EmailRead, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        EmailReadSizer.Add( self.m_staticline22, 0, wx.EXPAND |wx.ALL, 5 )

        self.EmailRead.SetSizer( EmailReadSizer )
        self.EmailRead.Layout()
        EmailPanelSizer.Add( self.EmailRead, 1, wx.EXPAND |wx.ALL, 5 )

        self.SetSizer( EmailPanelSizer )
        ######################################### STATIC UI #####################################

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Layout()
        EmailPanelSizer.Fit( self )

    def OnSearch(self, event):
        """
        Initiates a full_text call to Gmail API to get the emails in JSON format
        Then calls FetchEmailData(email_data)
        """
        obj = event.EventObject
        self.selected_labels = self.email_labels.GetSelections()
        self.query = self.email_search.GetValue()
        max_count_index = self.email_results_count.GetSelection()
        self.max_count = int(self.email_results_count.GetString(max_count_index))

        self.timer.Start(59000)

        labels = []

        for i in self.selected_labels:
            labels.append(self.email_labelsChoices[i])


        if self.query != "" and self.query != None:
            self.query = self.QUERY_OPTION  + " " + self.query
        else:
            self.query = self.QUERY_OPTION
            
        if self.HasInternet():
            emailInfo = GmailApi(labels, self.query, self.max_count)
            emailInfo.InitiateCredentials()
        
            self.email_data = emailInfo.GmailApiCall()

            if self.email_data != False :
                self.FetchEmailData(self.email_data)
            # else:
            #     wx.MessageBox("No messages found.", "Error. No data.")

            del emailInfo
        else:
            wx.MessageBox("There's no internet connection.", "Error. No Internet")

    def OnUpdate(self, event):
        """
        Used by the timer object to periodically make a minimal_text call to
        GmailAPI and compares the local history_id state to the one in the reply.
        Informs the user if there's a new email or a need to resync.
        After user's consent updates the UI and local history_id
        """
        try:
            _stored_history_id = self.get_history_id_db_email_table()

            _search_value = self.email_search.GetValue()
            _query = ""
            _selected_labels = self.email_labels.GetSelections()
            _max_count = 1
            _labels = []

            if _search_value != "" and _search_value != None:
                _query = self.QUERY_OPTION + " " + _search_value
            else:
                _query = self.QUERY_OPTION

            for i in _selected_labels:
                _labels.append(self.email_labelsChoices[i])

            if self.HasInternet():
                emailMinimalInfo = GmailApi(_labels, _query, _max_count)
                emailMinimalInfo.InitiateCredentials()
        
                _email_data = emailMinimalInfo.GmailMinimalApiCall()

                if _email_data != False :
                    
                    fetched_id = _email_data[0]['historyId']

                    if fetched_id != _stored_history_id:
                        self.truncate_db_email_table("email_history")
                        self.update_db_email_table(fetched_id)

                        msg_dialog_option = wx.MessageBox("You have a new email or your app is out of sync.\nPress OK to resync your app.", "Resync", wx.OK)
                        
                        if msg_dialog_option == wx.OK:
                            refresh_evt = wx.PyCommandEvent(wx.EVT_SEARCHCTRL_SEARCH_BTN.typeId, self.email_search.GetId())
                            wx.PostEvent(self.email_search, refresh_evt)

                else:
                    wx.MessageBox("No messages found.", "Error. No data.")

                del emailMinimalInfo
            else:
                wx.MessageBox("There's no internet connection.", "Error.No Internet")

        except Exception as e:
            wx.MessageBox(str(e), "Error while fetching stored Email history")

    def HasInternet(self):
        """
        Checks for an Internet connection
        return : True - If there's internet connection
        return : False - If there's no internet connection
        """
        try:
            socket.create_connection(("www.abv.bg", 80))
            return True
        except OSError:
            return False

    def FetchEmailData(self, data):
        """
        Receives its data from OnSearch(self, event).
        Fetches the data from the JSON and updates
        all email objects and stored history_id
        Calls populateUi(self, email_objects)
        """
        if len(self.email_obj_list) > 0:
            self.email_obj_list.clear()

        latest_histor_id = ""

        for history_id in data:
            latest_histor_id = history_id["historyId"]
            break

        self.truncate_db_email_table("email_history")
        self.update_db_email_table(latest_histor_id)
        
        for item in data:
            headers = item["payload"]["headers"]

            email = EmailData()

            for header in headers:
                if header["name"] == "Date":
                   email.set_sent_date(header["value"])

                if header["name"] == "Subject":
                   email.set_subject(header["value"])

                if header["name"] == "From":
                   email.set_sent_from(header["value"])

                if header["name"] == "To":
                   email.set_sent_to(header["value"])


            if "parts" in item["payload"]:
                   

               bodyParts = item["payload"]["parts"]

               for bodyPart in bodyParts:
                     if bodyPart["mimeType"] == "multipart/alternative":
                           parts = bodyPart["parts"]
                           
                           for part in parts:
                                    if part["mimeType"] == "text/plain":
                                       body_data = bytes(str(part["body"]["data"]), encoding = "utf-8")
                                       decode = base64.urlsafe_b64decode(body_data).decode("utf-8")
                                       email.set_mail_text(decode)

                     if bodyPart["mimeType"] == "image/png":
                         email.set_file_name(bodyPart["filename"])
                     
                     elif bodyPart["mimeType"] == "text/plain":
                            body_data = bytes(str(bodyPart["body"]["data"]), encoding = "utf-8")
                            decode = base64.urlsafe_b64decode(body_data).decode("utf-8")
                            email.set_mail_text(decode)

            self.email_obj_list.append(email)
            del email

        if self.EmailListSizer.GetItemCount() > 0:
            self.EmailListSizer.Clear(delete_windows=True)
            self.populateUi(self.email_obj_list)
        else:
            self.populateUi(self.email_obj_list)

    def populateUi(self, email_objects):
        """
        Goes through the list of EmailData objects and their properties
        and updates the UI by adding list item for each email
        """
        ind = 0

        for email in email_objects:

            ind = ind + 1

            self.EmailListItem = wx.Panel(self.EmailList, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
            EmailListItemSizer = wx.BoxSizer(wx.HORIZONTAL)

            self.var_email_sender = wx.StaticText(self.EmailListItem, wx.ID_ANY, email.get_sent_from(), wx.DefaultPosition, wx.Size(200, -1), 0)
            self.var_email_sender.Wrap(200)
        
            self.var_email_sender.SetMaxSize(wx.Size(200, -1))

            EmailListItemSizer.Add(self.var_email_sender, 0, wx.ALIGN_CENTER | wx.ALL, 5)

            self.m_staticline37 = wx.StaticLine(self.EmailListItem, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
            EmailListItemSizer.Add(self.m_staticline37, 0, wx.EXPAND | wx.ALL, 5)

            self.var_email_receiver = wx.StaticText(self.EmailListItem, wx.ID_ANY, email.get_sent_to(), wx.DefaultPosition, wx.Size(200, -1), 0)
            self.var_email_receiver.Wrap(200)

            EmailListItemSizer.Add(self.var_email_receiver, 0, wx.ALIGN_CENTER | wx.ALL, 5)

            self.m_staticline38 = wx.StaticLine(self.EmailListItem, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
            EmailListItemSizer.Add(self.m_staticline38, 0, wx.EXPAND | wx.ALL, 5)

            self.var_email_subject = wx.StaticText(self.EmailListItem, wx.ID_ANY, email.get_subject(), wx.DefaultPosition, wx.Size(200, -1), 0)
            self.var_email_subject.Wrap(200)

            EmailListItemSizer.Add(self.var_email_subject, 0, wx.ALIGN_CENTER | wx.ALL, 5)

            self.m_staticline391 = wx.StaticLine(self.EmailListItem, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
            EmailListItemSizer.Add(self.m_staticline391, 0, wx.EXPAND | wx.ALL, 5)

            self.var_email_date = wx.StaticText(self.EmailListItem, wx.ID_ANY, email.get_sent_date(), wx.DefaultPosition, wx.Size(150, -1), 0)
            self.var_email_date.Wrap(150)

            EmailListItemSizer.Add(self.var_email_date, 0, wx.ALIGN_CENTER | wx.ALL, 5)

            self.m_staticline40 = wx.StaticLine(self.EmailListItem, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
            EmailListItemSizer.Add(self.m_staticline40, 0, wx.EXPAND | wx.ALL, 5)

            self.button_email = wx.Button(self.EmailListItem, wx.ID_ANY, "Read {0}".format(ind), wx.DefaultPosition, wx.DefaultSize, 0)
            self.button_email.Bind(wx.EVT_BUTTON, self.OnReadButton)
            EmailListItemSizer.Add(self.button_email, 0, wx.ALL, 5)

            self.EmailListItem.SetSizer(EmailListItemSizer)
            self.EmailListItem.Layout()
            EmailListItemSizer.Fit(self.EmailListItem)
            self.EmailListSizer.Add(self.EmailListItem, 0, wx.ALL | wx.EXPAND, 0)
            self.EmailListSizer.Layout()

        self.EmailList.Layout()
        self.Layout()

    def OnReadButton(self, event):
        """
        When a read button from an email list item is clicked,
        all the data for this email is fetched from the app runtime memory
        to populate the detailed email read window.
        """
        btn = event.EventObject
        index = int(btn.GetLabel().split(" ")[1]) - 1

        try:
            email = self.email_obj_list[index]

            self.var_email_read_title.SetLabel(email.get_subject())
            self.var_email_read_sender.SetLabel(email.get_sent_from())
            self.var_email_read_sent_on.SetLabel(email.get_sent_date())
            self.var_email_file_count.SetLabel(email.get_file_name())
            self.var_read_email_content.SetLabel(email.get_mail_text())

            self.last_msg_text = email.get_mail_text()

            self.EmailRead.Layout()

        except IndexError:
            wx.MessageBox("There was an error while loading this message. Please reload the page.", "Error. Could not load.")

    def OnEmailButton(self, event):
        """
        Called by detailed email button controls. Either clears the email window
        or calls for a TTS object. Depending on the pressed button
        """
        btn = event.EventObject

        if btn is self.button_email_close:
            self.var_email_read_title.SetLabel("")
            self.var_email_read_sender.SetLabel("")
            self.var_email_read_sent_on.SetLabel("")
            self.var_email_file_count.SetLabel("")
            self.var_read_email_content.SetLabel("")

            self.last_msg_text = None

            try:
                self.tts.Stop()
                del self.tts
            except:
                pass

            self.EmailRead.Layout()

        elif btn is self.button_email_read:
            try:
                self.tts = TextToSpeech(self, self.last_msg_text)
                self.tts.Play()
            except:
                wx.MessageBox("No message to be played.", "Warning")

    def truncate_db_email_table(self, table_name):
        """
        Method to clear the history_id DB table when needed
        """
        try:
            db_cursor = self.db_conn.cursor()
            db_cursor.execute("DELETE FROM {}".format(table_name))
            self.db_conn.commit()
        except Exception as e:
            wx.MessageBox(str(e), "Error while truncating DB")

    def update_db_email_table(self, history_id):
        """
        Method to update the email table. Primarily when the 
        local history_id is to be updated
        """
        try:
            db_cursor = self.db_conn.cursor()
            db_cursor.execute("INSERT INTO email_history VALUES ({})".format(history_id))
            self.db_conn.commit()
        except Exception as e:
            wx.MessageBox(str(e), "Error while writing to DB")

    def get_history_id_db_email_table(self):
        """
        Method to retrieve the stored history_id
        return : str - Success
        return : false - Fail
        """
        try:
            db_cursor = self.db_conn.cursor()
            db_cursor.execute("SELECT history_id FROM email_history WHERE rowid = 1")
            db_return = db_cursor.fetchall()

            if len(db_return) > 0:
                history_id = None
                for data in db_return:
                    history_id = list(data)[0]
                    break
                return history_id
            else:
                return False
        except Exception as e:
            wx.MessageBox(str(e), "Error while fetching stored history_id")



    def OnClose(self, event):
        """
        Destroys the window on its closing and stops the TTS reader if it's running
        """
        try:
            self.tts.Stop()
            del self.tts
        except:
            pass
        self.Destroy()
