import wx
import socket
from TweeterApiCall import Tweeter
import webbrowser

class Tweet( object ):
    """
    A simple custom object to store the data of a tweet
    ...
    Attributes:
    tweet_id : str
        The tweet's id
    posted_by : str
        The name of the person who posted it
    tweet_date : str
        The date of creattion of the tweet
    tweet_likes : int
        The number of likes the tweet has
    tweet_retweeted : int
        The number of times the tweet was retweeted
    tweet_text : str
        The text of a tweet
    retweet_text : str
        The text of the retweet
    ...
    Methods:
    SetTweetId(self, _id : str)
        Sets the id of the tweet
    GetTweetId(self)
        Returns the id of the tweet
        return : str
    SetPostedBy(self, _posted_by : str)
        Sets the name of the author of the tweet
    GetPostedBy(self)
        Returns the names of the author of the tweet
        return : str
    SetPostedByScrnName(self, _scrn_name : str)
        Sets the screen name of the author of the tweet
    GetPostedByScrnName(self)
        Returns the screen name of the author of the tweet
        return : str
    SetTweetDate(self, _date : str)
        Sets the date of creation of the tweet
    GetTweetDate(self)
        Returns the date of creation of the tweet
        return : str
    SetTweetLikes(self, _likes : int)
        Sets the number of likes the tweet has
    GetTweetLikes(self)
        Returns the number of likes the tweet has
        return : int
    SetRetweets(self, _retweets : int)
        Sets the number of retweets the tweet has
    GetRetweets(self)
        Returns the number of retweets the tweet has
        return : int
    SetTweetText(self, _txt : str)
        Sets the text of the tweet
    GetTweetText(self)
        Returns the text of the tweet
        return : str
    SetRetweetText(self, _retweet_text : str)
        Sets the text of the retweet
    GetRetweetText(self)
        Returns the text of the retweet
        return : text
    """
    def __init__(self):
        self.tweet_id = ""
        self.posted_by = ""
        self.posted_by_scrn_name = ""
        self.tweet_date = ""
        self.tweet_likes = 0
        self.tweet_retweeted = 0
        self.tweet_text = ""
        self.retweet_text = None

    def SetTweetId(self, _id):
        """Sets the id of the tweet"""
        self.tweet_id = _id

    def GetTweetId(self):
        """
        Returns the id of the tweet
        return : str
        """
        return self.tweet_id

    def SetPostedBy(self, _posted_by):
        """Sets the name of the author of the tweet"""
        self.posted_by = _posted_by

    def GetPostedBy(self):
        """
        Returns the names of the author of the tweet
        return : str
        """
        return self.posted_by

    def SetPostedByScrnName(self, _scrn_name):
        """Sets the screen name of the author of the tweet"""
        self.posted_by_scrn_name = _scrn_name

    def GetPostedByScrnName(self):
        """
        Returns the screen name of the author of the tweet
        return : str
        """
        return self.posted_by_scrn_name

    def SetTweetDate(self, _date):
        """Sets the date of creation of the tweet"""
        self.tweet_date = _date

    def GetTweetDate(self):
        """
        Returns the date of creation of the tweet
        return : str
        """
        return self.tweet_date

    def SetTweetLikes(self, _likes):
        """
        Sets the number of likes the tweet has
        """
        self.tweet_likes = _likes

    def GetTweetLikes(self):
        """
        Returns the number of likes the tweet has
        return : int
        """
        return self.tweet_likes

    def SetRetweets(self, _retweets):
        """Sets the number of retweets the tweet has"""
        self.tweet_retweeted = _retweets

    def GetRetweets(self):
        """
        Returns the number of retweets the tweet has
        return : int
        """
        return self.tweet_retweeted

    def SetTweetText(self, _txt):
        """Sets the text of the tweet"""
        self.tweet_text = _txt

    def GetTweetText(self):
        """
        Returns the text of the tweet
        return : str
        """
        return self.tweet_text

    def SetRetweetText(self, _retweet_text):
        """Sets the text of the retweet"""
        self.retweet_text = _retweet_text

    def GetRetweetText(self):
        """
        Returns the text of the retweet
        return : text
        """
        return self.retweet_text

    def __del__(self):
        del self

