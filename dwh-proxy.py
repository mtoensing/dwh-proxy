#!/usr/bin/env python3
"""Write sensor data to DB"""

import argparse
import re
import logging
import sys
import datetime
import pymysql
import json
import urllib.request
import os
from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(__file__)) + "/";

def writeyoutube(args):

    with open(current_dir + 'youtube-apikey.json') as json_data_file:
        data = json.load(json_data_file)
        channel_id = data["youtube"]["channelid"]
        api_key = data["youtube"]["apikey"]

    apiurl = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&fields=items/statistics/subscriberCount&key={api_key}".format(channel_id=channel_id,api_key=api_key)

    req = urllib.request.Request(apiurl)
    r = urllib.request.urlopen(req).read()
    jsonreponse = json.loads(r.decode('utf-8'))

    subscribercount = jsonreponse['items'][0]['statistics']['subscriberCount']

    writeMySQL(args, "YouTube" , None, 'subscribercount', int(subscribercount), None , "Subscriber"  )

def writemccpu(args):

    cmd = args.cmd
    cpustring = os.popen(cmd).read()
    cpuload = re.sub('[^0-9,.]', '', cpustring)
    writeMySQL(args, "MCServer" , None, 'cpu', cpuload , None , "%"  )

def writemcmem(args):

    cmd = args.cmd
    memstring = os.popen(cmd).read()
    memload = re.sub('[^0-9,.]', '', memstring)
    writeMySQL(args, "MCServer" , None, 'mem', memload , None , "%"  )

def writemctps(args):

    cmd = args.cmd
    tpsstring = os.popen(cmd).read()
    tps = tpsstring.split(",")
    # Average TPS of last minute
    tps_5 = re.sub('[^0-9,.]', '', tps[3])
    print(tpsstring)
    print(tps_5)

    writeMySQL(args, "MCServer" , None, 'tps', tps_5 , None , "TPS"  )

def writetwitter(args):

    channelname = args.channelname

    apiurl = "https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names={channelname}".format(channelname=channelname)

    req = urllib.request.Request(apiurl)
    r = urllib.request.urlopen(req).read()
    jsonreponse = json.loads(r.decode('utf-8'))

    followers_count = jsonreponse[0]['followers_count']

    writeMySQL(args, "Twitter" , None, 'followers_count', followers_count, None , "Follower" )


def writeweather(args):

    with open(current_dir + 'weather-apikey.json') as json_data_file:
        data = json.load(json_data_file)
        apikey = data["weather"]["apikey"]

    city = args.city
    apiurl = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={apikey}&units=metric".format(city=city, apikey=apikey)

    req = urllib.request.Request(apiurl)
    r = urllib.request.urlopen(req).read()
    jsonreponse = json.loads(r.decode('utf-8'))

    temperature = jsonreponse['main']['temp']
    humidity = jsonreponse['main']['humidity']
    wind = jsonreponse['wind']['speed']

    writeMySQL(args, city , None, 'temperature', temperature, None , "Celsius" )
    writeMySQL(args, city , None, 'humidity', humidity, None , "Celsius" )
    writeMySQL(args, city , None, 'wind', wind, None , "Celsius"  )

def writeblog(args):

    # Note f before first quote of string
    apiurl = "https://api.marc.tv/"

    req = urllib.request.Request(apiurl)
    r = urllib.request.urlopen(req).read()
    jsonreponse = json.loads(r.decode('utf-8'))

    currentvisitors = jsonreponse['row']['visitors']

    writeMySQL(args, "Marc.TV" , None, 'currentvisitors', currentvisitors, None , "Visitors" )

def writemcserver(args):

    # Note f before first quote of string
    apiurl = "https://mc.marc.tv/db/data.json"

    req = urllib.request.Request(apiurl)
    r = urllib.request.urlopen(req).read()
    jsonreponse = json.loads(r.decode('utf-8'))

    currentplayers = jsonreponse['server']['players_online']

    writeMySQL(args, "MCServer" , None, 'currentplayers', currentplayers, None , "Player"  )

def writeMySQL(args,device,type,event,value,reading,unit):

    with open(current_dir + 'mysql-config.json') as json_data_file:
        data = json.load(json_data_file)

        server = data["mysql"]["server"]
        user = data["mysql"]["user"]
        password = data["mysql"]["password"]
        db = data["mysql"]["db"]

    db = pymysql.connect(server,user,password,db )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "INSERT INTO history (TIMESTAMP,DEVICE,TYPE,EVENT,VALUE,READING,UNIT) VALUES (NOW(), %s, %s, %s, %s,%s ,%s)"
    val = (device ,type ,event ,value ,reading ,unit)

    try:
       # Execute the SQL command
       cursor.execute(sql, val)
    except:
       print ("Error: unable to connect to mysql db")
    # disconnect from server
    db.close()


def main():
    """Main function.

    Mostly parsing the command line arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose', action='store_const', const=True)
    subparsers = parser.add_subparsers(help='sub-command help', )

    parser_poll = subparsers.add_parser('writeweather', help='poll and write weather')
    parser_poll.add_argument('city', type=str)
    parser_poll.set_defaults(func=writeweather)

    parser_poll = subparsers.add_parser('writemctps', help='poll and write write mctps')
    parser_poll.add_argument('cmd', type=str)
    parser_poll.set_defaults(func=writemctps)

    parser_poll = subparsers.add_parser('writemccpu', help='poll and write write mc cpu')
    parser_poll.add_argument('cmd', type=str)
    parser_poll.set_defaults(func=writemccpu)

    parser_poll = subparsers.add_parser('writemcmem', help='poll and write write mc mem')
    parser_poll.add_argument('cmd', type=str)
    parser_poll.set_defaults(func=writemcmem)

    parser_poll = subparsers.add_parser('writeblog', help='poll and write blog')
    parser_poll.set_defaults(func=writeblog)

    parser_poll = subparsers.add_parser('writeyoutube', help='poll and write youtube')
    parser_poll.set_defaults(func=writeyoutube)

    parser_poll = subparsers.add_parser('writemcserver', help='poll and write mcserver')
    parser_poll.set_defaults(func=writemcserver)

    parser_poll = subparsers.add_parser('writetwitter', help='poll and write twitter')
    parser_poll.add_argument('channelname', type=str)
    parser_poll.set_defaults(func=writetwitter)

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == '__main__':
    main()
