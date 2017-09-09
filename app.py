from flask import Flask, jsonify, render_template, request, json
import requests, base64, os, re
from wit import Wit
import location_info

app = Flask(__name__)

UPLOAD_FOLDER = '/app/images/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Temp allow get for dev settings
@app.route('/getImage', methods=['POST', 'GET'])
def getImage():

   if request.method == 'POST':
      print request.form
      message = json.dumps(request.form['imageData'])

   else:
      image_file = "app/images/train4.jpg"
      with open(image_file, "rb") as image_file:
         message = get_image_mssg(base64.b64encode(image_file.read()))

         try:
            message = message['responses'][0]['fullTextAnnotation']['text']
         except Exception as e:
            return message

   re.sub('[^a-zA-Z0-9\.]', ' ', message)
   jsonResponse = process_image(message)
   return jsonResponse


def process_image(message):
   print message
   client = Wit('KL3MRYO3BEEASGTV7SVJF7CT6T2327UH')
   resp = client.message(message)
   print resp
   jresp = {}
   jresp['datetime_from'] = ""
   jresp['datetime_to'] = ""

   #Add time info
   if('datetime' in resp['entities']):
      try:
         jresp['datetime_from'] = resp['entities']['datetime'][0]['values'][0]['value']

      except KeyError as e:
         jresp['datetime_from'] = resp['entities']['datetime'][0]['from']['value']
         jresp['datetime_to'] = resp['entities']['datetime'][0]['to']['value']

   else:
      jresp['datetime_from'] = resp['entities'][0]['value'][0]['value']


   #Add location
   if('location' in resp['entities']):
      jresp['location'] = resp['entities']['location'][0]['value']
   elif('local_search_query' in resp['entities']):
      jresp['location'] = resp['entities']['local_search_query'][0]['value']
   else:
      jresp['location'] = ""

   #Add event name
   if('message_subject' in resp['entities'] ):
      jresp['title'] = resp['entities']['message_subject'][0]['value']
   else:
      jresp['title'] = ""

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


if __name__ == '__main__':
   # Bind to PORT if defined, otherwise default to 5000.
   port = int(os.environ.get('PORT', 5000))
   app.run(host='0.0.0.0', port=port)