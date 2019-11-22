import wx
import twitter

class Tweeter( object ):
    """
    A class to initiate a connection to Twitter API
    ...
    Attributes:
    CONSUMER_KEY : str
        The consumer key, provided by Twitter API
    CONSUMER_SECRET : str
        The consumer secret, provided by Twitter API
    ACCESS_TOKEN_KEY : str
        The access token key, provided by the API
    ACCESS_TOKEN_SECRET : str
        The access token key, provided by the API
    twt : twitter.Api
        An instance of twitter.Api() to connect to the API
    ...
    Methods:
    init(self)
        Initiates a connection to Twitter
    GetInstance(self)
        Returns reference to the active twitter.Api() instance 
    """
    def __init__(self):
        self.CONSUMER_KEY = ''
        self.CONSUMER_SECRET = ''

        self.ACCESS_TOKEN_KEY = ''
        self.ACCESS_TOKEN_SECRET = ''

        self.twt = None

    def init(self):
        """Initiates a connection to Twitter"""
        try:
            self.twt = twitter.Api(self.CONSUMER_KEY, self.CONSUMER_SECRET, self.ACCESS_TOKEN_KEY, self.ACCESS_TOKEN_SECRET, sleep_on_rate_limit = True)
        except Exception as e:
            wx.MessageBox(str(e), "Error")

    def GetInstance(self):
        """Returns reference to the active twitter.Api() instance"""
        return self.twt

    def __del__(self):
        del self