import flask
from flask import request, jsonify
import json
import os
import sys
import requests

app = flask.Flask(__name__)
gps = {"lat": None,"long":None}
values = {'compass':-180,'location':gps}
science = {'atmospheric_pressure':None,
'air_temperature':None,
'air_humidity':None,
'soil_temperature':None,
'soil_humidity':None,
#'gases':None,
'CO2':None,
'CO':None,
'CH4':None,
'phosphor':None,
'potassium':None,
'nitrogen':None,
'pH':None,
'elevation':None}
retrieval = {'CFL':None,'CFR':None,'CML':None,'CMR':None,'CBL':None,'CBR':None}
coordinates = {"latitude":[],"longitude":[]}
power = None 
string_data = ""
ip = "localhost"
@app.route("/")
def admin_control():
	return flask.render_template("admin_control.html")

@app.route("/retrieval")
def retrieval_task():
	return flask.render_template("retrieval.html")

@app.route("/autonomous")
def autonomous():
	return flask.render_template("autonomous.html")

@app.route("/science")
def science_task():
	return flask.render_template("science_task.html")		
	
@app.route("/ping")
def ping():
	response = os.system("ping -c 1 localhost");
	if(response==0):
		return "Connected"
	else:
		return "Not connected"	

@app.route("/science/set_science")
def set_science():
	global science		
	data_string = request.args.get('json')
	data = json.loads(data_string)
	for key in science:
		science[key] = data[key]
	return science	
	
@app.route("/science/get_science")
def get_science():
    global science
    return jsonify(science)
         	
@app.route("/science/image_stitch")
def image_stitch():
    print("Input locations of three images\n")
    image1 = str(input())
    image2 = str(input())
    image3 = str(input())
    os.system(f"python3 image_stitch.py {image1} {image2} {image3}")
    return "1"    

@app.route("/retrieval/set_retrieval")
def set_retrieval():
    global retrieval
    data_string = request.args.get('json')
    data = json.loads(data_string)
    for key in retrieval:
        retrieval[key] = data[key]
    return retrieval

@app.route("/retrieval/get_retrieval")    
def get_retrieval():
    global retrieval
    return jsonify(retrieval)

@app.route("/retrieval/send_coordinates")
def send_coordinates():
    global coordinates
    #string = request.data
    #print(request.data)
    return ""
            	
@app.route("/set_values")
def set_values():
    global values
    data_string = request.args.get('json')
    data = json.loads(data_string)
    for key in values:
        values[key] = data[key]
    return values

@app.route("/get_values")
def get_values():
    global values
    return jsonify(values)
    
@app.route("/send_values", methods=['GET','POST'])
def send_values():
    global power
    global string_data
    if request.method == "POST":
        global string_data
        string_data = request.data
        data = json.loads(string_data)
    return string_data
	
if __name__ == "__main__":
    app.run(host = ip, debug=True)
