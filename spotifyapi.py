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

def makeDatabase(db_name):
    """Creates an Inital Database"""
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def makeSpotifytable(cur, conn, info): 
    """Creates the Spotify Artist Table"""
    cur.execute('CREATE TABLE IF NOT EXISTS SpotifyArtist (Artist Text, Popularity Integer)') 
    id = None
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
    conn.commit()

rapcaviar= '37i9dQZF1DX0XUsuxWHRQd'
top50usa = '37i9dQZEVXbLp5XoPON0wI'
pophits= '37i9dQZF1DXcBWIGoYBM5M'
country = '37i9dQZF1DX1lVhptIYRda'
bangers = '2HB9mGe8dyjusADzqY1qPO'

def artistlistfromplaylist(playlistid):
    """Takes (a) Playlist ID(s) and searches for the playlist(s), returning a list of artists in that playlist"""
    popularartistlist = []
    for id in playlistid:
        r = requests.get(baseurl + "playlists/" + id, headers=headers).json()['tracks']['items']
        for item in r:
            if item['track']['album']['artists'][0]['name'] not in popularartistlist:
                popularartistlist.append(item['track']['album']['artists'][0]['name'])
    return popularartistlist
#print(artistlistfromplaylist(rapcaviar))

def searchforartistpopularity(q, type = 'artist', limit = 10):
    """Returns a list of a searched artist's popularity"""
    r = requests.get(baseurl + 'search?q=' + q + '&type=' + type + '&limit=' + str(limit), headers=headers).json()['artists']['items'][0]['popularity']
    return r
#print(searchforartist('Drake')[0]['popularity'])

#print(artistlistfromplaylist([rapcaviar, pophits, country]))
def makeartistpopularities(artistlist):
    "Creates a Dictionary of Artists and their Popularities"
    artistdict = {}
    for artist in artistlist:
        artistdict[artist] = searchforartistpopularity(artist)
    return artistdict

#print(makeartistlist([rapcaviar, pophits, country]))
#print(makeartistpopularities(makeartistlist([rapcaviar, pophits, country])))

"""def main():
    artists = []
    for item in ["Drake", "Dababy", "Megan Thee Stallion"]:
        artists.append(searchforartist(item)) #WILL HAVE TO SUBSTITUTE SEARCH FOR ARTISTS FOR A MORE CONDENSED FUNCTION RETURN
    cur, conn = makeDatabase("spotifyartists.db")
    makeSpotifytable(cur, conn, artists)


if __name__ == "__main__":
    main()"""