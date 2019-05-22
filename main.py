import sys
import spotipy
import spotipy.util as util
import matplotlib.pyplot as plt
import numpy as np

scope = "playlist-read-private playlist-modify-private playlist-read-collaborative playlist-modify-public"

def getData():
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print ("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    token = util.prompt_for_user_token(username, scope)
    if token:
        sp = spotipy.Spotify(auth=token)
        for playlist in sp.current_user_playlists()['items']:
            if 'Car' in playlist['name']:
                id = playlist['id']

        limit = sp.user_playlist(sp.current_user()['id'], id)['tracks']['total']
        data = []
        offset = 0
        while(offset < limit):
            for track in sp.user_playlist_tracks(sp.current_user()['id'], id, offset=offset)['items']:
                data.append(int(track['track']['album']['release_date'][0:4]))
            offset += 100
        return data
    else:
        print ("Can't get token for", username)

def plot(data):
    minimum = min(data)
    maximum = max(data)
    labels = [f'{minimum+x}' for x in range(maximum-minimum+1)]
    year = minimum
    counted_data = []
    while (year <= maximum):
        counted_data.append(data.count(year))
        year += 1

    index = np.arange(len(labels))
    print(len(labels), len(counted_data))
    plt.bar(labels, counted_data)
    plt.xlabel('Year')
    plt.ylabel('# of Occurrences')
    plt.xticks(index, labels, rotation=90, fontsize=6)
    plt.title('Spotify Tracks by Year Released')
    plt.show()



if __name__ == "__main__":
    data = getData()
    plot = plot(data)
