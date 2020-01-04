import sys,json,random,time,os,requests

currentValues = [0,0,0,0,0,0]
while(1):
    time.sleep(0.5)
    for i in range(6):
        currentValues[i] = round(random.uniform(2,5),2)
    current_dict = {"CFL":currentValues[0],
                    "CFR":currentValues[1],
                    "CML":currentValues[2],
                    "CMR":currentValues[3],
                    "CBL":currentValues[4],
                    "CBR":currentValues[5]}
    string_data = json.dumps(current_dict)
    r = requests.get("http://localhost:5000/retrieval/set_retrieval?json="+string_data)
