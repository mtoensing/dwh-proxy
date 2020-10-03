#!/usr/bin/env python3
# V0.4
# Marc Tönsing
"""Write sensor data to DB"""

import argparse
import re
import logging
import sys
import datetime
import pymysql
import json
import asyncio
import urllib.request
import os

from pathlib import Path
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

current_dir = os.path.dirname(os.path.abspath(__file__)) + "/";

async def merossasync(devicetype):

    with open(current_dir + 'meross-auth.json') as json_data_file:
        data = json.load(json_data_file)
        email = data["meross"]["email"]
        password = data["meross"]["password"]

    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(email=email, password=password)

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Retrieve all the MS100 devices that are registered on this account
    await manager.async_device_discovery()
    sensors = manager.find_devices(device_type="ms100")

    if len(sensors) < 1:
        print("No MS100 plugs found...")
    else:
        dev = sensors[0]

        # Manually force and update to retrieve the latest temperature sensed from
        # the device. This ensures we get the most recent data and not a cached value
        await dev.async_update()

        # Access read cached data
        temp = dev.last_sampled_temperature
        humid = dev.last_sampled_humidity
        time = dev.last_sampled_time

        #writeMySQL(args, "meross" , None, 'temperature', temperature, None , "Celsius" )
        #writeMySQL(args, "meross" , None, 'humidity', humidity, None , "Humidity" )

        print(f"Current sampled data on {time.isoformat()}; Temperature={temp}°C, Humidity={humid}%")
    # Close the manager and logout from http_api
    manager.close()
    await http_api_client.async_logout()

def writemeross(args):

    devicetype = args.devicetype

    loop = asyncio.get_event_loop()
    loop.run_until_complete(merossasync(devicetype=devicetype))
    loop.close()

def writefeedly(args):

    feedId = args.feedId

    # Note f before first quote of string
    apiurl = f"http://cloud.feedly.com/v3/feeds/feed%2F{feedId}"

    req = urllib.request.Request(apiurl)
    r = urllib.request.urlopen(req).read()
    jsonreponse = json.loads(r.decode('utf-8'))

    subscribers = jsonreponse['subscribers']

    writeMySQL(args, 'feedly' , None, 'subscribers', subscribers, None , "Subscribers" )


def writematomo(args):

    with open(current_dir + 'matomo-authkey.json') as json_data_file:
        data = json.load(json_data_file)
        token_auth = data["matomo"]["token_auth"]

    matomourl = args.matomourl
    siteid = args.siteid

    # Note f before first quote of string
    apiurl = f"{matomourl}/?module=API&format=json&method=VisitsSummary.get&idSite={siteid}&date=today&period=day&token_auth=&token_auth={token_auth}"

    req = urllib.request.Request(apiurl)
    r = urllib.request.urlopen(req).read()
    jsonreponse = json.loads(r.decode('utf-8'))

    nb_uniq_visitors = jsonreponse['nb_uniq_visitors']
    nb_visits = jsonreponse['nb_visits']

    writeMySQL(args, 'matomo' , siteid, 'unique_visitors', nb_uniq_visitors, None , "unique visitors" )
    writeMySQL(args, 'matomo' , siteid, 'visits', nb_visits, None , "visits" )


def writedockerhub(args):

    dockerhubuser = args.dockerhubuser
    dockerhubcontainer = args.dockerhubcontainer

    # Note f before first quote of string
    apiurl = f"https://hub.docker.com/v2/repositories/{dockerhubuser}/{dockerhubcontainer}/"

    req = urllib.request.Request(apiurl)
    r = urllib.request.urlopen(req).read()
    jsonreponse = json.loads(r.decode('utf-8'))

    star_count = jsonreponse['star_count']
    pull_count = jsonreponse['pull_count']

    writeMySQL(args, dockerhubcontainer , "dockerhub", 'star_count', star_count, None , "stars" )
    writeMySQL(args, dockerhubcontainer , "dockerhub", 'pull_count', pull_count, None , "pulls" )


def writeyoutube(args):

    with open(current_dir + 'youtube-apikey.json') as json_data_file:
        data = json.load(json_data_file)
        channel_id = data["youtube"]["channelid"]
        api_key = data["youtube"]["apikey"]

    apiurl = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&fields=items/statistics&key={api_key}".format(channel_id=channel_id,api_key=api_key)

    req = urllib.request.Request(apiurl)
    r = urllib.request.urlopen(req).read()
    jsonreponse = json.loads(r.decode('utf-8'))

    subscribercount = jsonreponse['items'][0]['statistics']['subscriberCount']
    viewcount = jsonreponse['items'][0]['statistics']['viewCount']

    writeMySQL(args, "YouTube" , None, 'viewcount', int(viewcount), None , "Views"  )
    writeMySQL(args, "YouTube" , None, 'subscribercount', int(subscribercount), None , "Subscriber"  )

def writemccpu(args):

    cpustring = args.cmd
    cpuload = re.sub('[^0-9,.]', '', cpustring)

    writeMySQL(args, "MCServer" , None, 'cpu', cpuload , None , "%"  )

def writemcmem(args):

    memstring = args.cmd
    memload = re.sub('[^0-9,.]', '', memstring)

    writeMySQL(args, "MCServer" , None, 'mem', memload , None , "%"  )

def writemctps(args):

    tpsstring = args.cmd
    tps = tpsstring.split(",")
    # Average TPS of last 5 mintes minute
    tps_5 = re.sub('[^0-9,.]', '', tps[3])
    #print(tpsstring)
    #print(tps_5)

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
    writeMySQL(args, city , None, 'humidity', humidity, None , "Humidity" )
    writeMySQL(args, city , None, 'wind', wind, None , ""  )

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

    #print(datetime.datetime.now())
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

    parser_poll = subparsers.add_parser('writemeross', help='poll and write meross iot')
    parser_poll.add_argument('devicetype', type=str)
    parser_poll.set_defaults(func=writemeross)

    parser_poll = subparsers.add_parser('writefeedly', help='poll and write feedly subscribers')
    parser_poll.add_argument('feedId', type=str)
    parser_poll.set_defaults(func=writefeedly)

    parser_poll = subparsers.add_parser('writematomo', help='poll and write matomo stats')
    parser_poll.add_argument('matomourl', type=str)
    parser_poll.add_argument('siteid', type=str)
    parser_poll.set_defaults(func=writematomo)

    parser_poll = subparsers.add_parser('writedockerhub', help='poll and write docker hub')
    parser_poll.add_argument('dockerhubuser', type=str)
    parser_poll.add_argument('dockerhubcontainer', type=str)
    parser_poll.set_defaults(func=writedockerhub)

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
