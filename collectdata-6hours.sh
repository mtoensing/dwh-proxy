#!/bin/bash
docker run --rm --name collectdata-6hours -v /volume2/SSD/scripts/dwh-docker:/usr/src/myapp -w /usr/src/myapp  marctv/python-pymysql:latest sh -c "python dwhproxy.py writetwitter 'MarcTV' && python dwhproxy.py writeyoutube && python dwhproxy.py writedockerhub 'marctv' 'minecraft-papermc-server' && python dwhproxy.py writedockerhub 'marctv' 'minecraft-bedrock-server' && python dwhproxy.py writedockerhub 'marctv' 'minecraft-overviewer'"