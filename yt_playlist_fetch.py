from ytmusicapi import YTMusic

ytmusic = YTMusic('headers_auth.json')

playlists=ytmusic.get_library_playlists(ytmusic)

y=0
while y < len(playlists):
    pl_name=playlists[y]['title']
    playlist=playlists[y]['playlistId']
    

    my_playlist=ytmusic.get_playlist(playlist,400)

    file=pl_name+"_playlist.txt"
    print(f"\nWriting Playlist {pl_name} to file {file}...")
    
    x=0
    with open(file, 'w') as output:
        while x < len(my_playlist['tracks']):    
            #print(my_playlist['tracks'][x]['title'] + " - " + my_playlist['tracks'][x]['artists'][0]['name'])
            output.write(my_playlist['tracks'][x]['title'] + " - " + my_playlist['tracks'][x]['artists'][0]['name']+"\n")
            x+=1
    y+=1
