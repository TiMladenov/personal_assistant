import urllib.request
import json
import requests
import math

class WeatherLocation(object):
    """
    A class that is used to get the location of the user and the weather
    for this location
    ...
    external_ip : str
        Stores the external IP of the user [The use of VPN might reduces accuracy]
    location_base_url : str
        Base URL that will be queried to get the location of the user
    key : str
        A key for the location_base_url when queried
    temp : int
        Stores the temperature of user's geo location
    weather : str
        The weather around user's geo location [clear, rain, etc]
    weather_base_url : str
        The base url that is queried to get the weather for user's
        get location
    weather_key : str
        The key to perform the action above
    city : str
        User's city [IP dependent for accuracy]
    country : str
        User's country [IP dependent for accuracy]
    ...
    Methods:
    FindIpAddress(self)
        Queries ident.me. The response is user's public IP address.
    GetIpAddress(self)
        Returns the stored public IP address
        return : str
    GetLocation(self)
        Uses the public IP to find the location and country (code)
        of the user
    Parse(self, response : str)
        Parses the received response to JSON format.
        return : JSON - success
        return : Error [str] - error
    GetCity(self)
        Returns the stored user city
        return : str
    GetCountry(self)
        Returns the stored user country
        return : str
    FindWeather(self, base_url, city, country, key)
        Queries the base_url to get the weather for the city + country
        Sets instances' weather conditions and temperature variables.
        Calls GetWeatherDetails(self, response)
    GetWeatherDetails(self, response : str)
        Parses the provided response to JSON
        return JSON - success
        return Error - error
    GetWeather(self)
        return weather : str
    GetTemp(self)
        return temp : int
    """
    def __init__(self):

        self.external_ip = ""
        self.location_base_url = "http://api.ipstack.com/"
        self.key = ""
        
        self.temp = None
        self.weather = "N/A"
        self.weather_base_url = "https://openweathermap.org/data/2.5/weather?q="
        self.weather_key = ""

        self.city = "N/A"
        self.country = "N/A"

        self.FindIpAddress()
        self.GetLocation()
        self.FindWeather(self.weather_base_url, self.city, self.country, self.weather_key)

    def __del__(self):
        del self

    def FindIpAddress(self):
        """Queries ident.me. The response is user's public IP address."""
        self.external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf-8')

    def GetIpAddress(self):
        """
        Returns the stored public IP address
        return : str
        """
        return self.external_ip

    def GetLocation(self):
        """
        Uses the public IP to find the location and country (code)
        of the user
        """
        callString = self.location_base_url + self.external_ip + "?access_key=" + self.key
        callString = format(callString)

        response = requests.get(callString)
        response = self.Parse(response)

        if "city" in response:
                self.city = response["city"]

        if "country_code" in response:
            self.country = response["country_code"]

    def Parse(self, _response):
        """
        Parses the received response to JSON format.
        return : JSON - success
        return : Error [str] - error
        """
        data = ""
        if _response.status_code == 200:
            data = json.loads(_response.content.decode('utf-8'))
        else:
            data = "There was an error while loading the location data: {0}".format(_response.status_code)
        return data

    def GetCity(self):
        """
        Returns the stored user city
        return : str
        """
        return self.city

    def GetCountry(self):
        """
        Returns the stored user country
        return : str
        """
        return self.country

    def FindWeather(self, _base_url, _city, _country, _key):
        """
        Queries the base_url to get the weather for the city + country
        Sets instances' weather conditions and temperature variables.
        Calls GetWeatherDetails(self, response)
        """
        callStr = _base_url + _city + "," +  _country + "&appid=" + _key
        callStr = format(callStr)
        response = requests.get(callStr)
        response = self.GetWeatherDetails(response)

        try:
            if "weather" in response and "main" in response["weather"][0]:
                self.weather = response["weather"][0]["main"]

            if "main" in response and "temp" in response["main"]:
                self.temp = int(math.ceil(float(response["main"]["temp"])))
        except Exception as e:
            print(e)
            self.weather = 'N/A'
            self.temp = 'N/A'

    def GetWeatherDetails(self, _response):
        """
        Parses the provided response to JSON
        return JSON - success
        return Error - error
        """
        data = ""
        if _response.status_code == 200:
            data = json.loads(_response.content.decode('utf-8'))
        else:
            data = "There was an error while loading the weather data: {0}".format(_response.status_code)
        return data

    def GetWeather(self):
        """return weather : str"""
        return self.weather

    def GetTemp(self):
        """return temp : int"""
        return self.temp