import spotipy
import time
import json
import numpy as np
import csv
import sys
import spotipy.util as util

def rec(username = 'yangchen0411', energy=0.5,acousticness=0.5,
       danceability=0.5, valence=0.5):
    scope = 'user-library-read playlist-read-private playlist-read-collaborative playlist-modify-public'
    #scope = 'user-library-read'

    token = util.prompt_for_user_token('yangchen0411',
                                       scope=scope,
                                       client_id='70c50ae31d444b79b8c77983eb6dfd2a',
                                       client_secret='ae9b0ba2a48f4516bb5774a59c7e8026',
                                       redirect_uri='https://www.google.com')

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        tracks = sp.recommendations(seed_genres=['study', 'dance', 'party', 'work-out', 'sleep'], 
                                    target_energy=energy,
                                    target_acousticness=acousticness,
                                    target_danceability=danceability,
                                    target_valence=valence,
                                    limit=3)
        track_ids = []
        for t in tracks['tracks']:
            track_ids.append(t['id'])
        playlists = sp.current_user_playlists()
        find = False
        for item in playlists['items']:
            if 'iCarRadio' == item['name']:
                playlist_id = item['id']
                results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
                return True
                find = True
        if not find:
            new_list = sp.user_playlist_create(username, 'iCarRadio')
            playlist_id = new_list['id']
            results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
            return True
    return False
