import wx
from FbApiCall import FbApi
import socket
from datetime import datetime

class FB_page( object ):
    """
    A simple custom class to save the properties of a Facebook page
    ...
    Attributes:
    id : str
        The id of the page as in the Graph API
    name : str
        The name of the page as in the Graph API
    ...
    Methods:
    SetPageId(self, _id : str)
        Sets the id of the page
    SetPageName(self, _name : str)
        Sets the name of the page
    GetPageId(self)
        Returns the id of the page
        return : str
    GetPageName(self)
        Returns the name of the page
        return : str
    """
    def __init__(self):
        self.id = None
        self.name = None

    def SetPageId(self, _id):
        """Sets the id of the page"""
        self.id = _id

    def SetPageName(self, _name):
        """Sets the name of the page"""
        self.name = _name

    def GetPageName(self):
        """
        Returns the name of the page
        return : str
        """
        return self.name

    def GetPageId(self):
        """
        Returns the id of the page
        return : str
        """
        return self.id

    def __del__(self):
        del self

class FB_comment( object ):
    """
    A simple custom class to save the properties of a comment to a FB_post()
    ...
    Attributes:
    comment_created_on : str
        The date of creation of the comment
    comment_from : str
        The name of the author of the comment
    comment_message : str
        The text of the comment
    ...
    Methods:
    SetCommentCreatedOn(self, _date : str)
        Sets the date of creation of the comment
    SetCommentFrom(self, _from : str)
        Sets the names of comment's creator
    SetCommentMessage(self, _msg : str)
        Sets the text of the comment
    GetCommentMessage(self)
        Returns the text of the comment
        return : str
    GetCommentFrom(self)
        Returns the names of the author of the comment
        return : str
    GetCommentCreatedOn(self)
        Returns the date of creation of the comment
        return : str
    """
    def __init__(self):
        self.comment_created_on = None
        self.comment_from = None
        self.comment_message = None

    def SetCommentCreatedOn(self, _date):
        """Sets the date of creation of the comment"""
        self.comment_created_on = _date

    def SetCommentFrom(self, _from):
        """Sets the names of comment's creator"""
        self.comment_from = _from

    def SetCommentMessage(self, _msg):
        """Sets the text of the comment"""
        self.comment_message = _msg

    def GetCommentMessage(self):
        """
        Returns the text of the comment
        return : str
        """
        return self.comment_message

    def GetCommentFrom(self):
        """
        Returns the names of the author of the comment
        return : str
        """
        return self.comment_from

    def GetCommentCreatedOn(self):
        """
        Returns the date of creation of the comment
        return : str
        """
        return self.comment_created_on

    def __del__(self):
        del self

class FB_post( object ):
    """
    A simple custom class to save the data of a Facebook post
    ...
    Attributes:
    id : str
        The id of the post from Graph API
    message : str
        The text of the post
    created_on : str
        The date of post's creation
    likes : int
        The number of likes the post has
    comments : list
        Stores all the comments for a given post (FB_comment() instances)
    comments_count : int
        Keeps track of the number of comments for a facebook post
    ...
    Methods:
    SetId(self, _id)
        Sets the id of the post
    GetId(self)
        Returns the id of the post
        return : str
    SetMessage(self, _msg)
        Sets the text of the post
    GetMessage(self)
        Returns the text of the post
        return : str
    SetCreatedOn(self, _created_on)
        Sets the date of creation of the post
    GetCreatedOn(self)
        Gets the date of creation of the post
        return : str
    SetLikes(self, _likes)
        Sets the number of likes the post has
    GetLikes(self)
        Returns the number of likes the post has
        return : int
    SetComments(self, _comment_info)
        The JSON of a comment for this post is passed to this method.
        It creates an instance to FB_comment() and passes comment's data
        to it, then appends in to the comments list and updates the number
        of comments the post has.
    GetCommentCount(self)
        Returns the total number of comments for the specific post
        return : int
    GetComments(self)
        Returns the list of comments for the specific post
        return : list
    """
    def __init__( self ):
        self.id = None
        self.message = None
        self.created_on = None
        self.likes = 0
        self.comments = []
        self.comments_count = 0

    def SetId(self, _id):
        """Sets the id of the post"""
        self.id = _id

    def GetId(self):
        """
        Returns the id of the post
        return : str
        """
        return self.id

    def SetMessage(self, _msg):
        """Sets the text of the post"""
        self.message = _msg

    def GetMessage(self):
        """
        Returns the text of the post
        return : str
        """
        return self.message
    
    def SetCreatedOn(self, _created_on):
        """
        Sets the date of creation of the post
        """
        self.created_on = _created_on

    def GetCreatedOn(self):
        """
        Gets the date of creation of the post
        return : str
        """
        return self.created_on

    def SetLikes(self, _likes):
        """Sets the number of likes the post has"""
        self.likes = _likes

    def GetLikes(self):
        """
        Returns the number of likes the post has
        return : int
        """
        return self.likes

    def SetComments(self, _comment_info):
        """
        The JSON of a comment for this post is passed to this method.
        It creates an instance to FB_comment() and passes comment's data
        to it, then appends in to the comments list and updates the number
        of comments the post has.
        """
        self.comments_count = self.comments_count + 1

        comment = FB_comment()
        comment.SetCommentCreatedOn(_comment_info['created_time'])
        comment.SetCommentFrom(_comment_info['from']['name'])
        comment.SetCommentMessage(_comment_info['message'])

        self.comments.append(comment)

    def GetCommentCount(self):
        """
        Returns the total number of comments for the specific post
        return : int
        """
        return self.comments_count

    def GetComments(self):
        """
        Returns the list of comments for the specific post
        return : list
        """
        return self.comments

    def __del__(self):
        del self

