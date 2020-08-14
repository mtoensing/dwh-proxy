#!/bin/bash
docker run -it --rm --name my-running-script -v "$PWD":/usr/src/myapp -w /usr/src/myapp marctv/python-pymysql:latest python dwhproxy.py writeweather "Hannover,de"
docker run -it --rm --name my-running-script -v "$PWD":/usr/src/myapp -w /usr/src/myapp marctv/python-pymysql:latest python dwhproxy.py writetwitter "MarcTV"
docker run -it --rm --name my-running-script -v "$PWD":/usr/src/myapp -w /usr/src/myapp marctv/python-pymysql:latest python dwhproxy.py writeyoutube
docker run -it --rm --name my-running-script -v "$PWD":/usr/src/myapp -w /usr/src/myapp marctv/python-pymysql:latest python dwhproxy.py writedockerhub "marctv" "minecraft-papermc-server"
docker run -it --rm --name my-running-script -v "$PWD":/usr/src/myapp -w /usr/src/myapp marctv/python-pymysql:latest python dwhproxy.py writedockerhub "marctv" "minecraft-bedrock-server"
docker run -it --rm --name my-running-script -v "$PWD":/usr/src/myapp -w /usr/src/myapp marctv/python-pymysql:latest python dwhproxy.py writedockerhub "marctv" "minecraft-overviewer"

#DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

#python3 $DIR/dwh-proxy.py writemctps "docker exec -i mcserver rcon-cli --host localhost --port 25575 --password mypass tps | sed -e  's/[^0-9., ]*//g' -e  's/ \+/ /g'"
#python3 $DIR/dwh-proxy.py writemccpu "docker stats mcserver --no-stream --format '{{.CPUPerc}}'"
#python3 $DIR/dwh-proxy.py writemcmem "docker stats mcserver --no-stream --format '{{.MemPerc}}'"

#python3 $DIR/dwh-proxy.py writeweather "Hannover,de"
#python3 $DIR/dwh-proxy.py writeblog
#python3 $DIR/dwh-proxy.py writemcserver
#python3 $DIR/dwh-proxy.py writetwitter "MarcTV"
#python3 $DIR/dwh-proxy.py writeyoutube
