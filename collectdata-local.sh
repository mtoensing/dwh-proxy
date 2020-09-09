#!/bin/bash
docker run --rm --name collectdata  -e TZ=Europe/Berlin -v /Users/mtoe/Documents/dwh-proxy:/usr/src/myapp -w /usr/src/myapp  marctv/python-pymysql:latest sh -c "python dwhproxy.py writematomo https://stats.toensing.com/ 3"
