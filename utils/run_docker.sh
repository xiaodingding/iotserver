#!/bin/bash
#


# Run redis
docker run --name redis -d redis

# Run iotserver
docker run -d --name iotserver -p 8080:8080 --link redis:redis iotserver/iotserver:v0.4.0-beta1

# Finished
echo -e "Please visit http://ServerIP:8080\n Username: admin\nPassword: admin\n"
