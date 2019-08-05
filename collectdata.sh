#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

python3 $DIR/dwh-proxy.py writeweather "Hannover,de"
python3 $DIR/dwh-proxy.py writeblog
python3 $DIR/dwh-proxy.py writemcserver
python3 $DIR/dwh-proxy.py writetwitter "MarcTV"
python3 $DIR/dwh-proxy.py writeyoutube
