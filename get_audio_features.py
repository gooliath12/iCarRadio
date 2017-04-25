# -*- coding:utf-8 -*-
import spotipy
import time
import json
import numpy as np
import pprint
import csv

# spotipy supports two authorization flows:

# The Authorization Code flow This method is suitable for long-running applications which the user logs into once.
# It provides an access token that can be refreshed.

# The Client Credentials flow The method makes it possible to authenticate your requests to the Spotify Web API,
# and to obtain a higher rate limit than you would
# Client credentials flow is appropriate for requests that do not require access to a user’s private data.


import sys
import spotipy.util as util


# user need to login Spotify, this is for get user's profile(playlist)
scope = 'user-library-read playlist-read-private playlist-read-collaborative playlist-modify-public'
#scope = 'user-library-read'
username = 'yangchen0411'
token = util.prompt_for_user_token(username,
                                   scope=scope,
                                   client_id='70c50ae31d444b79b8c77983eb6dfd2a',
                                   client_secret='ae9b0ba2a48f4516bb5774a59c7e8026',
                                   redirect_uri='https://www.google.com')


if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    #print "successfully token"
    
    # add a new playlist
    # new_list = sp.user_playlist_create(username, 'test_list')
    # pprint.pprint(new_list)
    
    # add tracks to playlist
    # results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
    # print(results)
    
    w = open('feature_table.csv', 'ab')
    w.write('playlist name'+',')
    w.write('energy'+',')
    w.write('liveness'+',')
    w.write('tempo'+',')
    w.write('speechiness'+',')
    w.write('acousticness'+',')
    w.write('instrumentalness'+',')
    w.write('danceability'+',')
    w.write('loudness'+',')
    w.write('valence'+'\n')

    # get_user_playlist
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        p_name = playlist['name']
        print p_name
        w.write(p_name.encode('utf-8')+',')
        
        energy = []
        liveness = []
        tempo = []
        speechiness = []
        acousticness = []
        instrumentalness = []
        danceability = []
        loudness = []
        valence = []
        
        u_name = playlist['owner']['id']
        results = sp.user_playlist(u_name, playlist['id'],fields="tracks,next")
        tracks = results['tracks']
        for i,item in enumerate(tracks['items']):
            track = item['track']
            tid = str(track['id'])
            features = sp.audio_features(tid)
            energy.append(float(features[0]['energy']))
            liveness.append(float(features[0]['liveness']))
            tempo.append(float(features[0]['tempo']))
            speechiness.append(float(features[0]['speechiness']))
            acousticness.append(float(features[0]['acousticness']))
            instrumentalness.append(float(features[0]['instrumentalness']))
            danceability.append(float(features[0]['danceability']))
            loudness.append(float(features[0]['loudness']))
            valence.append(float(features[0]['valence']))
            
        ene = np.array(energy, dtype=float)
        liv = np.array(liveness, dtype=float)
        tem = np.array(tempo, dtype=float)
        spe = np.array(speechiness, dtype=float)
        aco = np.array(acousticness, dtype=float)
        ins = np.array(instrumentalness, dtype=float)
        dan = np.array(danceability, dtype=float)
        lou = np.array(loudness, dtype=float)
        val = np.array(valence, dtype=float)
        
        w.write(str(ene.mean())+',')
        w.write(str(liv.mean())+',')
        w.write(str(tem.mean())+',')
        w.write(str(spe.mean())+',')
        w.write(str(aco.mean())+',')
        w.write(str(ins.mean())+',')
        w.write(str(dan.mean())+',')
        w.write(str(lou.mean())+',')
        w.write(str(val.mean())+'\n')
        w.write(',')
        w.write(str(ene.std())+',')
        w.write(str(liv.std())+',')
        w.write(str(tem.std())+',')
        w.write(str(spe.std())+',')
        w.write(str(aco.std())+',')
        w.write(str(ins.std())+',')
        w.write(str(dan.std())+',')
        w.write(str(lou.std())+',')
        w.write(str(val.std())+'\n')
        w.write('\n')
        
    w.close()


else:
    print "Can't get token"

