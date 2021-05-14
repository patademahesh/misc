#!/usr/bin/env python

from flask import Flask,request,redirect,Response
import requests
import argparse

parser = argparse.ArgumentParser(description='Metrics exporter proxy.')
parser.add_argument('--port', help="exporter port to listen on")
parser.add_argument('--proxy_host', help="host to forward traffic")
parser.add_argument('--proxy_port', help="port to forward traffic")
args = parser.parse_args()

app = Flask(__name__)
SITE_NAME = 'http://'+ args.proxy_host +':'+ args.proxy_port +'/'

@app.route('/')
def index():
    return 'Go to /metrics'

@app.route('/<path:path>',methods=['GET'])
def proxy(path):
    global SITE_NAME
    if request.method=='GET' and path=='metrics':
        url = SITE_NAME+path
        resp = requests.get(url)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    else:
        return 'Go to /metrics'

if __name__ == '__main__':
    app.run(debug = False,host='0.0.0.0',port=int(args.port))
