from requests import auth
import tweepy
#from tweepy.client import Client


authentication = tweepy.OAuthHandler("hg88yYv77DupNELwTvSuXjgWx", "LEvSK9ioZ0APvnYO5mYtHaHDSkaBFZfWT7O5s2r0MCpgKGGlN4", "twitter.com")
authentication.set_access_token("2184902148-c9neyAw18DzbZbKU9XIvrTxk9sb74NrtCATHeCD", "8jEWIYQomGmt5uwO7Y8SSzg3CRv2yiKgzjPVNPPJuw93w")
twitterapi = tweepy.API(auth = authentication)
print("Works")
myfollowers = twitterapi.get_followers(user_id = "cream_sada")
#myfollowers = twitterapi.get_followers()
print(myfollowers)

