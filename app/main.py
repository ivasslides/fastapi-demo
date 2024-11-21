#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import json
import os
import mysql.connector
from mysql.connector import Error


DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "ds2022"
DBPASS = os.getenv('DBPASS')
DB = "fbv2sc"

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def zone_apex():
    return {"testing": "done"}


@app.get('/genres')
def get_genres():
    db = mysql.connector.connent(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
    cur = db.cursor()
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}
    finally: 
        cur.close()
        db.close()

@app.get('/songs')
def get_songs(): 
    db = mysql.connector.connect(suer=DBUSER, host=DBHOST, password=DBPASS, database=DB)
    cur = db.cursor()
    query = "SELECT songs.title, songs.album, songs.artist, songs.year, songs.file AS file, songs.image AS image, songs.genre, genres.genre FROM songs JOIN genres WHERE songs.genre = genres.genreid;"
    try: 
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e: 
        return {"Error": "MySQL Error: " + str(e)}
    finally: 
        cur.close()
        db.close() 





