#!/bin/bash
tps=$(</volume2/SSD/scripts/data/tps.txt)
cpu=$(</volume2/SSD/scripts/data/cpu.txt)
mem=$(</volume2/SSD/scripts/data/mem.txt)
docker run --rm --name collectdata-5min  -v /etc/localtime:/etc/localtime:ro -v /etc/TZ:/etc/timezone:ro -e TZ=Europe/Berlin -v /volume2/SSD/scripts/dwh-docker:/usr/src/myapp -w /usr/src/myapp  marctv/python-pymysql:latest sh -c "python dwhproxy.py writeweather 'Hannover,de' && python dwhproxy.py writeblog && python dwhproxy.py writemcserver && python dwhproxy.py writemctps '${tps}' && python dwhproxy.py writemccpu '${cpu}' && python dwhproxy.py writemcmem '${mem}' && python dwhproxy.py writematomo https://stats.toensing.com/ 3"
