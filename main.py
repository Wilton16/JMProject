from spotifyapi import *
from twitter import *

def main():
    '''Main Function - Runs the whole program'''
    cur, conn = makeDatabase('spotifyartistsfollowings.db')
    playlists = {"rapcaviar": '37i9dQZF1DX0XUsuxWHRQd', "pophits" : '37i9dQZF1DXcBWIGoYBM5M', "country": '37i9dQZF1DX1lVhptIYRda'}
    followers= {}
    popularity = {}
    artistlist =[]
    for playlist in playlists.values():
        for genre in [spotifytwitterlookup(playlist, followers)]:
            continue
        for genre in [artistlistfromplaylist(playlist)]:
            artistlist.append(genre)
        popularity = makeartistpopularities(genre, popularity)
    sitems = str(popularity.items()).strip("dict_items(")[:-1].strip('[(').strip(')]').split('), (')
    stup = []
    for item in sitems:
        item = item.split(', ')
        item = tuple(item)
        stup.append(item)
    titems = str(followers.items()).strip("dict_items(")[:-1].strip('[(').strip(')]').split('), (')
    ttup = []
    for item in titems:
        item = item.split(', ')
        item = tuple(item)
        ttup.append(item)
    makeSpotifytable(cur, conn)
    makeTwittertable(cur, conn)
    '''tl = len(ttup)
    tn = tl// 25
    tr = tl %3
    tcount = 0
    '''
    for tupl in ttup:        
        inserttwitterdata(cur, conn, tupl)
    for tupl in stup:        
        insertspotifydata(cur, conn, tupl)
    

if __name__ == "__main__":
    main()