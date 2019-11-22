import time
import facebook
import requests
import wx

class FbApi( object ):
    """
    A class to make GET calls to the Facebook API calls
    ...
    Attributes:
    APP_ID [constant] : str
        app_id for FB API
    APP_SECRET [constant] : str
        app_secret for FB API
    USER_TOKEN_SHORT [constant] : str
        Short term token from FB Graph
    ACCESS_TOKEN_URL : str
        URL to Graph API to get a long term token
    graph : facebook.GraphAPI
        An instant to connect to FB Graph API
    ...
    Methods:
    initialize_only(self)
        Only initializes a connection to FB Graph API
    get_fb_info(self)
        Makes a call to Graph API and returns the user's info
        return : JSON
    get_fb_connections(self, id : str, msg : str):
        Used to get items (comments, likes, reactions) connected to main objects (user, pages, post)
        from Graph API.
        return : JSON
    put_fb_object(self, id : str, msg : str):
        Used to put or post to an object in Graph API. Works only if the application is permitted
        by FB to post or put to the Graph API.
    """
    def __init__(self):
        APP_ID = ''
        APP_SECRET = ''
        USER_TOKEN_SHORT = ''
        self.ACCESS_TOKEN_URL = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}'.format(APP_ID, APP_SECRET, USER_TOKEN_SHORT)
        self.graph = None

    def initialize_only(self):
        """Only initializes a connection to FB Graph API"""
        try:
            req = requests.get(self.ACCESS_TOKEN_URL)
            access_token_info = req.json()
            token = access_token_info['access_token']

            self.graph = facebook.GraphAPI(access_token = token, version = "2.12")
        except Exception as e:
            wx.MessageBox(str(e), "Error")


    def get_fb_info(self):
        """
        Makes a call to Graph API and returns the user's info
        return : JSON
        """
        try:
            req = requests.get(self.ACCESS_TOKEN_URL)
            access_token_info = req.json()
            token = access_token_info['access_token']

            self.graph = facebook.GraphAPI(access_token = token, version = "2.12")
            profile = self.graph.get_object(id = 'me')

            _fields = ['name,email,posts,likes,friends']
            fb_info = self.graph.get_object(id = 'me', fields = _fields)

            return fb_info
        except Exception as e:
            wx.MessageBox(str(e), "Error")

    def get_fb_connections(self, _id, _connection_name):
        """
        Used to get items (comments, likes, reactions) connected to main objects (user, pages, post)
        from Graph API.
        return : JSON
        """
        return self.graph.get_connections(_id, connection_name = _connection_name)

    def put_fb_object(self, _id, _msg):
        """
        Used to put or post to an object in Graph API. Works only if the application is permitted
        by FB to post or put to the Graph API.
        """
        try:
            self.graph.put_object(parent_object = _id, connection_name = 'feed', message = _msg)
        except Exception as e:
            wx.MessageBox(str(e), "Error")

    def __del__(self):
        del self
