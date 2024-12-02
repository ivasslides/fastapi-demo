import os
import json
import mysql.connector
import boto3
from chalice import Chalice

app = Chalice(app_name='pacman')
app.debug = True


#s3 things
S3_BUCKET = 'fbv2sc-dp1-spotify'
s3 = boto3.client('s3')

#base url
baseurl = 'http://fbv2sc-dp1-spotify.s3-website-us-east-1.amazonaws.com'

#database things 
DBHOST = os.getenv('DBHOST')
DBUSER = os.getenv('DBUSER')
DBPASS = os.getenv('DBPASS')
DB = os.getenv('DB')
db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur = db.cursor()

#file extenstions
_SUPPORTED_EXTENSIONS = (
    '.json'
)


#ingestor lambda function
@app.on_s3_event(bucket=S3_BUCKET, events=['s3:ObjectCreated:*'])
def s3_handler(event):
    if _is_json(event.key):
       #get the file, read it, and load it into JSON as an object
       response = s3.get_object(Buecket=S3_BUCKET, Key=event.key)
       text = response["Body"].read().decode()
       data = json.loads(text)

       #parse the data fields 1 by 1 from 'data'
       TITLE = data.get('title', 'unknown')
       ALBUM = data.get('album', 'unknown')
       ARTIST = data.get('artist', 'unknown')
       YEAR = data.get('year', 'unknown')
       GENRE = data.get('genre', 'unknown')

       #get unique ID for the bundle for mp3 and image
       keyhead = event.key
       identifier = keyhead.split('.')
       ID = identifier[0]
       MP3 = baseurl + ID + '.mp3'
       IMG = baseurl + ID + '.jpg'

       app.log.debug("Received new song: %s, key: %s", event.bucket.event.key)

       #try inserting song
       try:
         add_song = ("INSERT INTO songs "
               "(title, album, artist, year, file, image, genre) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")
         song_vals = (TITLE, ALBUM, ARTIST, YEAR, MP3, IMG, GENRE)
         cur.execute(add_song, song_vals)
         db.commit()

       except mysql.connector.Error as err:
         app.log.error("Failed to insert song: %s", err)
         db.rollback()

#perform suffix match against supported extensions
def _is_json(key):
   return key.endswith(_SUPPORTED_EXTENSIONS)
