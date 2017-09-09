from flask import Flask, jsonify, render_template, request, json
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def process_image():
    """Process image"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
