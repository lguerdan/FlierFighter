from flask import Flask, jsonify, render_template, request, json
import requests, base64, os, re
from wit import Wit
import location_info

app = Flask(__name__)


'''Receives confirmation from app'''
@app.route('/confirmation', methods=['POST'])
def confirmation():
    '''Use confirmation data'''
    '''Get weather data'''
    '''Get Lyft data, etc...'''
    if request.method == 'POST':
        current_location = request['currLocation']
        dest_location = request['location']
        start_time = request['datetime_from']
        response = {}
        weather_info = extraData.getWeatherData(dest_location, start_time)
        if weather_info:
            response['weather'] = \
                weather_info
        else:
            response['weather'] = {}
        lyft_info = extraData.getLyftData(dest_location, current_location)
        if lyft_info:
            response['lyft'] = \
                lyft_info
        else:
            response['lyft'] = {}
    return response

   jsonResponse = process_image(msg)
   return jsonResponse

@app.route('/getImage', methods=['POST', 'GET'])
def getImage():
    if request.method == 'POST':
        image64 = request.json['image']
        msg = get_image_mssg(image64)
        jsonResponse = process_image(msg)
        return jsonResponse
    else:
        msg = "HELLO MAY 1 AT 192 DRYDEN AVENUE"
        return location_info.extract_location(msg)


def process_image(message):

def process_image(message):

   print message
   client = Wit('KL3MRYO3BEEASGTV7SVJF7CT6T2327UH')
   resp = client.message(message)
   print resp

   try:
      jdummy = {}
      jdummy['location'] = "107 Temp Drive, St. Louis, MO"
      jdummy['title'] = "PennApps"
      jdummy['datetime_from'] = resp['entities']['datetime'][0]['from']['value']
      jdummy['datetime_to'] = resp['entities']['datetime'][0]['to']['value']

   jdummy = {}
   jdummy['datetime_from'] = resp['entities']['datetime'][0]['from']['value']
   jdummy['datetime_to'] = resp['entities']['datetime'][0]['to']['value']
   # jdummy['location'] = "512 Mark Wesley Lane, St. Charles OK"
   jdummy['location'] = location_info.extract_location(message)
   jdummy['title'] = "PennApps"
   jdummy['people'] = get_human_names(message)
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
