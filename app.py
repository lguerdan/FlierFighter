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
      if 'file' not in request.files:
            return jsonify({"error": "no file specified"})

      file = request.files['file']
      if file and allowed_file(file.filename):
         file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
         image_file = file.filename

   else:
      image_file = "app/images/train4.jpg"

   with open(image_file, "rb") as image_file:
      msg = get_image_mssg(base64.b64encode(image_file.read()))

   jsonResponse = process_image(msg)
   return jsonResponse


def process_image(message):

   client = Wit('KL3MRYO3BEEASGTV7SVJF7CT6T2327UH')
   resp = client.message(message)
   jresp = {}
   print json.dumps(resp)

   #Add time info
   try:
      jresp['datetime_from'] = resp['entities']['datetime'][0]['from']['value']
      jresp['datetime_from'] = extract_hours(resp['entities']['datetime'][0]['from'])
      jresp['datetime_to'] = resp['entities']['datetime'][0]['to']['value']
      jresp['datetime_to'] = extract_hours(resp['entities']['datetime'][0]['to'])

   except KeyError as e:
      jresp['datetime_from'] = resp['entities']['datetime'][0]['values'][0]['value']
      jresp['datetime_to'] = resp['entities']['datetime'][0]['values'][0]['value']

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


def extract_hours(timearr):
   print timearr

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