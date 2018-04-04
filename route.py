	
key = "AIzaSyBvlZ10cXAs93BbX-F5ZnYaWnzKhFPTGcU"

from flask import Flask, render_template, jsonify, url_for, redirect
import requests
import json
from queue import PriorityQueue
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

def a_star(adj_matrix, start_node_idx, end_node_idx):
    open_nodes = [start_node_idx]
    closed_nodes = []
    f_costs = PriorityQueue()
    g_costs = [0 for _ in range(len(adj_matrix))]
    path = []
    result = 0

    current_node_idx = start_node_idx
    g_costs[current_node_idx] = 0

    while len(open_nodes)>0:
        print("Checking node :", current_node_idx)
        print("Path to node :", path)
        # Simpul yang diperiksa adalah simpul tujuan, maka pencarian selesai
        if current_node_idx == end_node_idx:
            print("Done!\n")
            path.append(current_node_idx)
            break
        # Simpul yang diperiksa bukanlah simpul tujuan, lakukan perhitungan A*
        else:
            # Tandai simpul yang sedang diperiksa sebagai "sudah dikunjungi"
            open_nodes.remove(current_node_idx)
            closed_nodes.append(current_node_idx)
            # Bangkitkan semua tetangga yang belum dikunjungi
            for neighbour_idx in range(len(adj_matrix[current_node_idx])):
                if adj_matrix[current_node_idx][neighbour_idx]>0 and not(neighbour_idx in closed_nodes) :
                    open_nodes.append(neighbour_idx)
                    temp_path = path.copy()
                    temp_path.append(current_node_idx)
                    g_costs[neighbour_idx] = g_costs[current_node_idx] + adj_matrix[current_node_idx][neighbour_idx]
                    f_costs.put((g_costs[neighbour_idx] + abs(adj_matrix[neighbour_idx][end_node_idx]), neighbour_idx, temp_path))

            # Pilih simpul berikutnya yang akan diperiksa (yang memiliki nilai f_cost terkecil)
            f_cost_min = f_costs.get()
            print("Current distance :", g_costs[current_node_idx])
            print("Next f_cost_min :", f_cost_min)
            print()
            result = g_costs[current_node_idx]
            path = f_cost_min[2]
            current_node_idx = f_cost_min[1]

    return result, path

@app.route("/")
def retrieve():
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

	jarak = 0
	path = []
	#Hasil dalam bentuk array urutan jalan
	jarak, path = a_star(matriks, origin, final)
	print("Hasil :")
	print("   Jalur:", path)
	print("   Jarak :", jarak)

	gmap = gmplot.GoogleMapPlotter(-6.8909, 107.6105, 17) # Koordinat daerah ITB, level zoom
	#gmap = gmplot.GoogleMapPlotter(-6.921871, 107.607060, 18) # Koordinat daerah alun-alun, level zoom
	temp = []
	for idx in path:
		temp.append((data[0][idx][0], data[0][idx][1]))
	lats,lons =zip(*temp)
	gmap.plot(lats, lons, 'cornflowerblue', edge_width = 10)

	gmap.draw("my_map.html")
	return render_template('mode2.html')

if __name__ ==  "__main__":
    app.run(debug=True)