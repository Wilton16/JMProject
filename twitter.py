from requests import auth
import tweepy
import json
import os
import sqlite3
from spotifyapi import makeartistlist, makeartistpopularities
#from tweepy.client import Client


authentication = tweepy.OAuthHandler("hg88yYv77DupNELwTvSuXjgWx", "LEvSK9ioZ0APvnYO5mYtHaHDSkaBFZfWT7O5s2r0MCpgKGGlN4", "twitter.com")
authentication.set_access_token("2184902148-c9neyAw18DzbZbKU9XIvrTxk9sb74NrtCATHeCD", "8jEWIYQomGmt5uwO7Y8SSzg3CRv2yiKgzjPVNPPJuw93w")
twitterapi = tweepy.API(auth = authentication)

def makeDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def makeSpotifytable(cur, conn, info): 
    cur.execute('CREATE TABLE IF NOT EXISTS TwitterFollowers (Artist Text, Followers Integer)') 
    id = None
    cur.execute('SELECT max(Followers) FROM TwitterFollowers')
    try:
        row = cur.fetchone()

        if row is None:
            id = 0

        else:
            id = row[0]
    except:
        id = 0

    if id is None:
        id = 0
    
    count = 0
    while count < 25: #THIS SHOULD INSERT IT 25 AT A TIME!?
        cur.execute("INSERT OR IGNORE INTO TwitterFollowers (Artist, Followers) VALUES (?, ?)", info)
        conn.commit()
        id += 1
        count += 1
    conn.commit()

def artistsearchtwitter(artistname):
    topresult = twitterapi.search_users(q=artistname)[0]._json["followers_count"]
    return topresult

def spotifytwitterlookup(playlistids):
    artistfollowers=[]
    #print(playlistids)
    for id in playlistids:
        #print("!!!!" + str(id))
        for artist in makeartistlist([id]):
            artistfollowers.append(artist + " Followers: " + str(artistsearchtwitter(artist)))
    return artistfollowers

print("HERE WE GO" + str(spotifytwitterlookup(["37i9dQZF1DX0XUsuxWHRQd"])))
#for artist in makeartistlist(['37i9dQZF1DX0XUsuxWHRQd']):
#    print(artist + " " + str(artistsearchtwitter(artist)))
#for artist in ["Drake", "Kanye West", "Dababy", "Meg Thee Stallion", "Taylor Swift", "Doja Cat"]:
#    print(artist + " ~~ " + str(artistsearchtwitter(artist)))