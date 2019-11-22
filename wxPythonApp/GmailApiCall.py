from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import re

class GmailApi(object):
    """
    A class to make GET calls to Gmail API
    ...
    Attributes:
    SCOPES : str
        The scopes of the app for the Gmail API
        /only can read/
    labelIds : list
        The provided list of labels by the invoking class
    q : str
        The query paramenters to be send to Gmail API
    maxResults : str
        The maximum number of results that can be returned
        by GmailAPI
    service : Gmail API service
        Initiates a connection to Gmail API
    messeged_list : list
        A list where all the JSON responses, containing the email
        data, from the API are stored
    ...
    Methods:
    InitiateCredentials(self)
        Initiates an oauth2 handshake dance with Gmail API to set user's credentials
        if they are not existing yet or to authenticate the user if there is already
        a token.json file
    GmailApiCall(self)
        Makes a full_text call to Gmail API and returns a list, containing all email
        data in JSON
        return : list - success
        return : False - fail
    GmailMinimalApiCall(self)
        Makes a minimal_text call to Gmail API and returns a list, containing minimal
        information in JSON, like history_id. Used for syncing only.
        return : list - success
        return : False - fail
    """

    def __init__(self, labelIds, query, maxResults):

        self.SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

        self.labelIds = labelIds
        self.q = query
        self.maxResults = maxResults

        self.service = ""

        self.messages_list = []

    def __del__(self):
        del self

    def InitiateCredentials(self):
        """
        Initiates an oauth2 handshake dance with Gmail API to set user's credentials
        if they are not existing yet or to authenticate the user if there is already
        a token.json file
        """
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', self.SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('gmail', 'v1', http=creds.authorize(Http()))

    def GmailApiCall(self):
        """
        Makes a full_text call to Gmail API and returns a list, containing all email
        data in JSON
        return : list - success
        return : False - fail
        """
        results = self.service.users().messages().list(userId='me',labelIds = self.labelIds, q = self.q, maxResults = self.maxResults).execute()
        messages = results.get('messages', [])

        if messages:
            for message in messages:
                msg = self.service.users().messages().get(userId='me', id=message['id'], format='full').execute()
                self.messages_list.append(msg)
            return self.messages_list
        else:
            return False

    def GmailMinimalApiCall(self):
        """
        Makes a minimal_text call to Gmail API and returns a list, containing minimal
        information in JSON, like history_id. Used for syncing only.
        return : list - success
        return : False - fail
        """
        results = self.service.users().messages().list(userId='me',labelIds = self.labelIds, q = self.q, maxResults = self.maxResults).execute()
        messages = results.get('messages', [])

        if messages:
            for message in messages:
                msg = self.service.users().messages().get(userId='me', id=message['id'], format='minimal').execute()
                self.messages_list.append(msg)
            return self.messages_list
        else:
            return False