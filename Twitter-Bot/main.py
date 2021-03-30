from credentials import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, ACCOUNT_ID, ACCOUNT_NAME
import tweepy 
from tweepy import Stream 
from tweepy.streaming import StreamListener
import json 

import time
from logger import *

import requests
import os


def respondToTweet(tweet_text, tweeted_by, tweeted_at, tweet_id): 

    if "analyze" in tweet_text or "analyze" in tweet_text.lower():
        decode_info = True
    else:
        decode_info = False

    try:
        f = open("url.txt","r+")
        s_url = f.readline()
        server_url = 'https://fcfd57e81fbd.ngrok.io/predict'
        myobj = {'url': s_url+"?format=jpg&name=orig"}
        x = requests.post(server_url, json = myobj)
        json_data = x.json()
        print(json_data["url"])
        print(x.status_code)
        aws_url = json_data["url"]
        vercel_url = "https://forgedbot.vercel.app/preview/" + aws_url[43:-4]
        print(vercel_url)
        if x.status_code == 200:
            tweet = "Your requested image is processed,you can check the result here 👇" + "\n" + vercel_url
        
    except:
        tweet = "Sorry we can't process your request"


    #Step 3: Tweet Back Information 

    #Step 4: Post the Response
    if decode_info:
        postResponse(tweet, tweet_id)

    try:
        os.remove("url.txt")
    except:
        pass






class StdOutListener(StreamListener):
    def __init__(self, url=None):
        self.url = url

    def on_data(self, data): 
        # print(data)
        clean_data = json.loads(data)
        url = status(clean_data['in_reply_to_status_id'])
        url = str(url)
        f= open("url.txt","w+")
        f.write(url)
        f.close

        f = open("url.txt","r+")
        s_url = f.readline()


        user_mentions, tweeter_id_str = clean_data["entities"]["user_mentions"], clean_data["id_str"]
        tweeted_by, tweeted_at = clean_data["user"]["screen_name"], clean_data["in_reply_to_screen_name"]
        tweet, tweet_id = clean_data["text"], clean_data["id"]

        tweet_url = "https://twitter.com/{0}/status/{1}".format(str(tweeted_by), str(tweet_id))

        logging.info("====================================================")
        logging.info("Tweet by= " + str(tweeted_by))
        logging.info("Tweet at= " + str(tweeted_at))
        logging.info("Tweet= " + str(tweet))
        logging.info("Tweet URL= " + str(tweet_url))
        logging.info(clean_data)
        logging.info("====================================================")


        if user_mentions[0]["screen_name"] == ACCOUNT_NAME or user_mentions[0]["screen_name"] == ACCOUNT_NAME.lower():
            print("Responding to tweet..." + tweet_url)
            respondToTweet(tweet, tweeted_by, tweeted_at, tweet_id)
        elif tweeted_by != ACCOUNT_NAME and ACCOUNT_NAME in tweet: 
            print("Responding to tweet..." + tweet_url)
            respondToTweet(tweet, tweeted_by, tweeted_at, tweet_id)
        

        return True

    def on_error(self, status):
        if status == 420:
            return False
        print("IN ERROR")
        print(status)


def setUpAuth():
    # authentication of consumer key and secret 
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET) 
    # authentication of access token and secret 
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET) 
    api = tweepy.API(auth) 
    return api, auth

def status(data):
    api, auth = setUpAuth()
    sts = api.get_status(data)
    return sts.entities["media"][0]["media_url_https"]


def postResponse(tweet, tweetId): 
    logging.info("Tweeting tweet=" + str(tweet) + " TweetNo=" + str(tweetId))

    api, auth = setUpAuth()
    api.update_status(tweet, in_reply_to_status_id = tweetId, auto_populate_reply_metadata=True)
    #tweetId = tweet['results'][0]['id']
    # api.update_status('@<username> My status update', tweetId)


def followStream():
    api, auth = setUpAuth()
    listener = StdOutListener()

    stream = Stream(auth, listener)
    stream.filter(track=[ACCOUNT_NAME]) #filter=[ACCOUNT_ID]
    # publishTweet(tweet)
    #print(listener.give_url())
    #print("AP")
    


def publishTweet(tweet):
    api, auth = setUpAuth()
    # update the status 
    api.update_status(status = tweet)


if __name__ == "__main__":

    try: 
        followStream()
    except Exception:
        time.sleep(10)
        logging.exception("Fatal exception. Consult logs.")
        followStream()
    finally: 
        time.sleep(10)
        logging.exception("IN FINALLY")
        print("IN FINALLY")
        followStream()