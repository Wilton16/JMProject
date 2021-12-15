from main import *

conn = sqlite3.connect('spotifyartistsfollowings.db')
cur = conn.cursor()

cur.execute('SELECT SpotifyArtist.Popularity, TwitterFollowers.Followers FROM SpotifyArtist JOIN TwitterFollowers ON SpotifyArtist.Artist = TwitterFollowers.Artist')

rows = cur.fetchall()
#print(rows)
ratiolist = []
for row in rows:
    ratio=  row[1] / row[0]
    ratiolist.append(ratio)
average = sum(ratiolist)/len(ratiolist)

with open('writtenfile', 'w') as text:
    text.write('Here is a combination of spotify popularities and twitter followings for selected artists.')
    text.write('\n')
    text.write(str(rows))
    text.write('\n')
    text.write("Here is the individual correlations between an artist's spotify popularity and their twitter following.")
    text.write('\n')
    text.write(str(ratiolist))
    text.write('\n')
    text.write("Here is the average correlation between an artist's spotify popularity and their twitter following.")
    text.write('\n')
    text.write(str(average))
    text.write('\n')