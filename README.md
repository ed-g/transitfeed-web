# transitfeed_web
GTFS transitfeed and FeedValidator web service

Install:
 * `./setup.py build`
 * `pip install .`
 * `export TRANSITFEED_WEB_CONFIG_URL=https://host:port/path/transitfeed_web_config.json`
 * `transitfeed_web`


Docker:
 * `docker build -t transitfeed-web .`
 * `docker run -e TRANSITFEED_WEB_CONFIG_URL=https://host:port/path/transitfeed_web_config.json -d -p 5000:5000 transitfeed-web`

Format for `transitfeed_web_config.json` config file, put this on your web server:

```json
{ 
    "comment" : "This is a configuration file for https://github.com/ed-g/transitfeed_web"
    , "regexp_allowlist" : [
        "https://developers.google.com/transit/gtfs/examples/sample-feed.zip"
        , "https?://data.trilliumtransit.com/[-a-zA-Z_/]+.zip"
        , "https?://www.oregon-gtfs.com/[-a-zA-Z_/]+.zip"
        , "https?://oregon-gtfs.com/[-a-zA-Z_/]+.zip"
    ]
}
```

There's an regular-expression based allow-list `regexp_allowlist`, which only
allows download and validation for feeds specified in the config file, in order
to help prevent this tool from being used to hack into third party sites as a
web proxy, and to limit possible security exposure from malicious GTFS files. 

