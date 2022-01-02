#!/usr/bin/env python
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
from importlib import import_module
import os
from wifi import Cell, Scheme
from flask import Flask, render_template, Response, request, jsonify, make_response

from camera_pi import Camera

# ----- Button activator code -----
import RPi.GPIO as GPIO
import requests

def request_camera():
    print('button pressed')
    requests.get("http://localhost:5000/video_feed")

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 36 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(36,GPIO.RISING,callback=request_camera) # Setup event on pin 36 rising edge
# --------------------------------

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    data = {}
    data["send_email"] = os.getenv('SEND_EMAIL')
    data["sender_email"] = os.getenv('SENDER_EMAIL')

    return render_template('index.html', data=data)


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/wifi', methods=['GET', 'POST'])
def get_wifi():
    if request.method == 'GET':
        connections = Cell.all('wlan0')
        ssids = []
        for connection in connections:
            ssids.append(connection.ssid)
            print(connection)
        return jsonify(data=ssids)

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', threaded=True)
    finally:
        GPIO.cleanup() # Clean up
