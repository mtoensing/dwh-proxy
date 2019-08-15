# dwh-proxy
DataWareHouse Proxy for Grafana and MySQL

```pip3 pymysql``` 

On Synology:
```sudo python3 -m pip install pymysql```

## MySQL structure

See `history.sql`.

## mysql-config.json

```json
{
    "mysql":{
        "server":"ADR",
        "user":"USER",
        "password":"SECRET!!",
        "db":"DB"
    }
}
```


## weather-apikey.json

Get apikey from http://api.openweathermap.org

```json
{
    "weather":{
        "apikey":"key"
    }
}
```


## youtube-apikey.json

```json
{
    "youtube":{
        "apikey":"key",
        "channelid":"UCar1gwRwYqAGSNAuZoKDh2w"
    }
}
```
