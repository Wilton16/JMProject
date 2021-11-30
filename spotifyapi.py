import requests
import json

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

def searchforsong(q, type = 'track', limit = 10): #q for search query
    '''Returns a list of song search results'''
    r = requests.get(baseurl + 'search?q=' + q + '&type=' + type + '&limit=' + str(limit), headers=headers).json()['tracks']['items']
    return r
#print(searchforsong('Way 2 Sexy'))

def searchforartist(q, type = 'artist', limit = 10):
    '''Returns a list of artist search results'''
    r = requests.get(baseurl + 'search?q=' + q + '&type=' + type + '&limit=' + str(limit), headers=headers).json()['artists']['items']
    return r
#print(searchforartist('Drake')[0]['popularity'])

    