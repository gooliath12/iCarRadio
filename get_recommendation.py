import spotipy
import time
import json
import numpy as np
import csv
import sys
import spotipy.util as util

def rec(username = 'jamesguo1112', energy=0.5,acousticness=0.5,
       danceability=0.5, valence=0.5, genres=[], PL='iCarRadio'):
    """
    PL: playlist name
    """
    scope = 'user-library-read playlist-read-private playlist-read-collaborative playlist-modify-public'
    #scope = 'user-library-read'

    token = util.prompt_for_user_token('jamesguo1112',
                                       scope=scope,
                                       client_id='67e9f43715fe4227894f0ac0ce5861f7',
                                       client_secret='a31869dd41e3474286f07d5bc31d5316',
                                       redirect_uri='http://localhost/')

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False 
        # tracks = sp.recommendations(seed_genres=['study', 'dance', 'party', 'work-out', 'sleep'], 
        #                             target_energy=energy,
        #                             target_acousticness=acousticness,
        #                             target_danceability=danceability,
        #                             target_valence=valence,
        #                             limit=3)
        tracks = sp.recommendations(seed_genres=genres, limit=20) #target_acousticness=acousticness)
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
    gs = ["acoustic", "chill", "club", "dancehall", "happy", "holidays", "party", "rainy-day", "road-trip", "romance", "sad", "sleep", "study", "summer", "work-out"]
    for g in gs:
        genres = [g]
        rec(genres=genres, PL=g)
    # rec(genres=['sad', 'happy'], PL='Sad & Happy')
    # rec(genres=['happy'], PL='Acousticness', acousticness=1)
