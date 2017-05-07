import spotipy
import time
import json
import numpy as np
import csv
import sys
import spotipy.util as util
import random
import requests

def get_genre():
    gs = ["acoustic", "chill", "club", "dancehall", "happy", "holidays", "party", "rainy-day", "road-trip", "romance", "sad", "sleep", "study", "summer", "work-out"]
    i = random.randint(0, len(gs)-1)
    return [gs[i]]
    
def rec(sp, username = 'yangchen0411', energy=0.5,acousticness=0.5,
       danceability=0.5, valence=0.5, genres=[], PL='iCarRadio', l=5):
    tracks = sp.recommendations(seed_genres=genres, limit=l)
    track_ids = []
    for t in tracks['tracks']:
        track_ids.append(t['id'])
    playlists = sp.current_user_playlists()
    find = False
    for item in playlists['items']:
        if PL == item['name']:
            playlist_id = item['id']
            results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
            return True
            find = True
    if not find:
        new_list = sp.user_playlist_create(username, PL)
        playlist_id = new_list['id']
        results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
        return True
    return False

if __name__ == "__main__":
    scope = 'user-library-read playlist-read-private playlist-read-collaborative \
         user-read-currently-playing user-read-playback-state playlist-modify-public'

    token = util.prompt_for_user_token('yangchen0411',
                                       scope=scope,
                                       client_id='67e9f43715fe4227894f0ac0ce5861f7',
                                       client_secret='a31869dd41e3474286f07d5bc31d5316',
                                       redirect_uri='http://localhost/')

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        counter = 5
        cur_id = str(0)
        rec(sp, genres=get_genre(), l=7)
        response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', 
                          headers={"Authorization": "Bearer %s"%(token)})
        r = response.json()
        cur_id = r['item']['id']
        while True:
            if counter == 0:
                rec(sp, genres=get_genre())
                counter = 5
            else:
                response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', 
                                          headers={"Authorization": "Bearer %s"%(token)})
                r = response.json()
                if cur_id != r['item']['id']:
                    cur_id = r['item']['id']
                    counter -= 1
            time.sleep(120)
