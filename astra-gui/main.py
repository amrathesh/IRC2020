import flask
from flask import request, jsonify
import json
import os
import sys


app = flask.Flask(__name__)
battery_level = 100
compass = -180
gps = {"lat": None,"long":None}
values = {'battery':battery_level,'compass':compass,'location':gps}
@app.route("/")
def admin_control():
	return flask.render_template("admin_control.html")

@app.route("/retrieval")
def retrieval():
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
	
@app.route("/set_values")
def set_values():
    global values
    data_string = request.args.get('json')
    data = json.loads(data_string)
    values['battery'] = data['battery']
    values['compass'] = data['compass']
    values['location'] = data['location']
    return values

@app.route("/get_values")
def get_values():
    global values
    battery_level = values['battery']
    compass = values['compass']
    gps = values['location']
    return jsonify(values)
	

if __name__ == "__main__":
    app.run(host = 'localhost', debug=True)
