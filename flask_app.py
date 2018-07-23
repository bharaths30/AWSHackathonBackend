#!flask/bin/python
from flask import Flask, jsonify, request
import dnn_classifier as dnn
import urllib
import os
import hashlib

basePath = "/usr/src/app/images"
app = Flask(__name__)


imageTags = [
  {
    'url' : "bit.ly/asrfdr",
    'tags' : ["car", "vehicle"]
  },
  {
    'url' : "bit.ly/rjifmrfm",
    'tags' : ["dog", "animal"]
  }
]

def downloadImage(imageUrl):
  filename = hashlib.md5(imageUrl.encode('utf-8')).hexdigest().upper()
  urllib.urlretrieve(imageUrl, os.path.join(basePath, filename))
  return filename

@app.route('/', methods=["GET"])
def testMethod():
  print "inside index method"
  return jsonify({"key": "value"})

@app.route('/todo/api/v1/results', methods=['POST'])
def index():
  imageTags = []
  # print "Request received"
  data = request.get_json()
  urls = data["url"]
  url_list = urls.split(",")
  # print ("Request", url_list)
  for url in url_list:
    imageName = downloadImage(url)
    tags = dnn.classifyImage(os.path.join(basePath, imageName))
    imageTags.append({'url': url, 'tags': tags})
    os.remove(os.path.join(basePath, imageName))
  return jsonify({'imageTags': imageTags})

if __name__ == '__main__':
  app.run(host="0.0.0.0")
