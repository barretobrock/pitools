#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, redirect
from kavalkilu import Hosts

app = Flask(__name__)


@app.route('/')
def main_page():
    return 'Welcome to the Home Routing Landing Page!'


@app.route('/hosts')
def hosts():
    return redirect('http://tinyserv.local:5002/hosts')


@app.route('/keys')
def keys():
    return redirect('http://tinyserv.local:5002/keys')


@app.route('/', subdomain='nas')
def nas():
    return redirect('http://synserv.local:4000')


@app.route('/', subdomain='pihole')
def pihole():
    return redirect('http://tinyserv.local/admin')


@app.route('/client/<client>', subdomain='pihole')
def pihole_lookup(client: str):
    # Lookup client ip
    ip = Hosts().get_ip_from_host(client)
    return redirect(f'http://tinyserv.local/admin/index.php?client={ip}')


@app.route('/', subdomain='viz')
def grafana():
    return redirect('http://tinyserv.local:3000/dashboards')


@app.route('/', subdomain='ha')
def homeauto():
    ip = Hosts().get_ip_from_host('pi-elutuba')
    return redirect(f'http://{ip}:8123/lovelace/default_view')


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port='5003')
    app.run()
