from logging import raiseExceptions
import random
from signal import raise_signal
from redis.commands.json.path import Path
from flask import Flask, request, redirect, render_template
from flask.wrappers import Response
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
import redis
import time
import json
import rediscached
import mongodb
import crud
from prometheus_client import Counter
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})
c = Counter('io_task', 'io_task_counter')

# c = Counter('my_data', 'Description of my data')
# c.inc(1000)  # Increment by given value

try:
    mydb = mongodb.connect()
    worker = crud.Crud(mydb)
except ConnectionError:
    print("MONGO CONNECTION ERROR")

try:
    myredis = rediscached.connect()
except ConnectionError:
    print("REDIS CONNECTION ERROR")


@app.route("/io_task")
def io_task():
    c.inc()     # Increment by 1
    c.labels()
    # c.inc(1000)
    # print(type(c))
    # print(c)
    time.sleep(random.random())
    return "IO bound task finish!"


@app.route("/cpu_task")
def cpu_task():
    for i in range(10000):
        n = i*i*i
    return "CPU bound task finish!"


@app.route("/random_sleep")
def random_sleep():
    time.sleep(random.randint(0, 5))
    return "random sleep"


@app.route("/random_status")
def random_status():
    status_code = random.choice([200] * 6 + [300, 400, 400, 500])
    return Response("random status", status=status_code)


@app.route("/create", methods=['POST'])
def create():
    result = worker.insert_user()
    return result


@app.route("/getusers", methods=['GET'])
def get_users():
    result = worker.get_users()
    return result


@app.route("/delete/<id>", methods=['DELETE'])
def delete(id):
    result = worker.delete_user(id)
    return result


@app.route("/update/<id>", methods=['PUT'])
def update(id):
    result = worker.update_user(id)
    return result


@app.route("/getuser/<id>", methods=['GET'])
def get_user(id):
    result = worker.get_user(id)
    user = result.data.decode("utf-8")
    user = json.loads(user)
    # print(user)
    # print(user["_id"])
    user_cached = {
        "user": {
            "name": user["Name"],
            "lastName": user["lastName"]
        }
    }
    myredis.json().set("user:"+user["_id"], "$", user_cached)
    test = myredis.json().get("user:"+user["_id"])
    print(test)
    print(json.dumps(test))
    return result


# @app.route("/metrics", methods=['GET'])
# def export_metrics():
#     pass


@app.route('/')
def main():
    pass  # requests tracked by default
    return "hello"


# route nay ko track
@app.route('/skip')
@metrics.do_not_track()
def skip():  # default metrics are not collected
    return 'skip route'


@app.route('/<item_type>')
@metrics.do_not_track()
@metrics.counter('invocation_by_type', 'Number of invocations by type',
                 labels={'item_type': lambda: request.view_args['type']})
def by_type(item_type):
    return item_type  # only the counter is collected, not the default metrics


@app.route('/long-running')
@metrics.gauge('in_progress', 'Long running requests in progress')
def long_running():
    return "long-runnning"


@app.route('/status/<int:status>')
@metrics.do_not_track()
@metrics.summary('requests_by_status', 'Request latencies by status',
                 labels={'status': lambda r: r.status_code})
@metrics.histogram('requests_by_status_and_path', 'Request latencies by status and path',
                   labels={'status': lambda r: r.status_code, 'path': lambda: request.path})
def echo_status(status):
    return 'Status: %s' % status, status
