from oauth2client.client import GoogleCredentials
from flask import Flask, jsonify, render_template, request, json
<<<<<<< HEAD
from google.cloud import vision
from google.cloud.vision import types
import requests
=======
import requests, base64

>>>>>>> 937dcdac7e4ea6df8868719ec3117944aefcd8ae
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def process_image():

<<<<<<< HEAD
   path = ""
   """Detects document features in an image."""
   client = vision.ImageAnnotatorClient(key=AIzaSyA-ChOP_rd3Ny2_n8vgQfpY-sViFx3weU0)

   with io.open(path, 'rb') as image_file:
      content = image_file.read()

   image = types.Image(content=content)
   credentials = GoogleCredentials.get_application_default()
=======
   with open("images/sample1.jpg", "rb") as image_file:
       encoded_string = base64.b64encode(image_file.read())

   # filestring = "http://cdn.bluefaqs.netdna-cdn.com/wp-content/uploads/2010/06/Cliff.jpg"
>>>>>>> 937dcdac7e4ea6df8868719ec3117944aefcd8ae

   request = {}
   rtype = {}
   request["image"] = {"content" : encoded_string}
   request["features"] = []
   request["features"].append({"type": "TEXT_DETECTION"})

   payload = {}
   payload["requests"] = []
   payload["requests"].append(request)


   # return 'OK'

   r = requests.post("https://vision.googleapis.com/v1/images:annotate?key=AIzaSyA-ChOP_rd3Ny2_n8vgQfpY-sViFx3weU0", data=json.dumps(payload))
   respjson = json.loads(r.text)
   return json.dumps(respjson)


def send_image(image):
    r = requests.get('https://vision.googleapis.com/v1/images:annotate?key=AIzaSyA-ChOP_rd3Ny2_n8vgQfpY-sViFx3weU0')
    files = {'images': open('1300.jpg', 'rb')}
    requests.post(url, files=files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
