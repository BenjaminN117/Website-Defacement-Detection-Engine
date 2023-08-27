# Website Defacement Detection Engine

![Static Badge](https://img.shields.io/badge/Python-=>3.11.0-blue)
![Static Badge](https://img.shields.io/badge/Docker-=>20.10.22-blue)
![Static Badge](https://img.shields.io/badge/License-GPL3.0-yellow)
 
## Description

This is an automated defacement detection engine, it allows the web code running on a public server to be compared known correct code stored in an S3 bucket. This allows for rapid detection when websites are defaced and works with the AWS SES system to send notification emails to select users to inform them within minutes of the website being defaced. Along with this it provides a sample of the code that was modified by a potiential threat actor.

### Data Generated

- Time of detection
- Domain of server
- Code that has been modified compared to original code

### Future Improvements

- Begin a redployment process for defaced websites, so they automatically correct themselves
- Integrate with Git so the code doesn't have to be copied into an S3 bucket, it automatically pulls is from Git, meaning the most up to date code from production is being checked
- Get the IP address of the server

## Prerequisites

- Python >= 3.11.0
- Docker >= 20.10.22


## Dependancies

- boto3 = 1.28.35 - https://github.com/boto/boto3
- botocore = 1.31.35 - https://github.com/boto/botocore
- cloudpathlib = 0.15.1 - https://github.com/drivendataorg/cloudpathlib
- pywebcopy = 7.0.2 - https://github.com/rajatomar788/pywebcopy/
- s3transfer = 0.6.2 - https://github.com/boto/s3transfer

## Install

```
git clone https://github.com/BenjaminN117/Website-Defacement-Detection-Engine.git
```

Modify env.py file


Docker build

```
docker build -t web-detection-engine .
```

Local build

```
python3 -m venv web-detection-engine-venv
```

```
source web-detection-engine-venv/bin/activate
```

```
pip install -r requirements.txt
```

## Usage

Docker run

```
docker run -it --rm --name web-detection-engine web-detection-engine
```

Local build run

```
python3 src/main.py
```