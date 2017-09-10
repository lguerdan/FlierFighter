from flask import Flask, jsonify, render_template, request, json
import requests, base64, os, re
from wit import Wit
from geopy.geocoders import Nominatim
from dateutil.parser import parse

import location_info, extraData, process_image


app = Flask(__name__)

# Temp allow get for dev settings
@app.route('/getImage', methods=['POST', 'GET'])
def getImage():
   if request.method == 'POST':
      message = json.dumps(request.json['imageData'].encode("utf-8"))

   else:
      image_file = "app/images/" + request.args.get('file')
      with open(image_file, "rb") as image_file:
         message = process_image.get_image_mssg(base64.b64encode(image_file.read()))
         res = message

         try:
            message = message['responses'][0]['fullTextAnnotation']['text']

         except Exception as e:
            return message

   jsonResponse = process_image.process_image(res, message)
   return jsonResponse


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

if __name__ == '__main__':
   # Bind to PORT if defined, otherwise default to 5000.
   port = int(os.environ.get('PORT', 5000))
   app.run(host='0.0.0.0', port=port)