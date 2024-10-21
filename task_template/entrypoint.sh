#!/bin/bash
# uvicorn main:app --ssl-keyfile /usr/project/key.pem --ssl-certfile /usr/project/cert.pem --port 8062 --host 0.0.0.0
uvicorn main:app --port 8062 --host 0.0.0.0