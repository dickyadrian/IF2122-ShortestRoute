
key = "AIzaSyBvlZ10cXAs93BbX-F5ZnYaWnzKhFPTGcU"

"""import requests

response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=itb&key='+KEY)
gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13)
resp_json_payload = response.json()

print(resp_json_payload['results'][0]['geometry']['location'])"""

from flask import Flask, render_template, jsonify
import requests
import json
app = Flask(__name__)

global data

search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"

@app.route("/")
def retreive():
    return render_template('layout.html') 

@app.route("/sendRequest/<string:query>")
def results(query):
	query = query.replace("(", "[")
	query = query.replace(")", "]")
	query = "[" + query + "]"
	data = json.loads(query)
	print(data[0])
	return render_template('mode2.html')

@app.route("/nextmode")
def nextmode():
    return render_template('mode2.html', data = data) 

if __name__ ==  "__main__":
    app.run(debug=True)