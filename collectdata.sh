#!/bin/bash
tps=$(</volume2/SSD/scripts/data/tps.txt)
cpu=$(</volume2/SSD/scripts/data/cpu.txt)
mem=$(</volume2/SSD/scripts/data/mem.txt)
docker run --rm --name collectdata -v /volume2/SSD/scripts/dwh-docker:/usr/src/myapp -w /usr/src/myapp  marctv/python-pymysql:latest sh -c "python dwhproxy.py writeweather 'Hannover,de' && python dwhproxy.py writetwitter 'MarcTV' && python dwhproxy.py writeyoutube && python dwhproxy.py writedockerhub 'marctv' 'minecraft-papermc-server' && python dwhproxy.py writedockerhub 'marctv' 'minecraft-bedrock-server' && python dwhproxy.py writedockerhub 'marctv' 'minecraft-overviewer' && python dwhproxy.py writeblog && python dwhproxy.py writemcserver && python dwhproxy.py writemctps '${tps}' && python dwhproxy.py writemccpu '${cpu}' && python dwhproxy.py writemcmem '${mem}'"

#docker run -it --rm --name my-running-script -v "$PWD":/usr/src/myapp -w /usr/src/myapp  marctv/python-pymysql:latest sh -c "python dwhproxy.py writemctps '${tps}'"
#docker run -it --rm --name my-running-script -v "$PWD":/usr/src/myapp -w /usr/src/myapp  marctv/python-pymysql:latest sh -c "python dwhproxy.py writemccpu '${cpu}'"
#docker run -it --rm --name my-running-script -v "$PWD":/usr/src/myapp -w /usr/src/myapp  marctv/python-pymysql:latest sh -c "python dwhproxy.py writemcmem '${mem}'"

#python3 $DIR/dwh-proxy.py writemctps "docker exec -i mcserver rcon-cli --host localhost --port 25575 --password netherrack tps | sed -e  's/[^0-9., ]*//g' -e  's/ \+/ /g'"
#python3 $DIR/dwh-proxy.py writemccpu "docker stats mcserver --no-stream --format '{{.CPUPerc}}'"
#python3 $DIR/dwh-proxy.py writemcmem "docker stats mcserver --no-stream --format '{{.MemPerc}}'"

#DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

#python3 $DIR/dwh-proxy.py writemctps "docker exec -i mcserver rcon-cli --host localhost --port 25575 --password mypass tps | sed -e  's/[^0-9., ]*//g' -e  's/ \+/ /g'"
#python3 $DIR/dwh-proxy.py writemccpu "docker stats mcserver --no-stream --format '{{.CPUPerc}}'"
#python3 $DIR/dwh-proxy.py writemcmem "docker stats mcserver --no-stream --format '{{.MemPerc}}'"

#python3 $DIR/dwh-proxy.py writeweather "Hannover,de"
#python3 $DIR/dwh-proxy.py writeblog
#python3 $DIR/dwh-proxy.py writemcserver
#python3 $DIR/dwh-proxy.py writetwitter "MarcTV"
#python3 $DIR/dwh-proxy.py writeyoutube
