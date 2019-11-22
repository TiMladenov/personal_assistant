#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests
import wx
import news_panel_class


class ReadNews(object):
    """
    A class to make GET calls to The Guardian API
    ...
    Attributes:
    API_URL_BASE : str
        A base URL to The Guardian API
    API_TOKEN : str
        A token to access The Guardian API
    base_query : str
        The query entered by the user
    date_from : str
        The provided by the user date_from for news
        (lower bound)
    date_to : str
        (upper bound)
        The provided by the user date_to for news
    parent : wx.Window
        A reference to the window from which the request was
        initiated
    news_provider : str
        Currently serves only a cosmetic purpose. May be used
        in future when multiple REST news providers are included
    response_dict : dict
        Returns a response [True or False] and a status code. If True, the JSON
        response from the API is included in the return
    headers : dict
        The headers to be used for auth with The Guardian's API.
    ...
    Methods:
    GetQuery(self)
        Makes a call to the API and calls and passes the response
        to parseGet(response)
    GetNewsProvider(self)
        Returns the used news provider
    parseGet(self, response : JSON)
        Parses the response and labels it as Success if there aren't
        any error messages or labels it as Error if there are error
        messages. If the response is success, it also attaches the
        returned JSON from the API.
        return : dict + JSON - success
        return : error - fail
    """

    def __init__(self, parent, from_date, to_date, news_provider, query_txt):

        self.API_URL_BASE = \
            'https://content.guardianapis.com/search?api-key='
        self.API_TOKEN = ''
        self.base_query = '&q=' + query_txt
        self.date_from = '&from-date=' + from_date
        self.date_to = '&to-date=' + to_date
        self.parent = parent
        self.news_provider = news_provider

        self.response_dict = {"Error" : "", "Success" : ""}

        self.headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(self.API_TOKEN)}

        self.query = self.API_URL_BASE + self.API_TOKEN + "&order-by=newest" + self.base_query + self.date_from \
            + self.date_to + "&page-size=100" + "&show-fields=thumbnail%2CbodyText"
        self.query = format(self.query)

    def __del__(self):
        pass

    def GetQuery(self):
        """
        Makes a call to the API and calls and passes the response
        to parseGet(response)
        """
        response = requests.get(self.query, headers=self.headers)
        response = self.parseGet(response)
        return self.response_dict

    def GetNewsProvider(self):
        """Returns the used news provider"""
        return self.news_provider

    def parseGet(self, _response):
        """
        Parses the response and labels it as Success if there aren't
        any error messages or labels it as Error if there are error
        messages. If the response is success, it also attaches the
        returned JSON from the API.
        return : dict + JSON - success
        return : error - fail
        """
        if _response.status_code == 200:
            data = json.loads(_response.content.decode('utf-8'))
            self.response_dict["Success"] = data
            return self.response_dict
        elif _response.status_code >= 300:
            err = ('{0} : Unexpected redirect.').format(_response.status_code)
            self.response_dict["Error"] = err
            return self.response_dict
        elif _response.status_code == 400:
            err = ('{0} : Bad request').format(_response.status_code)
            self.response_dict["Error"] = err
            return self.response_dict
        elif _response.status_code == 401:
            err = ('{0} : Auth failed').format(_response.status_code)
            self.response_dict["Error"] = err
            return self.response_dict
        elif _response.status_code == 404:
            err = ('{0} : Ups, url not found').format(_response.status_code)
            self.response_dict["Error"] = err
            return self.response_dict
        elif _response.status_code >= 500:
            err = ('{0} : Server error').format(_response.status_code)
            self.response_dict["Error"] = err
            return self.response_dict
        else:
            err = ('Unexpected Error: [HTTP {0}]: Content: {1}').format(_response.status_code, _response.content)
            self.response_dict["Error"] = err
            return self.response_dict