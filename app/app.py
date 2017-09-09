from flask import Flask, jsonify, render_template, request, json
import requests, base64

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def process_image():

   with open("images/sample1.jpg", "rb") as image_file:
       encoded_string = base64.b64encode(image_file.read())

   # filestring = "http://cdn.bluefaqs.netdna-cdn.com/wp-content/uploads/2010/06/Cliff.jpg"

   request = {}
   rtype = {}
   request["image"] = {"content" : encoded_string}
   request["features"] = []
   request["features"].append({"type": "TEXT_DETECTION"})

   payload = {}
   payload["requests"] = []
   payload["requests"].append(request)


   # return 'OK'

   r = requests.post("https://vision.googleapis.com/v1/images:annotate?key=AIzaSyA-ChOP_rd3Ny2_n8vgQfpY-sViFx3weU0", data=json.dumps(payload))
   respjson = json.loads(r.text)
   return json.dumps(respjson)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
