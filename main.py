
from flask import Flask, jsonify, render_template
import json

from flask import jsonify

import scrape_mars as scrape_mars
import mongo_mars as mongo_mars

app = Flask(__name__)


#### Home API response ####

@app.route("/")
def home():
    return render_template('index.html')


#### Scraping API ####

@app.route("/scrape")
def scrape():

    print('[########] Scraping...\n')
    mars_data = scrape_mars.scrape_mars()

    print('\n[########] Data scraped.\n')

    print(json.dumps(mars_data, sort_keys=True, indent=4))

    mongo_write.write_to_db(mars_data)

    return json.dumps(mars_data, sort_keys=True, indent=4)

@app.route("/data")
def data():

    json_dict = mongo_write.read_DB()

    return jsonify(result=json_dict)

if __name__ == '__main__':
    app.run(debug=True)