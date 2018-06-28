from flask import Flask, Response
from redis import Redis, RedisError

from prometheus_client import Gauge, Counter
from prometheus_client.core import CollectorRegistry

import os
import socket
import psutil
import prometheus_client

redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

REGISTRY = CollectorRegistry(auto_describe=False)

c = Gauge("cpu_usage", "the usage of cpu", registry=REGISTRY)
m = Gauge("mem_usage", "the usage of memory", registry=REGISTRY)
v = Counter("visit_count", "visit count", registry=REGISTRY)

app = Flask(__name__)

def add(a, b):
    return a+b;

@app.route("/metrics")
def prom():
    c.set(psutil.cpu_percent(interval=1))
    m.set(psutil.virtual_memory().percent)
    v.inc()
    return Response(prometheus_client.generate_latest(REGISTRY), mimetype="text/plain")

@app.route("/")
def hello():
    v.inc()
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>This is My Test Hello {name}!</h3>" \
        "<b>Hostname:</b> {hostname}<br />" \
        "<b>Visits:</b> {visits}"

    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
