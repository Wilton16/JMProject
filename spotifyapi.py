import requests
import json
import os
import sqlite3


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
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def makeSpotifytable(cur, conn, info): 
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

def pullpopularsongs(playlistid): #fields = ".artists"  + "&fields=" + fields
    print(playlistid)
    r = requests.get(baseurl + "playlists/" + playlistid, headers=headers).json()['tracks']['items']
    #print(r[0]['track']['album']['artists'][0]['name']) #uses a playlist called 2021 bangers
    #dict_keys(['collaborative', 'description', 'external_urls', 'followers', 'href', 'id', 'images', 'name', 'owner', 'primary_color', 'public', 'snapshot_id', 'tracks', 'type', 'uri'])
    #[TRACKS] dict_keys(['href', 'items', 'limit', 'next', 'offset', 'previous', 'total'])
    popularartistlist = []
    for item in r:
        popularartistlist.append(item['track']['album']['artists'][0]['name']) #['track']['artists']['name'])

    return popularartistlist

def searchforsong(q, type = 'track', limit = 10): #q for search query
    '''Returns a list of song search results'''
    r = requests.get(baseurl + 'search?q=' + q + '&type=' + type + '&limit=' + str(limit), headers=headers).json()['tracks']['items']
    return r
#print(searchforsong('Way 2 Sexy'))

def searchforartistpopularity(q, type = 'artist', limit = 10):
    '''Returns a list of artist search results'''
    r = requests.get(baseurl + 'search?q=' + q + '&type=' + type + '&limit=' + str(limit), headers=headers).json()['artists']['items'][0]['popularity']
    return r
#print(searchforartist('Drake')[0]['popularity'])

#need a condensing function still!
#print(pullpopularsongs('37i9dQZEVXbLp5XoPON0wI'))

"""artistlist = []
for playlistid in [rapcaviar,pophits,country]: #top50usa
    for artist in pullpopularsongs(playlistid):
        if artist not in artistlist:
            artistlist.append(artist)"""
#print(artistlist)
def makeartistlist(playlistids):
    listofartists = []
    for playlistid in playlistids:
        #print("!" + str(playlistid))
        for artist in pullpopularsongs(playlistid):
            if artist not in listofartists:
                listofartists.append(artist)
    return listofartists

"""artistpopularities =[]
for artist in artistlist:
    artistdictionary = dict()
    artistdictionary[artist] = searchforartistpopularity(artist)
    artistpopularities.append(artistdictionary)
print(artistpopularities)"""

def makeartistpopularities(artistlist):
    popularities_of_artists = []
    for artist in artistlist:
        artistdict = {}
        artistdict[artist] = searchforartistpopularity(artist)
        popularities_of_artists.append(artistdict)
    return popularities_of_artists

#print(makeartistpopularities(makeartistlist([rapcaviar, pophits, country])))

"""def main():
    artists = []
    for item in ["Drake", "Dababy", "Megan Thee Stallion"]:
        artists.append(searchforartist(item)) #WILL HAVE TO SUBSTITUTE SEARCH FOR ARTISTS FOR A MORE CONDENSED FUNCTION RETURN
    cur, conn = makeDatabase("spotifyartists.db")
    makeSpotifytable(cur, conn, artists)


if __name__ == "__main__":
    main()"""