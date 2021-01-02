import os
import shutil
import socket
from datetime import time
from multiprocessing import Pool
from multiprocessing import cpu_count
import signal
from time import sleep
from happy_birthday import birthday_helper
import googlecloudprofiler
import psutil
from flask import Flask, render_template, request, session, redirect, url_for
from flask_bootstrap import Bootstrap
from process_tweets import process_tweet
from gcp_services.retrieve_web_credentials import get_credentials, publish_msg
from cpu_blow import *

app = Flask(__name__)
Bootstrap(app)

app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'


@app.route('/blow_mem')
def blow_memory():
    memory_blow_up()
    return render_template("home.html", msg="Finished eating memory :).")


def memory_blow_up():
    blow = list()
    for number in range(10000000):
        blow.append(number)
    sleep(10)


@app.route('/happy_birth_day', methods=['GET', 'POST'])
def happy_birth_day():
    if request.method == 'GET':
        return render_template("add_friends.html")
    elif request.method == 'POST':
        data = request.form.to_dict(flat=True)
        birthday_helper.insert(data)
        friends_list = birthday_helper.refactor()
        return render_template("add_friends.html")
    else:
        return "Method not supported for /questions/add"


@app.route('/blow_cpu')
def blow_cpu():
    execute_cpu_blow()
    return render_template("home.html", msg="Finished consuming " + str(cpu_count()) + " CPUs :).")


@app.route('/twitter')
def tw():
    tweets = process_tweet()
    return render_template("tweets.html", tweets=tweets)


@app.route('/romeo.txt')
def romeo():
    return "<html><body>This is a romeo.txt file - Only for tests :). Juliet txt will follow. by, Jonasa..</html"


@app.route('/execute', methods=['GET', 'POST'])
def execute():
    credentials = dict()
    credentials = get_credentials("jonasa-login")
    if request.form['user_name'] != credentials['user_name'] or request.form['password'] != credentials['password']:
        error = 'Invalid Credentials. Please try again.'
        remote_addr = str(request.remote_addr)
        publish_msg(f"Wrong credentials from IP: {remote_addr}")
    else:
        session['logged_in'] = True
        return render_template("home.html")
    return render_template("index.html", error=error)


@app.route('/')
def login():
    return render_template("index.html")


def get_host_name():
    return socket.getfqdn()


def retrieve_disk_status(drive):
    disk_status = dict()
    disk_usage = shutil.disk_usage(drive)
    disk_status['free_disk_space'] = int(disk_usage.free / (1024 * 1024 * 1024))
    disk_status['tot_disk_space'] = int(disk_usage.total / (1024 * 1024 * 1024))
    disk_status['free_percent'] = int(disk_status['free_disk_space'] / disk_status['tot_disk_space'] * 100)
    return disk_status


def retrieve_memory_status():
    memory_status = dict()
    memory_status['total'] = int(psutil.virtual_memory().total / (1024 * 1024 * 1024))
    memory_status['free'] = int(psutil.virtual_memory().available / (1024 * 1024 * 1024))
    memory_status['percent'] = int(psutil.virtual_memory().percent)
    return memory_status


def retrive_cpu_usage():
    return psutil.cpu_percent(1)


@app.route('/monitor_resources')
def monitor_resources():
    data = request.form.to_dict(flat=True)
    birthday_helper.insert(data)
    return render_template("monitor_resources.html", disk=disk_status, memory=memory_status,
                           cpu_usage=cpu_usage, host=get_host_name())


def hello_world():
    a = "test"
    print(f"We are here:{a}")


if __name__ == "__main__":
    try:
        googlecloudprofiler.start(
            service='jonasa-profiler',
            service_version='1.0.1',
            # verbose is the logging level. 0-error, 1-warning, 2-info,
            # 3-debug. It defaults to 0 (error) if not set.
            verbose=3,
            # project_id must be set if not running on GCP.
            # project_id='my-project-id',
        )
    except (ValueError, NotImplementedError) as exc:
        print(exc)  # Handle errors here
    app.run(host='0.0.0.0', port=4444)
