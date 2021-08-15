# yt_playlist_fetch.py
Very simple script to download all of your youtube music playlists.  Relies on ytmusicapi. 

The hardest part is creating the required headers_auth.json file (documented under setup here - https://ytmusicapi.readthedocs.io/en/latest/setup.html). 

pip install ytmusicapi. 

run python and then type in the following:  

from ytmusicapi import YTMusic.   

YTMusic.setup(filepath='headers_auth.json')  

Please paste the request headers from Firefox and press Ctrl-D to continue:  


