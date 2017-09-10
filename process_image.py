import requests, json, re
from flask import jsonify
from wit import Wit
from geopy.geocoders import Nominatim

def process_image(message):
   jresp = {}

   message = message.title()
   jresp['title'] = message.split('\n')[0]
   ' '.join(jresp['title'].split())

   #Add location if it is valid
   geolocator = Nominatim()
   for line in message.split('\n')[1:]:
      try:
         location = geolocator.geocode(line)
         if(location):
            jresp['location'] = location.address

      except Exception as e:
         pass

   try:
      client = Wit('KL3MRYO3BEEASGTV7SVJF7CT6T2327UH')
      resp = client.message(message)
   except Exception as e:
      return jsonify({'error': 'Failed to parse image response. Request may be too long.'})

   #Add time info
   jresp['datetime_from'] = ""
   jresp['datetime_to'] = ""
   try:
      if('datetime' in resp['entities']):
         try:
            first = resp['entities']['datetime'][0]
            if ('values' in first and len(first['values']) > 0):

               jresp['datetime_from'] = resp['entities']['datetime'][0]['values'][0]['value']
            else:
               jresp['datetime_from'] = resp['entities']['datetime'][0]['value']

         except KeyError as e:
            jresp['datetime_from'] = resp['entities']['datetime'][0]['from']['value']
            jresp['datetime_to'] = resp['entities']['datetime'][0]['to']['value']

      else:
         jresp['datetime_from'] = resp['entities'][0]['value'][0]['value']
         jresp['datetime_from'] = resp['entities'][0]['value'][0]['value']

   except Exception as e:
         jresp['datetime_from'] = ""
         jresp['datetime_from'] = ""

   if('location' not in jresp):
      #Add location if not already set
      if('location' in resp['entities']):
         jresp['location'] = resp['entities']['location'][0]['value']
      elif('local_search_query' in resp['entities']):
         jresp['location'] = resp['entities']['local_search_query'][0]['value']
      else:
         jresp['location'] = ""

   # Sanatize input
   re.sub('[^a-zA-Z0-9\.]', ' ', jresp['location'])
   ' '.join(jresp['location'].split())

   re.sub('[^a-zA-Z0-9\.]', ' ', jresp['datetime_from'])
   ' '.join(jresp['datetime_from'].split())

   re.sub('[^a-zA-Z0-9\.]', ' ', jresp['datetime_to'])
   ' '.join(jresp['datetime_to'].split())

   print jresp
   return jsonify(jresp)

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
   res = json.loads(r.text)

   return res