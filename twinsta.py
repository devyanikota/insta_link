from twython import TwythonStreamer
from dkey import INSTA_API_KEY, INSTA_AUTH_TOKEN, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_SECRET

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            self.tweet = data['text'].encode('utf-8')
            print self.tweet
        # Want to disconnect after the first result?
        self.disconnect()

    def on_error(self, status_code, data):
        print status_code, data

# Requires Authentication as of Twitter API v1.1
APP_KEY = TWITTER_CONSUMER_KEY
APP_SECRET = TWITTER_CONSUMER_SECRET
OAUTH_TOKEN = TWITTER_OAUTH_TOKEN
OAUTH_TOKEN_SECRET = TWITTER_OAUTH_SECRET

stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.statuses.filter(track='@bot_divs')

# stream.user()
# Read the authenticated users home timeline
# (what they see on Twitter) in real-time
# stream.site(follow='bot_divs')

from instamojo-py-master.instamojo import Instamojo
# Initialize the API wrapper by giving it your api_key and auth_token
API_KEY = INSTA_API_KEY
AUTH_TOKEN = INSTA_AUTH_TOKEN
api = Instamojo(api_key=API_KEY,
                auth_token=AUTH_TOKEN)

# Create a Link with one function call.
removelist = ['an', 'which', 'with', 'is', 'and']
tweet = stream.tweet
tweet = tweet.replace("@bot_divs","")
if tweet[-1:] == '.':
    tweet = tweet[:-1]
words = tweet.split()
# if i in removelist
titl = tweet.split("which is")[0]
desc = tweet.split("which is")[1].split("costs")[0]
# desc = ' '.join(i for i in words if i not in removelist)
# for word in words:
if 'INR' in words:
    cur = 'INR'
elif 'USD' in words:
    cur = 'USD'
p = words.index(cur)
bp = words[p-1]
response = api.link_create(title=titl,
                       description=desc,
                       base_price=bp,
                       currency=cur)

# Get the URL for the freshly created link!
print response['link']['url']
