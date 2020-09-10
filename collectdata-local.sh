#!/bin/bash
docker run --rm --name collectdata  -e TZ=Europe/Berlin -v /Users/mtoe/Documents/dwh-proxy:/usr/src/myapp -w /usr/src/myapp  marctv/python-pymysql:latest sh -c "python dwhproxy.py writefeedly http%3A%2F%2Fwww.marctv.de%2Ffeed%2Fartikel.xml"
