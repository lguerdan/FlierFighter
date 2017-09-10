import requests, json, re
from flask import jsonify
from wit import Wit
from geopy.geocoders import Nominatim
from dateutil.parser import parse
import auth


def is_date(string):
    try:
        parse(string)
        return True
    except ValueError:
        return False


def process_image(res, message):
   jresp = {}

   message = message.title()
   jresp['title'] = message.split('\N')[0]
   ' '.join(jresp['title'].split())

   descript = message.replace('\N', '\n')
   descript = descript.split('\n')
   print "The number of newlines: " + str(len(descript))
   #Add location if it is valid
   geolocator = Nominatim()
   for d in descript[::-1]:
       d = re.sub('[^a-zA-Z0-9\.]', ' ', d)
       d = re.sub(r'\|', '',  d)
       if d.count(' ') > 0 \
        and not is_date(d) \
        and not re.match('\d{2}:\d{2}:\d{2}', d) \
        and not re.search('\d{1}AM', d) \
        and not re.search('\d{1}PM', d):
           print d
           try:
              location = geolocator.geocode(d)
           except Exception as e:
              pass
           if location:
               if location.longitude < -30.0:
                   jresp['location'] = location.address
                   print "address is: " + location.address
                   break

   try:
      client = Wit(auth.wit_key)
      resp = client.message(message)
   except Exception as e:
      return jsonify({'error': 'Failed to parse image response. Request may be too long.'})

   # Add time info
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

   request_string = 'https://vision.googleapis.com/v1/images:annotate?key=' + auth.vision_key
   r = requests.post(request_string, data=json.dumps(payload))
   res = json.loads(r.text)

   return res