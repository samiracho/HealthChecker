#!/usr/bin/env python3
import os
from cron import Cron
from bottle import route, run, Bottle
import sys
from server import MyWSGIRefServer

# set the current dir as working directory
os.chdir(os.path.dirname(sys.argv[0]))

# Get default values
port = os.getenv('HK_DEFAULT_PORT', 8080)
time_interval = os.getenv('HK_TIME_INTERVAL', 300)


@route('/healthz')
def healthz():
    return "Health checker is alive"


# Create http server
app = Bottle()
server = MyWSGIRefServer(host='0.0.0.0', port=port)

# Run our background cron-job that does health checks every 5 min
background_checks = Cron(server, time_interval)

# Start bottle server
app.run(server=server)
