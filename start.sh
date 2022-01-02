#!/bin/bash

trap ctrl_c INT

function ctrl_c() {
  echo "Quiting ngrok"
  kill -9 `cat ngrok_pid.txt`
  rm ngrok_pid.txt
}

nohup ./ngrok http --region=eu --hostname=addvideo.eu.ngrok.io 5000 > ngrok.log 2>&1 &
echo $! > ngrok_pid.txt
source ./venv/bin/activate
python app.py
