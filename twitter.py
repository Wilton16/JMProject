from requests import auth
import tweepy
import json
import os
import sqlite3
from spotifyapi import artistlistfromplaylist, makeDatabase, rapcaviar, pophits, country

authentication = tweepy.OAuthHandler("hg88yYv77DupNELwTvSuXjgWx", "LEvSK9ioZ0APvnYO5mYtHaHDSkaBFZfWT7O5s2r0MCpgKGGlN4", "twitter.com")
authentication.set_access_token("2184902148-c9neyAw18DzbZbKU9XIvrTxk9sb74NrtCATHeCD", "8jEWIYQomGmt5uwO7Y8SSzg3CRv2yiKgzjPVNPPJuw93w")
twitterapi = tweepy.API(auth = authentication)

def makeTwittertable(cur, conn): 
    """Creates a Table in the Database for Twitter"""
    cur.execute('DROP TABLE IF EXISTS TwitterFollowers')
    for i in range(25):
        cur.execute('CREATE TABLE IF NOT EXISTS TwitterFollowers (Artist Text, Followers Integer)') 
    conn.commit()

def inserttwitterdata(cur, conn, info):
    '''Inserts Twitter Data into Table'''
    cur.execute('INSERT INTO TwitterFollowers (Artist, Followers) VALUES (?,?)', info)
    conn.commit()


def artistsearchtwitter(artistname):
    "Searches for an artist on twitter and pulls their follower count"
    topresult = twitterapi.search_users(q=artistname)[0]._json["followers_count"]
    return topresult

def spotifytwitterlookup(playlistids, followerdict = {}):
    """Takes a list from Spotify of artists that appear on a playlist and Searches for individual artists on twitter"""
    for id in [playlistids]:
        for artist in artistlistfromplaylist(id):
            followerdict[artist] = artistsearchtwitter(artist)
    return followerdict

#print(spotifytwitterlookup([rapcaviar, pophits, country]))
