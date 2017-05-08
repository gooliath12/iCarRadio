import spotipy
import time
import json
import numpy as np
import csv
import sys
import spotipy.util as util
import random
import requests


USERNAME = 'jamesguo1112'
PLAYLIST = 'iCarRadio'
CLIENT_ID = '67e9f43715fe4227894f0ac0ce5861f7'
CLIENT_SECRET = 'a31869dd41e3474286f07d5bc31d5316'


def get_genre():
    gs = ["acoustic", "chill", "club", "dancehall", "happy", "holidays", "party", "rainy-day", "road-trip", "romance", "sad", "sleep", "study", "summer", "work-out"]
    i = random.randint(0, len(gs)-1)
    return [gs[i]]


def rec(sp, username=USERNAME, energy=0.5,acousticness=0.5,
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


def get_token():
    scope = 'user-library-read playlist-read-private playlist-read-collaborative \
         user-read-currently-playing user-read-playback-state playlist-modify-public'

    token = util.prompt_for_user_token(USERNAME,
                                       scope=scope,
                                       client_id='67e9f43715fe4227894f0ac0ce5861f7',
                                       client_secret='a31869dd41e3474286f07d5bc31d5316',
                                       redirect_uri='http://localhost/')
    return token


def get_playlist_id(token):
    response = requests.get('https://api.spotify.com/v1/users/%s/playlists'%(USERNAME), 
                          headers={"Authorization": "Bearer %s"%(token)})
    r = response.json()
    playlists = r['items']
    for playlist in playlists:
        if playlist['name'] == 'iCarRadio':
            return playlist['id']

    return False   # No 'iCarRadio' in User's playlist


def get_lastsong_id(token, pid):
    """
    Get ID of the last song in playlist.
    pid: Playlist ID
    """
    response = requests.get('https://api.spotify.com/v1/users/%s/playlists/%s'%(USERNAME, pid), 
                          headers={"Authorization": "Bearer %s"%(token)})
    r = response.json()
    last_song_id = r['tracks']['items'][-1]['track']['id']
    # print "Last song is:", r['tracks']['items'][-1]['track']['name']
    return last_song_id


def get_current_song_id(token):
    response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', 
                                          headers={"Authorization": "Bearer %s"%(token)})
    r = response.json()
    cur_id = r['item']['id']
    return cur_id


def get_lastsong_name(token, pid):
    response = requests.get('https://api.spotify.com/v1/users/%s/playlists/%s'%(USERNAME, pid), 
                          headers={"Authorization": "Bearer %s"%(token)})
    r = response.json()
    return r['tracks']['items'][-1]['track']['name']



if __name__ == "__main__":
    scope = 'user-library-read playlist-read-private playlist-read-collaborative \
         user-read-currently-playing user-read-playback-state playlist-modify-public'

    token = util.prompt_for_user_token('jamesguo1112',
                                       scope=scope,
                                       client_id='67e9f43715fe4227894f0ac0ce5861f7',
                                       client_secret='a31869dd41e3474286f07d5bc31d5316',
                                       redirect_uri='http://localhost/')

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        # first create playlist here
        # rec(sp, genres=get_genre(), l=5)
        # print "Generated a playlist named iCarRadio."
        # time.sleep(5)
        # Get User's Current Playlists, serach for 'iCarRadio''s ID
        response = requests.get('https://api.spotify.com/v1/users/%s/playlists'%(USERNAME), 
                          headers={"Authorization": "Bearer %s"%(token)})
        r = response.json()
        playlists = r['items']
        find_pl = 0
        for playlist in playlists:
            if playlist['name'] == 'iCarRadio':
                pid = playlist['id']
                find_pl = 1
                break
        
        
            

        # Get last song's id
        response = requests.get('https://api.spotify.com/v1/users/%s/playlists/%s'%(USERNAME, pid), 
                          headers={"Authorization": "Bearer %s"%(token)})
        r = response.json()
        last_song_id = r['tracks']['items'][-1]['track']['id']
        print "Last song is:", r['tracks']['items'][-1]['track']['name']

        print "Start detecting."
        while True:
            response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', 
                                          headers={"Authorization": "Bearer %s"%(token)})
            r = response.json()
            cur_id = r['item']['id']
            if cur_id == last_song_id:
                # rec(sp, genres=get_genre())
                print "Last song. Append new songs."
                rec(sp, genres=get_genre(), l=5)
                time.sleep(3)
                response = requests.get('https://api.spotify.com/v1/users/%s/playlists/%s'%(USERNAME, pid), 
                          headers={"Authorization": "Bearer %s"%(token)})
                r = response.json()
                last_song_id = r['tracks']['items'][-1]['track']['id']
                print "Last song is:", r['tracks']['items'][-1]['track']['name']
            time.sleep(3)
    else:
        print "No token."
