import time, json
from add_tracks_to_iCarRadio import *
from gather_data import *

if __name__ == '__main__':
    # Initialization:
    print "Initialization."
    token = get_token()
    pid = get_playlist_id(token)
    if pid == False:  
        print "No 'iCarRadio' in user's playlists. Create a new one."
        push_to_kinesis(get_data())
        time.sleep(3)
        print "Created playlist 'iCarRadio'."
        pid = get_playlist_id(token)

    lastsong_id = get_lastsong_id(token, pid)
    print "Last song's name is:", get_lastsong_name(token, pid)

    print "Start."
    while True:
        try:
            data = get_data()
            print json.dumps(data, indent=4)
            cursong_id = get_current_song_id(token)
            if cursong_id == lastsong_id:
                push_to_kinesis(data)
                print "Playing the last song. Append new songs to playlist."
                time.sleep(3)   # Wait for new songs coming in
                lastsong_id = get_lastsong_id(token, pid)
                print "Last song's name is:", get_lastsong_name(token, pid)

            time.sleep(5)
        except KeyboardInterrupt:
            print "Quiting..."
            break
