import requests
import json

def send_request(url, method, payload=None, headers=None):
    print method + " " +url
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    #print data 
    if method == "GET":
        r = requests.get(url, headers=headers)
    elif method == "POST":
        r = requests.post(url, data=data, headers=headers)
    elif method == "PUT":
        r = requests.put(url, data=data, headers=headers)
    elif method == "DELETE":
        r = requests.delete(url, data=data, headers=headers)
    if r.status_code != requests.codes.ok or r.status_code != 210: 
        r.raise_for_status()
    return r