class Twitter_panel( wx.Panel ):
    """
    This class inherits from wx.Panel and is used to store the information of the auth. Twitter user in the app
    ...
    Attributes:
    user_tweet_list : list
        Stores Tweet() objects, created by the user
    home_tweet_list : list
        Stores Tweet() objects from users' home, i.e.
        created by other people or pages
    m_followers_choiceChoices : list
        List with the names of followers of the user
    m_following_choiceChoices : list
        List with the names of the people the user is following
    var_user_followers : str
        The number of followers the user has. UI element
    var_user_following : str
        The number of users the user is following. UI element
    var_user_posts : str
        The number of tweets the user has. UI element
    m_followers_choice : wx.Choice
        The dropdown with the names of the followers
    m_following_choice : wx.Choice
        The dropdown with the names of the people the user is following
    btn_usr_tweet : wx.Button
        Calls the OnTweet(self, event) and posts the tweet of the user
        when pressed
    btn_usr_reload : wx.Button
        Calls the OnReload(self, event) method and completely reloads the UI
        when pressed
    ...
    Methods:
    OnReload(self, event)
        If there's internet, tries to initiate a Tweeter API connector
        instance.
        Then calls the SetUserPage(self, twt) method and passes a reference
        to it
    SetUserPage(self, twt : Tweet)
        Gets the followers, following, tweets, timeline of the user, updates and
        populates the UI. Goes through all returned objects and fetches the information
        from them and saves it in the corresponding data structure.
        ...
        Calls on methods:
        SetUserPosts(user_tweet_list)
        SetTimelinePosts(home_tweet_list)
    SetUserPosts(self, user_tweet_list)
        Goes through all the tweets of the user. For each tweet it fetches its data
        and populates it to the corresponding location in the tweet list item.
        Then adds the tweet list item to the user tweet list
    SetTimelinePosts(self, home_tweet_list)
        Goes through all the tweets on user's home. For each tweet it fetches its data
        and populates it to the corresponding location in the home tweet list item.
        Then adds the home tweet list item to the home tweet list
    OnHomePostBtnPress(self, event)
        When invoked by the Read button of a tweet, this method will get the id of the tweet and the screen name of the author in order for the
        tweet URL to be built and then loaded into a web browser.
        When invoked by the Retweet button of a tweet, this method will get the id of the tweet and will
        post it to user's twitter are a retweet.
        ...
        In both cases makes a full UI reload.
    OnSearch(self, event)
        Searches for a page or a person with a query parameter provided by the user.
        The query URL is built and then opened in the browser
    OnTweet(self, event)
        Posts to Twitter API a new tweet provided by the user.
        Makes a full UI reload
    FormatDate(self, date)
        Formats the date from an ISO format to the format needed in the app
        and returns it
        return : str
    HasInternet(self)
        Checks if there an active internet connection
        return : True - there's internet
        return : False - there's no internet
    """
    def __init__(self, parent):
        super(Twitter_panel, self).__init__( parent = parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.TAB_TRAVERSAL)

        self.user_tweet_list = []
        self.home_tweet_list = []
        self.m_followers_choiceChoices = []
        self.m_following_choiceChoices = []
        
        #################################### STATIC UI ####################################
        Twitter_panel_sizer = wx.BoxSizer( wx.VERTICAL )

        self.Twitter_options = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL )
        Twitter_options_sizer = wx.BoxSizer( wx.HORIZONTAL )

        self.m_static_search = wx.StaticText( self.Twitter_options, wx.ID_ANY, u"Search people or pages:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_search.Wrap( -1 )
        Twitter_options_sizer.Add( self.m_static_search, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.search_twitter = wx.SearchCtrl( self.Twitter_options, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.search_twitter.ShowSearchButton( True )
        self.search_twitter.ShowCancelButton( False )
        self.search_twitter.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearch)
        Twitter_options_sizer.Add( self.search_twitter, 0, wx.ALL, 5 )


        self.Twitter_options.SetSizer( Twitter_options_sizer )
        self.Twitter_options.Layout()
        Twitter_options_sizer.Fit( self.Twitter_options )
        Twitter_panel_sizer.Add( self.Twitter_options, 0, wx.EXPAND |wx.ALL, 0 )

        Twitter_home_content = wx.BoxSizer( wx.HORIZONTAL )

        home_content_sizer = wx.BoxSizer( wx.VERTICAL )

        self.home_content_scroll = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.SUNKEN_BORDER|wx.VSCROLL )
        self.home_content_scroll.SetScrollRate( 5, 5 )
        self.home_content_scroll.SetMinSize(wx.Size(500, -1))
        self.home_content_list = wx.BoxSizer( wx.VERTICAL )

        self.home_content_scroll.SetSizer( self.home_content_list )
        self.home_content_scroll.Layout()
        self.home_content_list.Fit( self.home_content_scroll )
        home_content_sizer.Add( self.home_content_scroll, 1, wx.EXPAND |wx.ALL, 5 )

        Twitter_home_content.Add( home_content_sizer, 1, wx.EXPAND, 5 )

        user_content_sizer = wx.BoxSizer( wx.VERTICAL )

        self.user_info_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL )
        user_info_sizer = wx.BoxSizer( wx.HORIZONTAL )

        followers_sizer = wx.BoxSizer( wx.VERTICAL )

        self.m_static_followers = wx.StaticText( self.user_info_panel, wx.ID_ANY, u"Followers:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_followers.Wrap( -1 )
        followers_sizer.Add( self.m_static_followers, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.var_user_followers = wx.StaticText( self.user_info_panel, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.var_user_followers.Wrap( -1 )
        followers_sizer.Add( self.var_user_followers, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        user_info_sizer.Add( followers_sizer, 1, wx.EXPAND, 5 )

        self.m_staticline113 = wx.StaticLine( self.user_info_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        user_info_sizer.Add( self.m_staticline113, 0, wx.EXPAND |wx.ALL, 5 )

        following_sizer = wx.BoxSizer( wx.VERTICAL )

        self.m_static_following = wx.StaticText( self.user_info_panel, wx.ID_ANY, u"Following:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_following.Wrap( -1 )
        following_sizer.Add( self.m_static_following, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.var_user_following = wx.StaticText( self.user_info_panel, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.var_user_following.Wrap( -1 )
        following_sizer.Add( self.var_user_following, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        user_info_sizer.Add( following_sizer, 1, wx.EXPAND, 5 )

        self.m_staticline1131 = wx.StaticLine( self.user_info_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        user_info_sizer.Add( self.m_staticline1131, 0, wx.EXPAND |wx.ALL, 5 )

        posts_sizer = wx.BoxSizer( wx.VERTICAL )

        self.m_static_posts = wx.StaticText( self.user_info_panel, wx.ID_ANY, u"Tweets:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_posts.Wrap( -1 )
        posts_sizer.Add( self.m_static_posts, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.var_user_posts = wx.StaticText( self.user_info_panel, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.var_user_posts.Wrap( -1 )
        posts_sizer.Add( self.var_user_posts, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        user_info_sizer.Add( posts_sizer, 1, wx.EXPAND, 5 )

        self.m_staticline1132 = wx.StaticLine( self.user_info_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        user_info_sizer.Add( self.m_staticline1132, 0, wx.EXPAND |wx.ALL, 5 )

        followers_list_sizer = wx.BoxSizer( wx.VERTICAL )

        self.m_static_followers_list = wx.StaticText( self.user_info_panel, wx.ID_ANY, u"Followers:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_followers_list.Wrap( -1 )
        followers_list_sizer.Add( self.m_static_followers_list, 0, wx.ALL, 5 )

        self.m_followers_choice = wx.Choice( self.user_info_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.m_followers_choiceChoices, 0 )
        self.m_followers_choice.SetSelection( 0 )
        followers_list_sizer.Add( self.m_followers_choice, 0, wx.ALL, 5 )

        user_info_sizer.Add( followers_list_sizer, 1, wx.EXPAND, 5 )

        self.m_staticline1133 = wx.StaticLine( self.user_info_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        user_info_sizer.Add( self.m_staticline1133, 0, wx.EXPAND |wx.ALL, 5 )

        following_list_sizer = wx.BoxSizer( wx.VERTICAL )

        self.m_static_following_list = wx.StaticText( self.user_info_panel, wx.ID_ANY, u"Following:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_following_list.Wrap( -1 )
        following_list_sizer.Add( self.m_static_following_list, 0, wx.ALL, 5 )

        self.m_following_choice = wx.Choice( self.user_info_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.m_following_choiceChoices, 0 )
        self.m_following_choice.SetSelection( 0 )
        following_list_sizer.Add( self.m_following_choice, 0, wx.ALL, 5 )

        user_info_sizer.Add( following_list_sizer, 1, wx.EXPAND, 5 )

        self.user_info_panel.SetSizer( user_info_sizer )
        self.user_info_panel.Layout()
        user_info_sizer.Fit( self.user_info_panel )
        user_content_sizer.Add( self.user_info_panel, 0, wx.EXPAND |wx.ALL, 5 )

        self.user_ctrl_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        user_ctrl_sizer = wx.BoxSizer( wx.HORIZONTAL )

        self.btn_usr_tweet = wx.Button( self.user_ctrl_panel, wx.ID_ANY, u"Tweet", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btn_usr_tweet.Bind(wx.EVT_BUTTON, self.OnTweet)
        user_ctrl_sizer.Add( self.btn_usr_tweet, 1, wx.ALL, 5 )

        self.btn_usr_reload = wx.Button( self.user_ctrl_panel, wx.ID_ANY, u"Reload", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btn_usr_reload.Bind(wx.EVT_BUTTON, self.OnReload)
        user_ctrl_sizer.Add( self.btn_usr_reload, 1, wx.ALL, 5 )

        self.user_ctrl_panel.SetSizer( user_ctrl_sizer )
        self.user_ctrl_panel.Layout()
        user_ctrl_sizer.Fit( self.user_ctrl_panel )
        user_content_sizer.Add( self.user_ctrl_panel, 0, wx.EXPAND |wx.ALL, 5 )

        self.user_tweet_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL )
        user_tweet_sizer = wx.BoxSizer( wx.VERTICAL )

        self.user_tweet_txt_ctrl = wx.TextCtrl( self.user_tweet_panel, wx.ID_ANY, u"", wx.DefaultPosition, wx.Size( -1,200 ), wx.TE_MULTILINE )
        self.user_tweet_txt_ctrl.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
        self.user_tweet_txt_ctrl.SetMaxSize( wx.Size( -1,200 ) )
        user_tweet_sizer.Add( self.user_tweet_txt_ctrl, 1, wx.ALL|wx.EXPAND, 5 )

        self.user_tweet_panel.SetSizer( user_tweet_sizer )
        self.user_tweet_panel.Layout()
        user_tweet_sizer.Fit( self.user_tweet_panel )
        user_content_sizer.Add( self.user_tweet_panel, 0, wx.EXPAND |wx.ALL, 5 )

        self.user_feed_scroll = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.SUNKEN_BORDER|wx.VSCROLL )
        self.user_feed_scroll.SetScrollRate( 5, 5 )
        self.user_feed_list = wx.BoxSizer( wx.VERTICAL )

        self.user_feed_scroll.SetSizer( self.user_feed_list )
        self.user_feed_scroll.Layout()
        self.user_feed_list.Fit( self.user_feed_scroll )
        user_content_sizer.Add( self.user_feed_scroll, 1, wx.EXPAND |wx.ALL, 5 )

        Twitter_home_content.Add( user_content_sizer, 1, wx.EXPAND, 5 )

        Twitter_panel_sizer.Add( Twitter_home_content, 1, wx.EXPAND, 5 )

        self.SetSizer( Twitter_panel_sizer )
        self.Layout()
        Twitter_panel_sizer.Fit( self )
        self.Layout()
        #################################### STATIC UI ####################################

    def OnReload(self, event):
        """
        If there's internet, tries to initiate a Tweeter API connector
        instance.
        Then calls the SetUserPage(self, twt) method and passes a reference
        to it
        """
        if self.HasInternet():
            try:
                tweeter = Tweeter()
                tweeter.init()

                self.SetUserPage(tweeter.GetInstance())
            except Exception as e:
                wx.MessageBox(str(e), "Error fetching data")
        else:
            wx.MessageBox("No internet access", "Error")

    def SetUserPage(self, twt):
        """
        Gets the followers, following, tweets, timeline of the user, updates and
        populates the UI. Goes through all returned objects and fetches the information
        from them and saves it in the corresponding data structure.
        ...
        Calls on methods:
        SetUserPosts(user_tweet_list)
        SetTimelinePosts(home_tweet_list)
        """
        _followers = twt.GetFollowers()
        _following = twt.GetFriends()
        _tweets = twt.GetUserTimeline(trim_user=True)
        _timeline = twt.GetHomeTimeline(count = 30)

        followers_count = len(_followers)
        following_count = len(_following)
        tweets_count = len(_tweets)

        self.var_user_followers.SetLabel(str(followers_count))
        self.var_user_following.SetLabel(str(following_count))
        self.var_user_posts.SetLabel(str(tweets_count))

        if len(self.m_followers_choiceChoices) > 0:
            self.m_followers_choiceChoices.clear()

        if len(self.m_following_choiceChoices) > 0:
            self.m_following_choiceChoices.clear()

        if len(self.user_tweet_list) > 0:
            self.user_tweet_list.clear()

        if len(self.home_tweet_list) > 0:
            self.home_tweet_list.clear()

        if self.m_followers_choice.GetCount() > 0:
            self.m_followers_choice.Clear()

        if self.m_following_choice.GetCount() > 0:
            self.m_following_choice.Clear()

        for follower in _followers:
            self.m_followers_choiceChoices.append(follower.name)
            self.m_followers_choice.Append(follower.name)

        for following in _following:
            self.m_following_choiceChoices.append(following.name)
            self.m_following_choice.Append(following.name)

        for tweet in _tweets:
            tmp_tweet = Tweet()

            tmp_tweet.SetPostedBy(tweet.user.id)
            tmp_tweet.SetRetweets(str(tweet.retweet_count))
            tmp_tweet.SetTweetDate(str(tweet.created_at))
            tmp_tweet.SetTweetId(str(tweet.id))
            tmp_tweet.SetTweetLikes(str(tweet.favorite_count))
            tmp_tweet.SetTweetText(str(tweet.text))

            self.user_tweet_list.append(tmp_tweet)

        for timeline_post in _timeline:
            tmp_home_tweet = Tweet()

            tmp_home_tweet.SetPostedBy(timeline_post.user.name)
            tmp_home_tweet.SetPostedByScrnName(timeline_post.user.screen_name)
            tmp_home_tweet.SetRetweets(str(timeline_post.retweet_count))
            tmp_home_tweet.SetTweetDate(self.FormatDate(timeline_post.created_at))
            tmp_home_tweet.SetTweetId(timeline_post.id)
            tmp_home_tweet.SetTweetLikes(str(timeline_post.favorite_count))
            tmp_home_tweet.SetTweetText(timeline_post.text)

            retweet = timeline_post.retweeted_status
            if retweet and retweet != None:
                try:
                    tmp_home_tweet.SetTweetDate(self.FormatDate(retweet.created_at))
                    if retweet.quoted_status:
                        tmp_home_tweet.SetRetweetText(retweet.quoted_status.text)
                        tmp_home_tweet.SetPostedBy(retweet.quoted_status.user.name)
                        tmp_home_tweet.SetPostedByScrnName(retweet.quoted_status.user.screen_name)
                    tmp_home_tweet.SetTweetLikes(retweet.favorite_count)
                except Exception as e:
                    wx.MessageBox(str(e), "Error")

            self.home_tweet_list.append(tmp_home_tweet)

        self.SetUserPosts(self.user_tweet_list)
        self.SetTimelinePosts(self.home_tweet_list)

    def SetUserPosts(self, _tweet_list):
        """
        Goes through all the tweets of the user. For each tweet it fetches its data
        and populates it to the corresponding location in the tweet list item.
        Then adds the tweet list item to the user tweet list
        """
        if self.user_feed_list.GetItemCount() > 0:
            self.user_feed_list.Clear(delete_windows=True)

        for tweet in _tweet_list:
            self.user_feed_list_item = wx.Panel( self.user_feed_scroll, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL )
            user_feed_item_sizer = wx.BoxSizer( wx.VERTICAL )

            feed_item_txt_sizer = wx.BoxSizer( wx.VERTICAL )

            self.feed_item_txt_scroll = wx.ScrolledWindow( self.user_feed_list_item, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,125 ), wx.HSCROLL|wx.SUNKEN_BORDER|wx.VSCROLL )
            self.feed_item_txt_scroll.SetScrollRate( 5, 5 )
            self.feed_item_txt_scroll.SetMinSize( wx.Size( -1,125 ) )
            self.feed_item_txt_scroll.SetMaxSize( wx.Size( -1,125 ) )

            feed_txt_sizer = wx.BoxSizer( wx.VERTICAL )

            self.var_user_tweet_text = wx.StaticText( self.feed_item_txt_scroll, wx.ID_ANY, tweet.GetTweetText(), wx.DefaultPosition, wx.DefaultSize, 0 )
            self.var_user_tweet_text.Wrap( 400 )

            feed_txt_sizer.Add( self.var_user_tweet_text, 0, wx.ALL|wx.EXPAND, 5 )

            self.feed_item_txt_scroll.SetSizer( feed_txt_sizer )
            self.feed_item_txt_scroll.Layout()
            feed_item_txt_sizer.Add( self.feed_item_txt_scroll, 1, wx.ALL|wx.EXPAND, 5 )

            user_feed_item_sizer.Add( feed_item_txt_sizer, 0, wx.ALL|wx.EXPAND, 5 )

            feed_item_meta_sizer = wx.BoxSizer( wx.HORIZONTAL )

            self.m_static_posted_on = wx.StaticText( self.user_feed_list_item, wx.ID_ANY, u"Posted On:", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.m_static_posted_on.Wrap( -1 )

            feed_item_meta_sizer.Add( self.m_static_posted_on, 0, wx.ALL, 5 )

            self.var_user_tweet_posted = wx.StaticText( self.user_feed_list_item, wx.ID_ANY, self.FormatDate(tweet.GetTweetDate()), wx.DefaultPosition, wx.DefaultSize, 0 )
            self.var_user_tweet_posted.Wrap( -1 )

            feed_item_meta_sizer.Add( self.var_user_tweet_posted, 0, wx.ALL, 5 )

            self.m_staticline1091 = wx.StaticLine( self.user_feed_list_item, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
            feed_item_meta_sizer.Add( self.m_staticline1091, 0, wx.EXPAND |wx.ALL, 5 )

            self.m_static_likes = wx.StaticText( self.user_feed_list_item, wx.ID_ANY, u"Likes:", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.m_static_likes.Wrap( -1 )

            feed_item_meta_sizer.Add( self.m_static_likes, 0, wx.ALL, 5 )

            self.var_user_tweet_likes = wx.StaticText( self.user_feed_list_item, wx.ID_ANY, str(tweet.GetTweetLikes()), wx.DefaultPosition, wx.DefaultSize, 0 )
            self.var_user_tweet_likes.Wrap( -1 )

            feed_item_meta_sizer.Add( self.var_user_tweet_likes, 0, wx.ALL, 5 )

            self.m_staticline1101 = wx.StaticLine( self.user_feed_list_item, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
            feed_item_meta_sizer.Add( self.m_staticline1101, 0, wx.EXPAND |wx.ALL, 5 )

            self.m_static_user_retweets = wx.StaticText( self.user_feed_list_item, wx.ID_ANY, u"Retweets:", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.m_static_user_retweets.Wrap( -1 )

            feed_item_meta_sizer.Add( self.m_static_user_retweets, 0, wx.ALL, 5 )

            self.var_user_retweets = wx.StaticText( self.user_feed_list_item, wx.ID_ANY, str(tweet.GetRetweets()), wx.DefaultPosition, wx.DefaultSize, 0 )
            self.var_user_retweets.Wrap( -1 )

            feed_item_meta_sizer.Add( self.var_user_retweets, 0, wx.ALL, 5 )

            user_feed_item_sizer.Add( feed_item_meta_sizer, 0, wx.EXPAND, 5 )

            self.user_feed_list_item.SetSizer( user_feed_item_sizer )
            self.user_feed_list_item.Layout()
            user_feed_item_sizer.Fit( self.user_feed_list_item )
            self.user_feed_list.Add( self.user_feed_list_item, 0, wx.EXPAND |wx.ALL, 5 )
            self.user_feed_list.Layout()

        self.Layout()

    def SetTimelinePosts(self, _home_tweet_list):
        """
        Goes through all the tweets on user's home. For each tweet it fetches its data
        and populates it to the corresponding location in the home tweet list item.
        Then adds the home tweet list item to the home tweet list
        """
        if self.home_content_list.GetItemCount() > 0:
            self.home_content_list.Clear(delete_windows = True)

        for _home_tweet in _home_tweet_list:
            self.home_content_list_item = wx.Panel( self.home_content_scroll, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL )

            list_item_sizer = wx.BoxSizer( wx.VERTICAL )

            list_item_text_sizer = wx.BoxSizer( wx.VERTICAL )

            self.list_item_scroll = wx.ScrolledWindow( self.home_content_list_item, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,125 ), wx.HSCROLL|wx.SUNKEN_BORDER|wx.VSCROLL )
            self.list_item_scroll.SetScrollRate( 5, 5 )
            self.list_item_scroll.SetMaxSize( wx.Size( -1,125 ) )

            list_item_scroll_sizer = wx.BoxSizer( wx.VERTICAL )

            self.var_home_item_text = wx.StaticText( self.list_item_scroll, wx.ID_ANY, _home_tweet.GetTweetText(), wx.DefaultPosition, wx.DefaultSize, 0 )
            self.var_home_item_text.Wrap( 400 )

            list_item_scroll_sizer.Add( self.var_home_item_text, 0, wx.ALL|wx.EXPAND, 5 )

            self.list_item_scroll.SetSizer( list_item_scroll_sizer )
            self.list_item_scroll.Layout()
            list_item_text_sizer.Add( self.list_item_scroll, 1, wx.ALL|wx.EXPAND, 5 )

            list_item_sizer.Add( list_item_text_sizer, 1, wx.EXPAND, 5 )

            list_item_meta_sizer = wx.BoxSizer( wx.HORIZONTAL )

            self.m_static_posted_by = wx.StaticText( self.home_content_list_item, wx.ID_ANY, u"Posted by:", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.m_static_posted_by.Wrap( -1 )

            list_item_meta_sizer.Add( self.m_static_posted_by, 0, wx.ALL, 5 )

            self.var_home_posted_by = wx.StaticText( self.home_content_list_item, wx.ID_ANY, _home_tweet.GetPostedBy(), wx.DefaultPosition, wx.DefaultSize, 0 )
            self.var_home_posted_by.Wrap( -1 )

            list_item_meta_sizer.Add( self.var_home_posted_by, 0, wx.ALL, 5 )

            self.m_staticline108 = wx.StaticLine( self.home_content_list_item, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
            list_item_meta_sizer.Add( self.m_staticline108, 0, wx.EXPAND |wx.ALL, 5 )

            self.m_static_posted_on = wx.StaticText( self.home_content_list_item, wx.ID_ANY, u"Posted On:", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.m_static_posted_on.Wrap( -1 )

            list_item_meta_sizer.Add( self.m_static_posted_on, 0, wx.ALL, 5 )

            self.var_home_posted_on = wx.StaticText( self.home_content_list_item, wx.ID_ANY, _home_tweet.GetTweetDate(), wx.DefaultPosition, wx.DefaultSize, 0 )
            self.var_home_posted_on.Wrap( -1 )

            list_item_meta_sizer.Add( self.var_home_posted_on, 0, wx.ALL, 5 )

            self.m_staticline109 = wx.StaticLine( self.home_content_list_item, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
            list_item_meta_sizer.Add( self.m_staticline109, 0, wx.EXPAND |wx.ALL, 5 )

            self.m_static_likes = wx.StaticText( self.home_content_list_item, wx.ID_ANY, u"Likes:", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.m_static_likes.Wrap( -1 )

            list_item_meta_sizer.Add( self.m_static_likes, 0, wx.ALL, 5 )

            self.var_home_likes = wx.StaticText( self.home_content_list_item, wx.ID_ANY, str(_home_tweet.GetTweetLikes()), wx.DefaultPosition, wx.DefaultSize, 0 )
            self.var_home_likes.Wrap( -1 )

            list_item_meta_sizer.Add( self.var_home_likes, 0, wx.ALL, 5 )

            self.m_staticline110 = wx.StaticLine( self.home_content_list_item, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
            list_item_meta_sizer.Add( self.m_staticline110, 0, wx.EXPAND |wx.ALL, 5 )

            self.m_static_retweets = wx.StaticText( self.home_content_list_item, wx.ID_ANY, u"Retweets:", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.m_static_retweets.Wrap( -1 )

            list_item_meta_sizer.Add( self.m_static_retweets, 0, wx.ALL, 5 )

            self.var_home_retweets = wx.StaticText( self.home_content_list_item, wx.ID_ANY, str(_home_tweet.GetRetweets()), wx.DefaultPosition, wx.DefaultSize, 0 )
            self.var_home_retweets.Wrap( -1 )

            list_item_meta_sizer.Add( self.var_home_retweets, 0, wx.ALL, 5 )

            list_item_sizer.Add( list_item_meta_sizer, 0, wx.EXPAND, 5 )

            self.m_staticline111 = wx.StaticLine( self.home_content_list_item, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
            list_item_sizer.Add( self.m_staticline111, 0, wx.EXPAND |wx.ALL, 0 )

            list_item_controls = wx.BoxSizer( wx.HORIZONTAL )

            self.btn_home_retweet = wx.Button( parent=self.home_content_list_item, id = wx.ID_ANY, label = u"Retweet",pos = wx.DefaultPosition, size = wx.DefaultSize, style = 0, name = str(_home_tweet.GetTweetId()) )
            self.Bind(wx.EVT_BUTTON, self.OnHomePostBtnPress, self.btn_home_retweet)
            list_item_controls.Add( self.btn_home_retweet, 0, wx.ALL, 5 )

            self.btn_home_see_browser = wx.Button( parent=self.home_content_list_item, id = wx.ID_ANY, label = u"See in browser",pos = wx.DefaultPosition, size = wx.DefaultSize, style = 0, name = str(_home_tweet.GetTweetId()))
            self.Bind(wx.EVT_BUTTON, self.OnHomePostBtnPress, self.btn_home_see_browser)
            list_item_controls.Add( self.btn_home_see_browser, 0, wx.ALL, 5 )

            list_item_sizer.Add( list_item_controls, 0, wx.EXPAND, 5 )

            self.home_content_list_item.SetSizer( list_item_sizer )
            self.home_content_list_item.Layout()
            list_item_sizer.Fit( self.home_content_list_item )
            self.home_content_list.Add( self.home_content_list_item, 0, wx.EXPAND |wx.ALL, 5 )
            self.home_content_list.Layout()

        self.Layout()

    def OnHomePostBtnPress(self, event):
        """
        When invoked by the Read button of a tweet, this method will get the id of the tweet and the screen name of the author in order for the
        tweet URL to be built and then loaded into a web browser.
        When invoked by the Retweet button of a tweet, this method will get the id of the tweet and will
        post it to user's twitter are a retweet.
        ...
        In both cases makes a full UI reload.
        """
        btn = event.EventObject
        twitter_creator = ""

        for tweet in self.home_tweet_list:
            if btn.GetName() == str(tweet.GetTweetId()):
                twitter_creator = tweet.GetPostedByScrnName()
                break

        if btn.GetLabel() == self.btn_home_see_browser.GetLabel():
            url = "https://twitter.com/{}/status/{}".format(twitter_creator, btn.GetName())
            webbrowser.open_new_tab(url)

        if btn.GetLabel() == self.btn_home_retweet.GetLabel():
            try:
                twitter = Tweeter()
                twitter.init()
                twitter = twitter.GetInstance()
                twitter.PostRetweet(int(btn.GetName()))

                try:
                    tweeter = Tweeter()
                    tweeter.init()

                    self.SetUserPage(tweeter.GetInstance())
                except Exception as e:
                    wx.MessageBox(str(e), "Error fetching data")

            except Exception as e:
                wx.MessageBox(str(e), "Error")

    def OnSearch(self, event):
        """
        Searches for a page or a person with a query parameter provided by the user.
        The query URL is built and then opened in the browser
        """
        query = self.search_twitter.GetValue()
        query = query.replace(" ", "+")
        webbrowser.open_new_tab("https://twitter.com/search?q={}&src=typed_query".format(query))

    def OnTweet(self, event):
        """
        Posts to Twitter API a new tweet provided by the user.
        Makes a full UI reload
        """
        txt = self.user_tweet_txt_ctrl.GetValue()

        if txt != "" and txt:
             try:
                twitter = Tweeter()
                twitter.init()
                twitter = twitter.GetInstance()
                twitter.PostUpdate(status = txt)
                try:
                    tweeter = Tweeter()
                    tweeter.init()
                    self.SetUserPage(tweeter.GetInstance())
                except Exception as e:
                    wx.MessageBox(str(e), "Error fetching data")

             except Exception as e:
                wx.MessageBox("No internet access", "Error")

    def FormatDate(self, date):
        """
        Formats the date from an ISO format to the format needed in the app
        and returns it
        return : str
        """
        date = date.split(" ")
        date = date[0] + ", " + date[1] + " " + date[2]
        return date

    def HasInternet(self):
        """
        Checks if there an active internet connection
        return : True - there's internet
        return : False - there's no internet
        """
        try:
            socket.create_connection(("www.abv.bg", 80))
            return True
        except OSError:
            return False