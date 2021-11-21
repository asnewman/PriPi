# PriPi Camera System
A privacy-focused camera system using Raspberry Pi hardware.

Base code forked from [miguelgrinberg/flask-video-streaming](https://github.com/miguelgrinberg/flask-video-streaming).

## Running
### Prerequisites
- Python 3.6+
- virtualenv
- Install OpenCV on your RaspberryPi - [instructions](https://gist.github.com/asnewman/9da37388183189bf022fd1de45609372)
### New installation
1. Clone code: `git clone https://github.com/asnewman/PriPi.git`
1. `cd` into the new directory and start a new virtualenv: `python3 -m venv ./venv`
1. `source ./venv/bin/activate`
1. `pip install -r requirements.txt`
1. Update `.env` with the appropriate values
1. `deactivate`
1. `./start.sh` (if that doesn't work run `chmod 777 ./start.sh`
