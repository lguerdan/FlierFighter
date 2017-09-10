from flask import Flask, jsonify, render_template, request, json
import requests, base64, os, re
from wit import Wit
import location_info
import extraData
from geopy.geocoders import Nominatim
from dateutil.parser import parse



app = Flask(__name__)


# Temp allow get for dev settings
@app.route('/getImage', methods=['POST', 'GET'])
def getImage():

   if request.method == 'POST':
      message = json.dumps(request.json['imageData'].encode("utf-8"))

   else:
      image_file = "app/images/" + request.args.get('file')
      with open(image_file, "rb") as image_file:
         message = get_image_mssg(base64.b64encode(image_file.read()))
         res = message
         try:
            # print json.dumps(json.loads(message), indent=4)
            # print json.dumps(message)
            message = message['responses'][0]['fullTextAnnotation']['text']
            # print message
         except Exception as e:
            return message

   re.sub('[^a-zA-Z0-9\.]', ' ', message)
   message = message.replace('\n', ' ').replace('\r', '')
   # print message

   # jsonResponse = process_image(location_info.reduce_text(message))
   # jsonResponse = process_image(message, res)
   jsonResponse = process_image(location_info.reduce_text(message), res)
   return jsonResponse


def is_date(string):
    try: 
        parse(string)
        return True
    except ValueError:
        return False


def process_image(message, res):
   try:
      client = Wit('KL3MRYO3BEEASGTV7SVJF7CT6T2327UH')
      resp = client.message(message)
   except Exception as e:
      return jsonify({'error': 'Failed to parse image response. Request may be too long.'})
   # break message into parts based on newline
   jresp = {}
#    messages = message.splitlines()
   geolocator = Nominatim()
   print "Entering loop"
   responses = res['responses'][0]
   textT = responses['textAnnotations']
   num = 1
   descript = textT[0]['description']
   descript = descript.split('\n')
   for d in descript[::-1]:
       d = re.sub('[^a-zA-Z0-9\.]', ' ', d)
       d = re.sub(r'\|', '',  d)
       if d.count(' ') > 0 \
        and not is_date(d) \
        and not re.match('\d{2}:\d{2}:\d{2}', d) \
        and "PM" not in d \
        and "AM" not in d:
           print d
           location = geolocator.geocode(d)
           if location:
               if location.longitude < -30.0:
                   jresp['location'] = location.address
                   print "address is: " + location.address
                   break
#    for elm in textT:
#        descript = elm['description']
#        print descript
#        print num
#        num += 1
       #print descript.find(' ')
       # #print descript
       # descript = descript.split('\n')
       '''
       for d in descript:
           print d
           if d.count(' ') > 0 and len(d) > 3:
               location = geolocator.geocode(d)
               if location:
                   jresp['location'] = location.address
                   print "address is: " + location.address
                   break
        '''

#    for m in messages:
#        print m, '\n'
#        print '\n'
#        location = geolocator.geocode(m)
#        if location:
#            jresp['location'] = location.address
#            print "address is: " + location.address
#            break

   jresp['datetime_from'] = ""
   jresp['datetime_to'] = ""
   # print resp['entities']
   #Add time info
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

      # finally:
      #    jresp['datetime_from'] = ""
      #    jresp['datetime_to'] = ""


   else:
      jresp['datetime_from'] = resp['entities'][0]['value'][0]['value']
      jresp['datetime_from'] = resp['entities'][0]['value'][0]['value']


   #Add location
#    if('location' in resp['entities']):
#       jresp['location'] = resp['entities']['location'][0]['value']
#    elif('local_search_query' in resp['entities']):
#       jresp['location'] = resp['entities']['local_search_query'][0]['value']
#    else:
#       jresp['location'] = ""

   #Add event name
   if('message_subject' in resp['entities'] ):
      jresp['title'] = resp['entities']['message_subject'][0]['value']
   else:
      jresp['title'] = ""

   # print jresp
   return jsonify(jresp)

@app.route('/confirmation', methods=['POST', 'GET'])
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
#    responses = res['responses'][0]
#    textT = responses['textAnnotations']
#    for elm in textT:
#        print elm['description']
   return res


if __name__ == '__main__':
   # Bind to PORT if defined, otherwise default to 5000.
   port = int(os.environ.get('PORT', 5000))
   app.run(host='0.0.0.0', port=port)