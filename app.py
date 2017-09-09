from flask import Flask, jsonify, render_template, request, json
import requests, base64, os, re
from wit import Wit
import location_info

app = Flask(__name__)

# Temp allow get for dev settings
@app.route('/getImage', methods=['POST', 'GET'])
def getImage():
   if request.method == 'POST':
      print request.json
      image64 = request.json['image']
      msg = get_image_mssg(image64)
   else:
      with open("app/images/train1.jpg", "rb") as image_file:
         msg = get_image_mssg(base64.b64encode(image_file.read()))

   jsonResponse = process_image(msg)
   return jsonResponse


def process_image(message):

   client = Wit('KL3MRYO3BEEASGTV7SVJF7CT6T2327UH')
   resp = client.message(message)

   try:
      jdummy = {}
      jdummy['location'] = "107 Temp Drive, St. Louis, MO"
      jdummy['title'] = "PennApps"
      jdummy['datetime_from'] = resp['entities']['datetime'][0]['from']['value']
      jdummy['datetime_to'] = resp['entities']['datetime'][0]['to']['value']

   # If a range isn't provided
   except KeyError as e:
      jdummy['datetime_from'] = resp['entities']['datetime'][0]['values'][0]['value']
      jdummy['datetime_to'] = resp['entities']['datetime'][0]['values'][0]['value']

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
   message = respjson['responses'][0]['fullTextAnnotation']['text']
   return re.sub('[^a-zA-Z0-9\.]', ' ', message)


if __name__ == '__main__':
   # Bind to PORT if defined, otherwise default to 5000.
   port = int(os.environ.get('PORT', 5000))
   app.run(host='0.0.0.0', port=port)