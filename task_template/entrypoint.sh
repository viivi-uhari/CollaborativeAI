#!/bin/bash
# For HTTPS use uncomment the following 3 lines
# echo "$SSL_CERTIFICATE" >> cert.pem
# echo "$SSL_KEY" >> key.pem
# uvicorn main:app --ssl-keyfile /usr/project/key.pem --ssl-certfile /usr/project/cert.pem --port 8062 --host 0.0.0.0

# if you use https, comment this line
uvicorn main:app --port 8062 --host 0.0.0.0