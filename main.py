
from flask import Flask, jsonify, render_template
import json

from flask import jsonify
from flask import Markup

import scrape_mars as scrape_mars
import mongo_mars as mongo_mars

app = Flask(__name__)


#### Home API response ####

@app.route("/")
def home():
    json_dict = mongo_mars.read_DB()

    ## Load html table.
    space_facts_html_file = json_dict['space_facts_html']
    with open(space_facts_html_file, 'r') as myfile:
        data = myfile.read().replace('\n', '')
    
    html_insert = Markup(data)

    return render_template('index.html', mars_data=json_dict, space_facts=html_insert)


#### Scraping API ####

@app.route("/scrape")
def scrape():

    print('[########] Scraping...\n')
    mars_data = scrape_mars.scrape_mars_func()

    print('\n[########] Data scraped.\n')

    print(json.dumps(mars_data, sort_keys=True, indent=4))

    mongo_mars.write_to_db(mars_data)

    json_dict = mongo_mars.read_DB()

    return jsonify(result=json_dict)

@app.route("/data")
def data():

    json_dict = mongo_mars.read_DB()

    return jsonify(result=json_dict)

if __name__ == '__main__':
    app.run(debug=True)