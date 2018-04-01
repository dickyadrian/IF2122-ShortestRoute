
key = "AIzaSyB1mfNCMMsONkubGOCkM64a1PzGDwEiNaA"

"""import requests

response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=itb&key='+KEY)
gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13)
resp_json_payload = response.json()

print(resp_json_payload['results'][0]['geometry']['location'])"""

from flask import Flask, render_template, jsonify
import requests
app = Flask(__name__)

search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"

@app.route("/", methods=["GET"])
def retreive():
    return render_template('layout.html') 

@app.route("/sendRequest/<string:query>")
def results(query):
	search_payload = {"key":key, "query":query.replace("(","").replace(")","")}
	search_req = requests.get(search_url, params=search_payload)
	search_json = search_req.json()

	place_id = search_json["results"][0]["place_id"]

	details_payload = {"key":key, "placeid":place_id}
	details_resp = requests.get(details_url, params=details_payload)
	details_json = details_resp.json()

	url = details_json["result"]["url"]
	return jsonify({'result' : url})


if __name__ ==  "__main__":
    app.run(debug=True)