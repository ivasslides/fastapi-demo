#!/usr/bin/env python3

#library to build a thing, have to import the package
from fastapi import FastAPI
from typing import Optional
#pydantic allows us to create a model of the data
from pydantic import BaseModel

import json
import os

#instantiate the application (create an instance)
app = FastAPI()

#two endpoints for the api
#using get method (pulling the data)
@app.get("/")  # zone apex
#function that takes no parameters
def zone_apex():
    return {"Hello": "Iliana"}

#another get method
@app.get("/add/{a}/{b}")
#function called add takes two parameters of integers
def add(a: int, b: int):
#returns value of the sum of a + b
    return {"sum": a + b}

#creating another endpoint
@app.get("/multiply/{c}/{d}")
def multiply(c: int, d: int):
    return {"product": c * d}

#for lab 6, adding endpoint
@app.get("/bday/{e}")
def bday(e:str):
    return{"birthday": e}

#adding another
@app.get("/hey")
def hey(): 
    return{"wassup": "shawty"}

#adding one last one
@app.get("/bye")
def bye():
    return{"goodbye": "see ya, adios, later gator"}

