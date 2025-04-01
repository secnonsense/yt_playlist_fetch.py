# yt_playlist_fetch.py
Very simple script to download all of your youtube music playlists.  Relies on ytmusicapi. Can also be used to upload to populate playlists

The hardest part is creating the required headers_auth.json file (documented under setup here - https://ytmusicapi.readthedocs.io/en/stable/setup.html). 

pip install ytmusicapi 

run python and then type in the following:  

from ytmusicapi import YTMusic.   

YTMusic.setup(filepath='headers_auth.json')  

Please paste the request headers from Firefox and press Ctrl-D to continue:  

These headers can be grabbed from Developer tools or a proxy (Burp Suite) when access Youtube Music.  

The headers must contain: x-goog-authuser, cookie

**Usage: python yt_playlist_fetch.py [-u]**

To backup all playlists in files named PLAYLISTNAME_playlist.txt: python yt_playlist_fetch.py  

To upload to a playlist: python yt_playlist_fetch.py -u. 

The upload option will prompt for the filename to be uploaded and the playlist id of the playlist to upload to.  The playlist id can be found as part of the URL when viewing the playlist in the web version of Youtube Music.  

Note - There is no error checking for the filename to be uploaded (should be in the same path as the script) or for the playlist Id. If any of the song/video id's to be uploaded are already in the playlist you are uploading to, the script will silently fail.  It is best to upload to a newly created playlist.

This script has a webhook notification to slack to inform a successful backup once daily. There is a function that confirms that a backup of the file was completed successfully within in the last hour. Also there is a function to backup to an s3 bucket as well.  This requires the boto3 and botocore python libraries as well as a bucket name defined in the script in the bucket variable. It also uses the webhook function to notify that the files were copied to s3 successfully once daily (at 8am). 
