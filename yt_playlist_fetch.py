from ytmusicapi import YTMusic
import argparse

ytmusic = YTMusic('headers_auth.json')

def archive_playlists():
    playlists=ytmusic.get_library_playlists(ytmusic)

    y=0
    while y < len(playlists):
        pl_name=playlists[y]['title']
        playlist=playlists[y]['playlistId']


        my_playlist=ytmusic.get_playlist(playlist,1400)

        file=pl_name+"_playlist.txt"
        print(f"\nWriting Playlist {pl_name} to file {file}...")

        x=0
        with open(file, 'w') as output:
            while x < len(my_playlist['tracks']):    
                #print(my_playlist['tracks'][x]['title'] + " - " + my_playlist['tracks'][x]['artists'][0]['name'])
                output.write(my_playlist['tracks'][x]['title'].replace(',', '') + "," + my_playlist['tracks'][x]['artists'][0]['name'].replace(',', '')+"," + my_playlist['tracks'][x]['videoId'] + "\n")
                x+=1
        y+=1
        
def read_playlist_archive():
    songs=[]
    file=input("Input Filename to upload: ")
    with open(file, 'r') as upload:
        for content in upload:
            values=content.split(',')
            songs.append(values[2].strip())
    return songs
        
def upload_to_playlist(songs):
    playlist=input("Input Playlist ID to upload to: ")
    ytmusic.add_playlist_items(playlist.strip(),songs)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--upload", help="Choose if uploading songs from a playlist archive file", action="store_true")
    return parser.parse_args()

def main():
    args=parse_args()
    if args.upload:
        songs=read_playlist_archive()
        upload_to_playlist(songs)
    else:
        archive_playlists()

if __name__ == "__main__":
    main()
