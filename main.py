import shutil
import socket

import psutil
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    return render_template("index.html")


def get_host_name():
    return socket.getfqdn()


def retrieve_disk_status(drive):
    disk_status = dict()
    disk_usage = shutil.disk_usage(drive)
    disk_status['free_disk_space'] = int(disk_usage.free/(1024*1024*1024))
    disk_status['tot_disk_space'] = int(disk_usage.total/(1024*1024*1024))
    disk_status['free_percent'] = int(disk_status['free_disk_space']/disk_status['tot_disk_space']*100)
    return disk_status


def retrieve_memory_status():
    memory_status = dict()
    memory_status['total'] = int(psutil.virtual_memory().total/(1024*1024*1024))
    memory_status['free'] = int(psutil.virtual_memory().available/(1024*1024*1024))
    memory_status['percent'] = int(psutil.virtual_memory().percent)
    return memory_status


def retrive_cpu_usage():
    return psutil.cpu_percent(1)


@app.route('/monitor_resources')
def monitor_resources():
    disk_status = retrieve_disk_status(drive = "c:/")
    memory_status = retrieve_memory_status()
    cpu_usage = retrive_cpu_usage()
    return render_template("monitor_resources.html", disk = disk_status, memory = memory_status,
                           cpu_usage = cpu_usage, host = get_host_name())


if __name__ == "__main__":
    app.run(debug = True, port = 4444)
