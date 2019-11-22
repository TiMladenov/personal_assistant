# Personal Assistant

This is a cross-platform (MacOS, Linux, Windows 10) native desktop personal assistant application
written in Python 3 using wxPython framework. It was created by me as one of my final year
projects before graduating in CS in New Bulgarian University, Sofia, Bulgaria.

# Technology stack
<img src="https://img.stackshare.io/service/993/pUBY5pVj.png" width="25" height="25"> <img src="https://upload.wikimedia.org/wikipedia/commons/c/c0/WxPython-logo.png" width="50" height="25">

# Application features

The application has a toolbar and main content area. The toolbar contains the following tabs:
- Alarm clock
- Author information
- Location (IP-based), time (OS-based), weather (location-based)

The location and weather data is fetched through APIs. If you are using VPN, you might not see
the relevant for your location information.

The main content area contains four tabs, they are:
- News (fetching news from the RESTful API of The Guardian)
    - The users can select "From-To" date and search for specific articles. If there are no
    results or connection, there will be a warning. The results will contain article ID, title, publisher
    (only The Guardian for now), publish date and a button to read each article. If the users want to
    read an article, they have to click on Read button and a pop-up window will appear, containing
    all the meta-information on the article and article's content. There's an option for Text-to-Speach,
    but this doesn't operate as intended under Linux, because the text is too long and the script
    blocks the UI thread until finished and a background thread needs to be added. 
    Under Windows 10 no such issue appears.
- News RSS (fetching news from RSS)
    - If the users want news from the last few days and do not care about search criteria,
    I have added a few RSS channels: The Guardian, The Economist, Times of India. They simply
    have to select one of the providers and the view will automatically populate only with the
    news from the selected provider. There a title, publish date, author's name (optional) and a
    button to read each article. The button here opens a pop-up, but with a link inside, leading
    to the article's webpage, which will open in the user's browser.
- Email (Gmail API)
    - The email tab provides users with the ability to browse their emails. The module is
    currently built to operate with Gmail API only. The users can search their emails based on
    keyword and / or a combination of labels and have an option to limit the number of returned
    results. If there are results, sender, receiver, subject, date of submission and a button
    will populate for each email respectively. The user can then chose an email to read by clicking
    its button. The email contents will populate like subject, sender, submission date and the number of
    attached files and main email messages listed. The users can then use Text-to-Speach to have the
    contents read to them (optional) or can use the Close button to close the email.
- Social (Facebook and Twitter)
    - Facebook
    The Graph API is heavily restricted, a lot of the core features are accessible only
    to verified applications. Mine isn't, so I have only access to basic functionality to add to my app.
    The users can browse their message posts and can expand them if needed to the right side of the view.
    There they can see the entire post and the comments for it. They can also see other basic information
    like the number of likes for posts, date of posting, author. The pages that the user liked could also be seen.
    No data is allowed to be pushed to Grap API.
    - Twitter
    Twitter's API is more liberal than FB Graph API and I was able to add more functionality to my app.
    The users can load their Home and Personal Twitter page. The Home page is where the tweets of followed
    Twitter users are located. The user can retweet these tweets or see them in a browser. There is also
    meta information displayed on each tweet like the author, post date, likes, retweets. There is an option
    for the users to search for something on Twitter through the app. The search results will be in their browser.
    To the right in the app is visible user's page. There, besides user's tweets and retweets,
    the number of followers, following, tweets, as well as their lists, could be seen, right above the
    text field for posting a new tweet.

# Prerequisites to run this application

You'll need Python 3 with [wxpython-phoenix](https://wxpython.org/Phoenix/docs/html/) installed. To do this in
Ubuntu 16.04 LTS, just run:

```
$ pip3 install -U \
-f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 \
wxPython
```
Then you'll need the following Python 3 modules:
```
$ pip3 install pyttsx3
```
```
$ pip3 install --upgrade google-api-python-client \
google-auth-httplib2 google-auth-oauthlib
```
```
$ pip3 install facebook-sdk
```
```
$ pip3 install python-twitter
```

# Private keys

This application is using certain APIs. You will need to provide your own private keys for each one of them:

| File | Keys |
|------|------|
|credentials.js|client_id, project_id, client_secret|
|FbApiCall.py|APP_ID, APP_SECRET, USER_TOKEN_SHORT|
|NewsApiCall.py|self.API_TOKEN|
|token.json|access_token, client_secret, token_type, access_token, refresh_token, client_id, refresh_token, token_expiry|
|TwitterApiCall.py|self.CONSUMER_SECRET, self.CONSUMER_KEY, self.ACCESS_TOKEN_KEY, self.ACCESS_TOKEN_SECRET|
|weather_location_class.py|self.key, self.weather_key|

# Screen shots
|Name|URL|
|----|---|
|Screen 1|https://drive.google.com/open?id=1SG6bR1RPxO2AHJpiEbhZX_QuTO4slpJ3|
|Screen 2|https://drive.google.com/open?id=1L-A_vKcD46LICV2tauVrlzhJajflT3ra|
|Screen 3|https://drive.google.com/open?id=1qIrr9aaFPHHYDKykT_mmtkDawai5nNak|
|Screen 4|https://drive.google.com/open?id=1qnV-O3kvcGLZP4LAbrlXBs4HBceeA9by|
|Screen 5|https://drive.google.com/open?id=1Avo4TcFZ3hFPGR73fReS-WyPRjYsay2M|
|Screen 6|https://drive.google.com/open?id=12CF-CTr6qUVYcNkbPYpQa3Lz40piB6gZ|
|Screen 7|https://drive.google.com/open?id=1G3q6TvOlwIAhEKaCAy2gDVUclW_pSB5L|

# Presentation video
|Video|URL|
|----|----|
|Video 1|https://www.youtube.com/watch?v=H-ckac-OVdE&feature=youtu.be|
|Video 2|https://www.youtube.com/watch?v=p6_-ZopSCIc&feature=youtu.be|

# License
BSD License
>Copyright (c) 2019, Tihomir Mladenov, tihomir.mladenov777@gmail.com
All rights reserved.

>Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

>1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
>2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

>THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

>The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of the Personal Assistant project.
