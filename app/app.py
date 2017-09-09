from flask import Flask, jsonify, render_template, request, json
import requests, base64, os

app = Flask(__name__)


@app.route("/new", methods=['POST', 'GET'])
def process_image():

   print request.json


   with open("app/images/sample1.jpg", "rb") as image_file:
       encoded_string = base64.b64encode(image_file.read())

   img_request = {}
   rtype = {}
   img_request["image"] = {"content" : encoded_string}
   img_request["features"] = []
   img_request["features"].append({"type": "TEXT_DETECTION"})

   payload = {}
   payload["requests"] = []
   payload["requests"].append(img_request)

   r = requests.post("https://vision.googleapis.com/v1/images:annotate?key=AIzaSyA-ChOP_rd3Ny2_n8vgQfpY-sViFx3weU0", data=json.dumps(payload))
   respjson = json.loads(r.text)
   message = respjson['responses'][0]['fullTextAnnotation']['text']

   return message


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
