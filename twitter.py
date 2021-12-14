from requests import auth
import tweepy
import json
#from tweepy.client import Client


authentication = tweepy.OAuthHandler("hg88yYv77DupNELwTvSuXjgWx", "LEvSK9ioZ0APvnYO5mYtHaHDSkaBFZfWT7O5s2r0MCpgKGGlN4", "twitter.com")
authentication.set_access_token("2184902148-c9neyAw18DzbZbKU9XIvrTxk9sb74NrtCATHeCD", "8jEWIYQomGmt5uwO7Y8SSzg3CRv2yiKgzjPVNPPJuw93w")
twitterapi = tweepy.API(auth = authentication)

def artistsearchtwitter(artistname):
    topresult = twitterapi.search_users(q=artistname)[0]._json["followers_count"]
    return topresult

#for artist in ["Drake", "Kanye West", "Dababy", "Meg Thee Stallion", "Taylor Swift", "Doja Cat"]:
#    print(artist + " ~~ " + str(artistsearchtwitter(artist)))