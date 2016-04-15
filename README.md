# transitfeed-web
GTFS transitfeed and FeedValidator web service

Install:
 * `./setup.py build`
 * `pip install .`
 * `export TRANSITFEED_WEB_CONFIG_URL=https://host:port/path/transitfeed_web_config.json`
 * `transitfeed_web`


Docker:
 * `docker build -t transitfeed-web .`
 * `docker run -e TRANSITFEED_WEB_CONFIG_URL=https://host:port/path/transitfeed_web_config.json -d -p 5000:5000 transitfeed-web`
