from flask import Flask, jsonify, render_template, request, json
import requests, base64, os
from wit import Wit
import location_info

app = Flask(__name__)

@app.route('/getImage', methods=['POST'])
def getImage():
    image64 = request.json['image']
    msg = get_image_mssg(image64)
    jsonResponse = process_image(msg)
    return jsonResponse


def process_image(message):

#    with open("app/images/sample1.jpg", "rb") as image_file:
#       message = get_image_mssg(base64.b64encode(image_file.read()))

   client = Wit('KL3MRYO3BEEASGTV7SVJF7CT6T2327UH')
   resp = client.message(message)

   jdummy = {}
   jdummy['datetime_from'] = resp['entities']['datetime'][0]['from']['value']
   jdummy['datetime_to'] = resp['entities']['datetime'][0]['to']['value']
   # jdummy['location'] = "512 Mark Wesley Lane, St. Charles OK"
   jdummy['location'] = location_info.extract_location(text)
   jdummy['title'] = "PennApps"

   return jsonify(jdummy)


# Takes byte string and returns a message text
def get_image_mssg(encoded_string):
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
   return respjson['responses'][0]['fullTextAnnotation']['text']


if __name__ == '__main__':
   # Bind to PORT if defined, otherwise default to 5000.
   port = int(os.environ.get('PORT', 5000))
   app.run(host='0.0.0.0', port=port)