class FB_panel( wx.Panel ):
    """
    This class extents the wx.Panel class and serves to populate the Facebook data of a user
    ...
    Attributes:
    posts_list : list
        List where all the loaded FB_post() instances are stored
    fb_page_obj_list : list
        List where all the loaded FP_page() instances are stores
    var_fb_page_choicesChoices : list
        Populates the names of all the pages that the user likes
    var_fb_name : str
        Populates the names of the authenticated user
    var_fb_friend_count : str
        Populates the number of friends the auth. user has
    var_post_txt_full : str
        Populates the full text of the post
    var_meta_likes : str
        Populates the number of likes the post has
    var_meta_posted : str
        Populates the date the post creation
    btn_fb_update : wx.Button
        Updates the user interface completely.
        Calls on method loadFBdata(self, event)
    btn_post_message : wx.Button
        [non-functional] Creates a post and puts it to the Graph API
    ...
    Methods:
    loadFBdata(self, event)
        If there's internet, the method checks if the UI needs to be cleared
        and clears it.
        It initiates a call to Graph API and then loops through the returned JSON
        to get name, likes(pages), friends, posts (comments, likes, if they have) for the user. Creates the necessary
        objects to store the data for each type, then appends the objects to their
        respective lists.
        ...
        Calls on methods:
        ui_populate_name(data : str)
        ui_populate_pages(page_choices : list)
        ui_populate_friend_count(friends_count : int)
        ui_populate_posts(post_list : list)

    ui_populate_name(self, _data : str)
        Populates the names of the user to the UI
    ui_populate_pages(self, fb_page_choices : list)
        Appends the pages' names to the choice dropdown
    ui_populate_friend_count(self, _count : int)
        Populates the friends count of the user
    ui_populate_posts(self, _post_list : list)
        Goes through the list of posts, creates a list item for each
        post, adds the needed data to it, then appends the list item to the
        post list
    GetCompletePost(self, event)
        Called when the button of a post to be read is clicked. 
        Searches through all the posts, finds it and calls on 
        ReadCompletePost(post)
    ReadCompletePost(self, post : FB_post)
        Fetches post data and populates it in the right side of FB_panel to be
        read completely. If there are any comments for that post, it loads them
        too. Updates the UI
    PostMessage(self, event)
        Gets the value entered by the user the in TextCtrl and attempts to send it to the
        feed of the user
        [Non-Functional! The app is not submitted for approval at FB, thus cannot put data to the Graph]
    GetDateFromISO(self, iso_date : str)
        Returns a formatted date string from ISO date format, for the needs of the app
        return : str
    HasInternet(self)
        Checks if there's internet connection
        return : true - there's internet
        return : false - there's no internet
    """
    def __init__(self, parent):
        super(FB_panel, self).__init__(parent = parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL)

        self.posts_list = []
        self.fb_page_obj_list = []
        self.var_fb_page_choicesChoices = []

        ################################## STATIC UI ##################################
        FB_sizer = wx.BoxSizer( wx.VERTICAL )

        user_data = wx.BoxSizer( wx.HORIZONTAL )

        self.m_static_names = wx.StaticText( self, wx.ID_ANY, u"Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_names.Wrap( -1 )

        user_data.Add( self.m_static_names, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.var_fb_name = wx.StaticText( self, wx.ID_ANY, u"", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
        self.var_fb_name.Wrap( 100 )

        self.var_fb_name.SetMaxSize( wx.Size( 100,-1 ) )

        user_data.Add( self.var_fb_name, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_staticline44 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        user_data.Add( self.m_staticline44, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_static_liked_pages = wx.StaticText( self, wx.ID_ANY, u"Browse pages:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_liked_pages.Wrap( -1 )

        user_data.Add( self.m_static_liked_pages, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.var_fb_page_choices = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 200,-1 ), self.var_fb_page_choicesChoices, 0 )
        self.var_fb_page_choices.SetSelection( 0 )
        self.var_fb_page_choices.SetMaxSize( wx.Size( 200,-1 ) )

        user_data.Add( self.var_fb_page_choices, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_staticline45 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        user_data.Add( self.m_staticline45, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_static_friends = wx.StaticText( self, wx.ID_ANY, u"Friends:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_friends.Wrap( -1 )

        user_data.Add( self.m_static_friends, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.var_fb_friend_count = wx.StaticText( self, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.var_fb_friend_count.Wrap( -1 )

        user_data.Add( self.var_fb_friend_count, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_staticline47 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        user_data.Add( self.m_staticline47, 0, wx.EXPAND |wx.ALL, 5 )

        self.btn_fb_update = wx.Button( self, wx.ID_ANY, u"Update posts", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btn_fb_update.Bind(wx.EVT_BUTTON, self.loadFBdata)
        user_data.Add( self.btn_fb_update, 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 5 )

        FB_sizer.Add( user_data, 0, wx.EXPAND, 5 )

        self.m_staticline46 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        FB_sizer.Add( self.m_staticline46, 0, wx.EXPAND |wx.ALL, 0 )

        FB_content_container = wx.BoxSizer( wx.HORIZONTAL )

        self.FB_post_list = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.FB_post_list.SetScrollRate( 5, 5 )
        self.FB_post_list_sizer = wx.BoxSizer( wx.VERTICAL )

        self.FB_post_list.SetSizer( self.FB_post_list_sizer )
        self.FB_post_list.Layout()
        self.FB_post_list_sizer.Fit( self.FB_post_list )
        FB_content_container.Add( self.FB_post_list, 1, wx.EXPAND |wx.ALL, 5 )

        self.m_staticline53 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        FB_content_container.Add( self.m_staticline53, 0, wx.EXPAND |wx.ALL, 5 )

        self.FB_read_post = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        FB_read_post_sizer = wx.BoxSizer( wx.VERTICAL )

        self.FB_post_panel = wx.Panel( self.FB_read_post, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        FB_post_sizer = wx.BoxSizer( wx.VERTICAL )

        self.FB_post_text_window = wx.ScrolledWindow( self.FB_post_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.SIMPLE_BORDER|wx.VSCROLL )
        self.FB_post_text_window.SetScrollRate( 5, 5 )
        self.FB_post_text_window.SetMaxSize( wx.Size( -1,200 ) )

        FB_post_text_sizer = wx.BoxSizer( wx.VERTICAL )

        self.var_post_txt_full = wx.StaticText( self.FB_post_text_window, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.var_post_txt_full.Wrap( 400 )

        FB_post_text_sizer.Add( self.var_post_txt_full, 0, wx.EXPAND|wx.ALL, 5 )

        self.FB_post_text_window.SetSizer( FB_post_text_sizer )
        self.FB_post_text_window.Layout()
        FB_post_text_sizer.Fit( self.FB_post_text_window )
        FB_post_sizer.Add( self.FB_post_text_window, 1, wx.EXPAND |wx.ALL, 5 )

        self.FB_post_meta = wx.Panel( self.FB_post_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL )
        FB_post_meta_sizer = wx.BoxSizer( wx.HORIZONTAL )

        self.m_static_meta_likes = wx.StaticText( self.FB_post_meta, wx.ID_ANY, u"Likes:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_meta_likes.Wrap( -1 )

        FB_post_meta_sizer.Add( self.m_static_meta_likes, 0, wx.ALL, 5 )

        self.var_meta_likes = wx.StaticText( self.FB_post_meta, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.var_meta_likes.Wrap( -1 )

        FB_post_meta_sizer.Add( self.var_meta_likes, 0, wx.ALL, 5 )

        self.m_staticline60 = wx.StaticLine( self.FB_post_meta, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        FB_post_meta_sizer.Add( self.m_staticline60, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_static_posted = wx.StaticText( self.FB_post_meta, wx.ID_ANY, u"Posted on:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_static_posted.Wrap( -1 )

        FB_post_meta_sizer.Add( self.m_static_posted, 0, wx.ALL, 5 )

        self.var_meta_posted = wx.StaticText( self.FB_post_meta, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.var_meta_posted.Wrap( -1 )

        FB_post_meta_sizer.Add( self.var_meta_posted, 0, wx.ALL, 5 )

        self.m_staticline61 = wx.StaticLine( self.FB_post_meta, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        FB_post_meta_sizer.Add( self.m_staticline61, 0, wx.EXPAND |wx.ALL, 5 )

        self.FB_post_meta.SetSizer( FB_post_meta_sizer )
        self.FB_post_meta.Layout()
        FB_post_meta_sizer.Fit( self.FB_post_meta )
        FB_post_sizer.Add( self.FB_post_meta, 0, wx.EXPAND |wx.ALL, 5 )

        self.FB_post_reply = wx.ScrolledWindow( self.FB_post_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.SIMPLE_BORDER|wx.VSCROLL )
        self.FB_post_reply.SetScrollRate( 5, 5 )
        self.FB_post_reply_list = wx.BoxSizer( wx.VERTICAL )


        self.FB_post_reply.SetSizer( self.FB_post_reply_list )
        self.FB_post_reply.Layout()
        self.FB_post_reply_list.Fit( self.FB_post_reply )
        FB_post_sizer.Add( self.FB_post_reply, 1, wx.EXPAND |wx.ALL, 5 )

        self.FB_post_panel.SetSizer( FB_post_sizer )
        self.FB_post_panel.Layout()
        FB_post_sizer.Fit( self.FB_post_panel )
        FB_read_post_sizer.Add( self.FB_post_panel, 1, wx.EXPAND |wx.ALL, 5 )

        self.m_staticline59 = wx.StaticLine( self.FB_read_post, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        FB_read_post_sizer.Add( self.m_staticline59, 0, wx.EXPAND |wx.ALL, 5 )

        FB_post_comment = wx.BoxSizer( wx.VERTICAL )

        self.FB_post_message_box = wx.TextCtrl( self.FB_read_post, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,120 ), wx.TE_MULTILINE )
        self.FB_post_message_box.SetMaxSize( wx.Size( -1,300 ) )

        FB_post_comment.Add( self.FB_post_message_box, 0, wx.ALL|wx.EXPAND, 5 )

        self.btn_post_message = wx.Button( self.FB_read_post, wx.ID_ANY, u"Post Message", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btn_post_message.Bind(wx.EVT_BUTTON, self.PostMessage)
        FB_post_comment.Add( self.btn_post_message, 0, wx.ALL|wx.EXPAND, 5 )

        FB_read_post_sizer.Add( FB_post_comment, 0, wx.EXPAND, 5 )

        self.FB_read_post.SetSizer( FB_read_post_sizer )
        self.FB_read_post.Layout()
        FB_read_post_sizer.Fit( self.FB_read_post )
        FB_content_container.Add( self.FB_read_post, 1, wx.EXPAND |wx.ALL, 5 )

        FB_sizer.Add( FB_content_container, 1, wx.EXPAND, 5 )

        self.SetSizer( FB_sizer )
        self.Layout()
        FB_sizer.Fit( self )
        self.Layout()
        ################################## STATIC UI ##################################

    def loadFBdata(self, event):
        """
        If there's internet, the method checks if the UI needs to be cleared
        and clears it.
        It initiates a call to Graph API and then loops through the returned JSON
        to get name, likes(pages), friends, posts (comments, likes, if they have) for the user. Creates the necessary
        objects to store the data for each type, then appends the objects to their
        respective lists.
        ...
        Calls on methods:
        ui_populate_name(data : str)
        ui_populate_pages(page_choices : list)
        ui_populate_friend_count(friends_count : int)
        ui_populate_posts(post_list : list)
        """
        if self.HasInternet():
            fb_call = FbApi()
            posts = fb_call.get_fb_info()

            if self.FB_post_list_sizer.GetItemCount() > 0:
                self.FB_post_list_sizer.Clear(delete_windows = True)
                self.FB_post_list_sizer.Layout()

            if len(self.var_fb_page_choicesChoices) > 0:
                self.var_fb_page_choicesChoices.clear()
            
            if len(self.fb_page_obj_list) > 0:
                self.fb_page_obj_list.clear()

            if len(self.posts_list) > 0:
                self.posts_list.clear()

            for ind, data in posts.items():
                if ind == 'name':
                    self.ui_populate_name(data)

                if ind == 'likes':
                    pages = data['data']

                    for page in pages:
                        tmp_page = FB_page()

                        tmp_page.SetPageId(page['id'])
                        tmp_page.SetPageName(page['name'])

                        self.fb_page_obj_list.append(tmp_page)
                        self.var_fb_page_choicesChoices.append(tmp_page.GetPageName())
                        self.ui_populate_pages(self.var_fb_page_choicesChoices)

                if ind == 'friends':
                    friends_count = data['summary']['total_count']
                    self.ui_populate_friend_count(friends_count)

                if ind == 'posts':
                    for post in data['data']:
                        tmp_post = FB_post()
                        tmp_post.SetId(post['id'])
                        tmp_post.SetCreatedOn(post['created_time'])
                        if 'message' in post:
                            tmp_post.SetMessage(post['message'])
                        likes = None
                        comments = None
                        try:
                            likes = fb_call.get_fb_connections(post['id'], 'likes')
                            likes = likes['data']
                            comments = fb_call.get_fb_connections(post['id'], 'comments')
                            comments = comments['data']

                            if comments != []:
                                for comment in comments:
                                    tmp_post.SetComments(comment)

                            if likes != []:
                                tmp_post.SetLikes(len(likes))

                        except Exception as e:
                            pass
                        
                        self.posts_list.append(tmp_post)
                        del tmp_post

                    self.ui_populate_posts(self.posts_list)
        else:
            wx.MessageBox("There's no internet connection", "Connection error")

    def ui_populate_name(self, _data):
        """Populates the names of the user to the UI"""
        self.var_fb_name.SetLabel(_data)
        self.Layout()

    def ui_populate_pages(self, fb_page_choices):
        """Appends the pages' names to the choice dropdown"""
        self.var_fb_page_choices.Clear()

        for page in fb_page_choices:
            self.var_fb_page_choices.Append(page)
        self.Layout()

    def ui_populate_friend_count(self, _count):
        """Populates the friends count of the user"""
        self.var_fb_friend_count.SetLabel(str(_count))
        self.Layout()

    def ui_populate_posts(self, _post_list):
        """
        Goes through the list of posts, creates a list item for each
        post, adds the needed data to it, then appends the list item to the
        posts' list
        """
        for post in _post_list:
            if post.GetMessage():
                self.FB_post_list_item = wx.Panel( self.FB_post_list, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL )
                FB_post_list_item_sizer = wx.BoxSizer( wx.VERTICAL )

                FB_post_message = wx.BoxSizer( wx.HORIZONTAL )

                self.m_static_message = wx.StaticText( self.FB_post_list_item, wx.ID_ANY, u"Message", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.m_static_message.Wrap( -1 )

                FB_post_message.Add( self.m_static_message, 0, wx.ALL|wx.EXPAND, 5 )

                self.m_staticline54 = wx.StaticLine( self.FB_post_list_item, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
                FB_post_message.Add( self.m_staticline54, 0, wx.EXPAND |wx.ALL, 5 )

                self.message_container = wx.ScrolledWindow( self.FB_post_list_item, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,60 ), wx.HSCROLL|wx.VSCROLL )
                self.message_container.SetScrollRate( 5, 5 )
                self.message_container.SetMaxSize( wx.Size( -1,60 ) )

                message_container_sizer = wx.BoxSizer( wx.VERTICAL )

                self.var_fb_message = wx.StaticText( self.message_container, wx.ID_ANY, post.GetMessage(), wx.DefaultPosition, wx.DefaultSize, 0 )
                self.var_fb_message.Wrap( 300 )

                message_container_sizer.Add( self.var_fb_message, 0, wx.ALL|wx.EXPAND, 5 )

                self.message_container.SetSizer( message_container_sizer )
                self.message_container.Layout()
                FB_post_message.Add( self.message_container, 1, wx.EXPAND |wx.ALL, 5 )

                FB_post_list_item_sizer.Add( FB_post_message, 1, wx.EXPAND, 5 )

                self.m_staticline55 = wx.StaticLine( self.FB_post_list_item, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
                FB_post_list_item_sizer.Add( self.m_staticline55, 0, wx.EXPAND |wx.ALL, 0 )

                FB_post_meta_data = wx.BoxSizer( wx.HORIZONTAL )

                self.m_static_likes = wx.StaticText( self.FB_post_list_item, wx.ID_ANY, u"Likes:", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.m_static_likes.Wrap( -1 )

                FB_post_meta_data.Add( self.m_static_likes, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

                self.var_fb_post_likes = wx.StaticText( self.FB_post_list_item, wx.ID_ANY, str(post.GetLikes()), wx.DefaultPosition, wx.DefaultSize, 0 )
                self.var_fb_post_likes.Wrap( -1 )

                FB_post_meta_data.Add( self.var_fb_post_likes, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

                self.m_staticline56 = wx.StaticLine( self.FB_post_list_item, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
                FB_post_meta_data.Add( self.m_staticline56, 0, wx.EXPAND |wx.ALL, 5 )

                self.m_static_comments = wx.StaticText( self.FB_post_list_item, wx.ID_ANY, u"Comments:", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.m_static_comments.Wrap( -1 )

                FB_post_meta_data.Add( self.m_static_comments, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

                self.var_fb_comments = wx.StaticText( self.FB_post_list_item, wx.ID_ANY, str(post.GetCommentCount()), wx.DefaultPosition, wx.DefaultSize, 0 )
                self.var_fb_comments.Wrap( -1 )

                FB_post_meta_data.Add( self.var_fb_comments, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

                self.m_staticline57 = wx.StaticLine( self.FB_post_list_item, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
                FB_post_meta_data.Add( self.m_staticline57, 0, wx.EXPAND |wx.ALL, 5 )

                self.m_static_posted_on = wx.StaticText( self.FB_post_list_item, wx.ID_ANY, u"Posted:", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.m_static_posted_on.Wrap( -1 )

                FB_post_meta_data.Add( self.m_static_posted_on, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

                _created_date = self.GetDateFromISO(post.GetCreatedOn())
                self.m_staticText68 = wx.StaticText( self.FB_post_list_item, wx.ID_ANY, _created_date, wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
                self.m_staticText68.Wrap( -1 )

                FB_post_meta_data.Add( self.m_staticText68, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

                self.btn_fb_read_comment = wx.Button( parent = self.FB_post_list_item, id = wx.ID_ANY, label = u"Read comment", pos = wx.DefaultPosition, size = wx.DefaultSize, style = 0, name = post.GetId() )
                self.btn_fb_read_comment.Bind(wx.EVT_BUTTON, self.GetCompletePost)
                FB_post_meta_data.Add( self.btn_fb_read_comment, 0, wx.ALL|wx.EXPAND, 5 )

                FB_post_list_item_sizer.Add( FB_post_meta_data, 0, wx.EXPAND, 5 )

                self.FB_post_list_item.SetSizer( FB_post_list_item_sizer )
                self.FB_post_list_item.Layout()
                FB_post_list_item_sizer.Fit( self.FB_post_list_item )
                self.FB_post_list_sizer.Add( self.FB_post_list_item, 0, wx.EXPAND |wx.ALL, 5 )
                self.FB_post_list_sizer.Layout()
                self.Layout()


    def GetCompletePost(self, event):
        """
        Called when the button of a post to be read is clicked. 
        Searches through all the posts, finds it and calls on 
        ReadCompletePost(post)
        """
        btn = event.EventObject
        post_id = btn.GetName()

        for post in self.posts_list:
            if post_id == post.GetId():
                self.ReadCompletePost(post)

    def ReadCompletePost(self, _post):
        """
        Fetches post data and populates it in the right side of FB_panel to be
        read completely. If there are any comments for that post, it loads them
        too. Updates the UI
        """
        self.var_post_txt_full.SetLabel(_post.GetMessage())
        self.var_meta_likes.SetLabel(str(_post.GetLikes()))
        self.var_meta_posted.SetLabel(str(self.GetDateFromISO(_post.GetCreatedOn())))

        if self.FB_post_reply_list.GetItemCount() > 0:
            self.FB_post_reply_list.Clear(delete_windows = True)
            self.FB_post_reply_list.Layout()

        if _post.GetCommentCount() > 0:
            comments = _post.GetComments()

            for comment in comments:
                self.FB_post_reply_list_item = wx.Panel( self.FB_post_reply, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL )
                FB_list_item_sizer = wx.BoxSizer( wx.VERTICAL )

                FB_list_item_text = wx.BoxSizer( wx.HORIZONTAL )

                self.var_reply_text = wx.StaticText( self.FB_post_reply_list_item, wx.ID_ANY, comment.GetCommentMessage(), wx.DefaultPosition, wx.DefaultSize, 0 )
                self.var_reply_text.Wrap( 400 )

                FB_list_item_text.Add( self.var_reply_text, 0, wx.ALL, 5 )

                FB_list_item_sizer.Add( FB_list_item_text, 1, wx.EXPAND, 5 )

                self.m_staticline62 = wx.StaticLine( self.FB_post_reply_list_item, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
                FB_list_item_sizer.Add( self.m_staticline62, 0, wx.EXPAND |wx.ALL, 5 )

                FB_list_item_meta = wx.BoxSizer( wx.HORIZONTAL )

                self.m_static_reply_from = wx.StaticText( self.FB_post_reply_list_item, wx.ID_ANY, u"From:", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.m_static_reply_from.Wrap( -1 )

                FB_list_item_meta.Add( self.m_static_reply_from, 0, wx.ALL, 5 )

                self.var_reply_from = wx.StaticText( self.FB_post_reply_list_item, wx.ID_ANY, comment.GetCommentFrom(), wx.DefaultPosition, wx.DefaultSize, 0 )
                self.var_reply_from.Wrap( -1 )

                FB_list_item_meta.Add( self.var_reply_from, 0, wx.ALL, 5 )

                self.m_staticline63 = wx.StaticLine( self.FB_post_reply_list_item, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
                FB_list_item_meta.Add( self.m_staticline63, 0, wx.EXPAND |wx.ALL, 5 )

                self.m_static_reply_posted = wx.StaticText( self.FB_post_reply_list_item, wx.ID_ANY, u"Replied on:", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.m_static_reply_posted.Wrap( -1 )

                FB_list_item_meta.Add( self.m_static_reply_posted, 0, wx.ALL, 5 )

                self.var_reply_posted = wx.StaticText( self.FB_post_reply_list_item, wx.ID_ANY, self.GetDateFromISO(comment.GetCommentCreatedOn()), wx.DefaultPosition, wx.DefaultSize, 0 )
                self.var_reply_posted.Wrap( -1 )

                FB_list_item_meta.Add( self.var_reply_posted, 0, wx.ALL, 5 )

                FB_list_item_sizer.Add( FB_list_item_meta, 0, wx.EXPAND, 5 )

                self.FB_post_reply_list_item.SetSizer( FB_list_item_sizer )
                self.FB_post_reply_list_item.Layout()
                FB_list_item_sizer.Fit( self.FB_post_reply_list_item )
                self.FB_post_reply_list.Add( self.FB_post_reply_list_item, 0, wx.EXPAND |wx.ALL, 5 )
                self.FB_post_reply_list.Layout()

            self.Layout()

    def PostMessage(self, event):
        """
        Gets the value entered by the user the in TextCtrl and attempts to send it to the
        feed of the user
        [Non-Functional! The app is not submitted for approval at FB, thus cannot put data to the Graph]
        """
        _txt = self.FB_post_message_box.GetValue()

        fb_call = FbApi()
        fb_call.initialize_only()
        fb_call.put_fb_object('me', _txt)


    def GetDateFromISO(self, _iso_date):
        """
        Returns a formatted date string from ISO date format, for the needs of the app
        return : str
        """
        _format = "%Y-%m-%dT%H:%M:%S%z"
        _created_date_formatted = datetime.strptime(_iso_date, _format)
        _created_date_formatted = _created_date_formatted.strftime("%b %d, %H:%M")
        return _created_date_formatted

    def HasInternet(self):
        """
        Checks if there's internet connection
        return : true - there's internet
        return : false - there's no internet
        """
        try:
            socket.create_connection(("www.abv.bg", 80))
            return True
        except OSError:
            return False
