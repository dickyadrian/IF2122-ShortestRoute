	
key = "AIzaSyBvlZ10cXAs93BbX-F5ZnYaWnzKhFPTGcU"

from flask import Flask, render_template, jsonify, url_for, redirect
import requests
import json
from gmplot import gmplot
from math import sin, cos, sqrt, atan2, radians
app = Flask(__name__)



def convertToArray(text):
	points = text[0:(text.find('x'))]
	destinations = text[text.find('y')+1 : ]
	adjacency = text [(text.find('x')+1):(text.find('y')-1-len(destinations))]
	points = points.replace("(", "[")
	points = points.replace(")", "]")
	points = "[" + points + "]"
	destinations = "[" + destinations + "]"
	adjacency = "[" + adjacency + "]"
	dataPoints = json.loads(points)
	dataAdjacency = json.loads(adjacency)
	dataDestinations = json.loads(destinations)
	return (dataPoints, dataAdjacency, dataDestinations)

def buatMatriksJarak(data):
	R = 6373.0

	hubungan = data[0]

	result = []
	temp = []
	i = 0
	while(i < len(hubungan)):
		j = 0
		temp.clear()
		while(j < len(hubungan)):
			x1 = hubungan[i][0]
			y1 = hubungan[i][1]
			x2 = hubungan[j][0]
			y2 = hubungan[j][1]    

			lat1 = radians(float(x1))
			lon1 = radians(float(y1))
			lat2 = radians(float(x2))
			lon2 = radians(float(y2))

			dlon = lon2 - lon1
			dlat = lat2 - lat1

			a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
			c = 2 * atan2(sqrt(a), sqrt(1 - a))

			distance = (-1)*R * c *1000
			temp.append(int(distance))
			j = j+1
		
		temp2 = temp.copy()
		result.append(temp2)
		i = i+1
	i = 0
	adjacency = data [1]
	while(i < len(adjacency)):
		result[adjacency[i]][adjacency[i+1]] = result[adjacency[i]][adjacency[i+1]] * -1
		result[adjacency[i+1]][adjacency[i]] = result[adjacency[i+1]][adjacency[i]] * -1
		i = i+2

	return result 		

@app.route("/")
def retreive():
    return render_template('layout.html') 

@app.route("/sendRequest/<string:query>")
def results(query):
	data = convertToArray(query)
	#Data Adalah tuple, elemen ke 1 adalah list of point, elemen ke 2 adalah list adjacency, elemen ke 3 adalah 
	#list destinasi yang pernah dituju
	matriks = buatMatriksJarak(data)
	# Membuat matriks keterhubungan, simpul yang tidak terhubung jaraknya minus
	print(matriks)
	origin = data[2][len(data[2])-2]
	final = data[2][len(data[2])-1]
	#A* Algorithm here

	hasil = [1,0]
	#Hasil dalam bentuk array urutan jalan

	gmap = gmplot.GoogleMapPlotter(-6.8909,107.6105, 17) # Koordinat pusat, level zoom
	temp = []
	for idx in hasil:
		temp.append((data[0][idx][0], data[0][idx][1]))
	lats,lons =zip(*temp)
	gmap.plot(lats, lons, 'cornflowerblue', edge_width = 10)

	gmap.draw("my_map.html")
	return render_template('mode2.html')

if __name__ ==  "__main__":
    app.run(debug=True)