from ytmusicapi import YTMusic
import argparse
import requests
import sys
import json
import os
import boto3
from pathlib import Path
from datetime import datetime,timedelta
from botocore.exceptions import ClientError

ytmusic = YTMusic('/opt/yt_playlist/headers_auth.json')

def check_token():
    if os.path.exists(Path.home() / ".slack"):
        with open(Path.home() / ".slack") as f:
            my_variable=f.readlines()[0].strip('\n\r')
            return my_variable
    else:
        print(f"\nThis script requires .slack file with the slack webhook url and it must be stored in {Path.home()}/.slack \n")
        quit()

def webhook(uri,message):
    title = "YouTube Playlist Backup!"
    colors={"blue": "#142954","yellow": "#FFFF00","red": "#FF0000", "hotpink": "#FF00FF","green": "#85FF7A"}
    color=colors['red']
    body = json.dumps({"pretext": title, "text": message, "color": color})
    try:
        r = requests.post(uri, data=body, headers={"Content-type": "application/json"})
        if r.status_code != 200:
            sys.stderr.write(f"Response code: {r.status_code} {r.text} \n {r.__dict__} \n")
        else:
            print(r.text)
    except Exception as error:
            sys.stderr.write("Exception occurred retrieving data from slack API:. Error Code: {}\n".format(error))

def check_timestamp(file):
    mtime = os.path.getmtime(file)
    mtime_datetime = datetime.fromtimestamp(mtime)
    now = datetime.now()
    print("Modification time:", mtime_datetime)
    difference = now - mtime_datetime
    if difference < timedelta(hours=1):
        print("less than an hour - so backup was successful")
        less=True
    else:
        less=False
    return less, mtime_datetime
    
def backup_to_s3(pl_name,file,uri):
    s3 = boto3.resource('s3')
    dest=f"yt_backup/{pl_name}_playlist.txt"
    bucket="MYBUCKET"
    try:
        s3.meta.client.upload_file(file, bucket, dest)
        message=f"Filepath '{file}' successfully backed up to {bucket}"
        webhook(uri,message)
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            message=f"Filepath '{file}' does not exist in {bucket}"
            webhook(uri,message)
        else:
            message=f"Error checking object: {e}"
            webhook(uri,message)

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
        less,mtime=check_timestamp(file)
        message=f"\nWriting Playlist {pl_name} to file {file} timestamp: {mtime}..."
        print(message)
        if datetime.now().hour==8 and less:
            webhook(uri,message)
            backup_to_s3(pl_name,file,uri)
            print(f"Timestamp {mtime} is less than one hour for {file} so it was recently backed up!")
            
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
