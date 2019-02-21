

import scrape_mars as scrape_mars


import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template
from datetime import datetime as dt2

import json

app = Flask(__name__)


#### Home API response ####

@app.route("/")
def home():
    return render_template('index.html')


#### Precipitation API response ####

@app.route("/scrape")
def scrape():

    
    print('scraping')
    mars_data = scrape_mars.scrape_mars()
    print('scrapped')
    #print(mars_data)

    print(json.dumps(mars_data, sort_keys=True, indent=4))
    return 'done'



if __name__ == '__main__':
    app.run(debug=True)