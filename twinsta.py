# Streaming a tweet using the twitter handle.

from twython import TwythonStreamer
from instamojopkg.instamojo import Instamojo
from dkey import INSTA_API_KEY, INSTA_AUTH_TOKEN, TWITTER_CONSUMER_KEY, \
TWITTER_CONSUMER_SECRET, TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_SECRET

class MyStreamer(TwythonStreamer):

    def __init__(self,TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, \
                    TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_SECRET):
        super(MyStreamer,self).__init__(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, \
                    TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_SECRET)
        self.instaobj = MyInstalink()

    def on_success(self, data):
        if 'text' in data:
            tweet = data['text'].encode('utf-8')
            self.instaobj.generate_link(tweet)
        # disconnecting after the first result
        #self.disconnect()

    def on_error(self, status_code, data):
        print status_code, data


class MyInstalink():

    def __init__(self):
        # Initializing the API wrapper by giving it the api_key and auth_token
        self.api = Instamojo(api_key=INSTA_API_KEY,auth_token=INSTA_AUTH_TOKEN)


    def generate_link(self,tweet):

        # String operations as required to extract the title and description

        tweet = tweet.replace("@bot_divs","")

        if tweet[-1:] == '.':
            tweet = tweet[:-1]

        words = tweet.split()

        splitlist = tweet.split("which is")
        title = splitlist[0]
        desc = splitlist[1].split("costs")[0]

        if 'INR' in words:
            cur = 'INR'
        elif 'USD' in words:
            cur = 'USD'
        p = words.index(cur)
        bp = words[p-1]
        # Creating a Link with one function call.

        response = self.api.link_create(title=title,
                           description=desc,
                           base_price=bp,
                           currency=cur)

        # the URL for the freshly created link!
        with open('link.txt','a') as f:
         f.write(response['link']['url']+"\n")

if __name__ == '__main__':
    # Requires Authentication as of Twitter API v1.1
    stream = MyStreamer(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET,
                    TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_SECRET)

    stream.statuses.filter(track='@bot_divs')
