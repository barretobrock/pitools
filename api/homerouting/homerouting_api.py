#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, redirect
from kavalkilu import Hosts

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/hosts')
def hosts():
    return redirect('http://tinyserv.local:5002/hosts')


@app.route('/keys')
def keys():
    return redirect('http://tinyserv.local:5002/keys')


@app.route('/nas')
def nas():
    return redirect('http://synserv.local:4000')


@app.route('/pihole')
def pihole():
    return redirect('http://tinyserv.local/admin')


@app.route('/pihole/client/<client>')
def pihole_lookup(client: str):
    # Lookup client ip
    ip = Hosts().get_ip_from_host(client)
    return redirect(f'http://tinyserv.local/admin/index.php?client={ip}')


@app.route('/viz')
def grafana():
    return redirect('http://tinyserv.local:3000/dashboards')


@app.route('/ha')
def homeauto():
    ip = Hosts().get_ip_from_host('pi-elutuba')
    return redirect(f'http://{ip}:8123/lovelace/default_view')


if __name__ == '__main__':
    app.run()
