import requests
import json
import os
import sqlite3
from tweepy.parsers import RawParser

client_id = '2dfd4eb13e4748cd9be9bfc68b88af5e'
secret_id = '14376fb761a9464db1577ad397c3e0d1'

AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST request for accessing api given unique id's
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': secret_id,
})

# convert the response to JSON and save access token
auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']
#print(access_token)

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

baseurl = 'https://api.spotify.com/v1/'

def makeDatabase(database):
    """Creates an Inital Database"""
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+database)
    cur = conn.cursor()
    return cur, conn

def makeSpotifytable(cur, conn): 
    """Creates the Spotify Artist Table"""
    cur.execute('DROP TABLE IF EXISTS SpotifyArtist')
    cur.execute('CREATE TABLE IF NOT EXISTS SpotifyArtist (Artist Text, Popularity Integer)') 
    conn.commit()

def insertspotifydata(cur, conn, info):
    #cur.execute('SELECT EXISTS(SELECT 1 FROM SpotifyArtist WHERE Artist=? LIMIT 1)', (info[0],))
    cur.execute('INSERT INTO SpotifyArtist (Artist, Popularity) VALUES (?,?)', info)
    '''record = cur.fetchone()
    print(record)
    if record[0] == 0:
        cur.execute('INSERT INTO SpotifyArtist (Artist, Popularity) VALUES (?,?)', info)'''
    
    conn.commit()
    '''id = None
    cur.execute('SELECT max(Popularity) FROM SpotifyArtist')
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
        cur.execute("INSERT OR IGNORE INTO SpotifyArtist (Artist, Popularity) VALUES (?, ?)", info)
        conn.commit()
        id += 1
        count += 1
    conn.commit()'''

rapcaviar= '37i9dQZF1DX0XUsuxWHRQd'
pophits= '37i9dQZF1DXcBWIGoYBM5M'
country = '37i9dQZF1DX1lVhptIYRda'

def artistlistfromplaylist(playlistid):
    """Takes (a) Playlist ID(s) and searches for the playlist(s), returning a list of artists in that playlist"""
    popularartistlist = []
    #print(playlistid)
    for id in [playlistid]:
        #print("!!" + str(id))
        r = requests.get(baseurl + "playlists/" + str(playlistid), headers=headers).json()['tracks']['items'] #[0]
        for item in r:
            if item['track']['album']['artists'][0]['name'] not in popularartistlist:
                popularartistlist.append(item['track']['album']['artists'][0]['name'])
    return popularartistlist
#print(artistlistfromplaylist(pophits))

def searchforartistpopularity(q, type = 'artist', limit = 10):
    """Returns a list of a searched artist's popularity"""
    r = requests.get(baseurl + 'search?q=' + q + '&type=' + type + '&limit=' + str(limit), headers=headers).json()['artists']['items'][0]['popularity']
    return r
#print(searchforartist('Drake')[0]['popularity'])

#print(artistlistfromplaylist([rapcaviar, pophits, country]))
def makeartistpopularities(artistlist, artistdict= {}):
    "Creates a Dictionary of Artists and their Popularities"
    #artistdict = {}
    for genre in artistlist:
        for artist in [genre]:
            #print(artist)
            artistdict[artist] = searchforartistpopularity(artist)
    return artistdict

#print(makeartistlist([rapcaviar, pophits, country]))
#print(makeartistpopularities(artistlistfromplaylist([rapcaviar, pophits, country])))

def main():
    playlists = {"rapcaviar": '37i9dQZF1DX0XUsuxWHRQd', "pophits" : '37i9dQZF1DXcBWIGoYBM5M', "country": '37i9dQZF1DX1lVhptIYRda'}
    cur, conn = makeDatabase("spotifyartists.db")
    popularity = {}
    artistlist =[]
    for playlist in playlists.values():
        for genre in [artistlistfromplaylist(playlist)]:
            artistlist.append(genre)
        popularity = makeartistpopularities(genre, popularity)
    #print(popularity)
    #print(type(popularity))
    items = str(popularity.items()).strip("dict_items(")[:-1].strip('[(').strip(')]').split('), (')
    tup = []
    for item in items:
        item = item.split(', ')
        item = tuple(item)
        tup.append(item)
    #print(tup[0])
    #print(type(tup[0]))
    #makeSpotifytable(cur, conn, items)
    makeSpotifytable(cur, conn)
    for tupl in tup:        
        insertspotifydata(cur, conn, tupl)


if __name__ == "__main__":
    main()