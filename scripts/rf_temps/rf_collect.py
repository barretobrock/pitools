#!/usr/bin/env python3

"""InfluxDB monitoring relay for rtl_433."""

# Start rtl_433 (rtl_433 -F syslog::1433), then this script

import socket
from datetime import datetime
import json
import sys
from kavalkilu import InfluxDBLocal, InfluxDBNames, InfluxTblNames


UDP_IP = "127.0.0.1"
UDP_PORT = 1433

TAGS = [
    "channel",
    "id",
]

FIELDS = [
    "temperature_C",
    "humidity",
    "battery_ok"
]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.bind((UDP_IP, UDP_PORT))


def sanitize(text):
    return text.replace(" ", "_").replace("/", "_").replace(".", "_").replace("&", "")


def parse_syslog(line):
    """Try to extract the payload from a syslog line."""
    line = line.decode("ascii")  # also UTF-8 if BOM
    if line.startswith("<"):
        # fields should be "<PRI>VER", timestamp, hostname, command, pid, mid, sdata, payload
        fields = line.split(None, 7)
        line = fields[-1]
    return line


def rtl_433_probe():
    influx = InfluxDBLocal(InfluxDBNames.HOMEAUTO)

    while True:
        line, _addr = sock.recvfrom(1024)

        try:
            line = parse_syslog(line)
            data = json.loads(line)
            print(f'Seeing: {data}')

            if "model" not in data:
                continue
            measurement = sanitize(data["model"])

            tags = {}
            for tag in TAGS:
                if tag in data:
                    tags[tag] = data[tag]

            fields = {}
            for field in FIELDS:
                if field in data:
                    fields[field] = data[field]

            if len(fields) == 0:
                continue

            point = {
                "measurement": measurement,
                "time": datetime.now().isoformat(),
                "tags": tags,
                "fields": fields,
            }

            try:

                influx.write_single_data(InfluxTblNames.TEMPS, tags, fields)
            except Exception as e:
                print("error {} writing {}".format(e, point), file=sys.stderr)

        except KeyError:
            pass

        except ValueError:
            pass


def run():
    # with daemon.DaemonContext(files_preserve=[sock]):
    #  detach_process=True
    #  uid
    #  gid
    #  working_directory
    rtl_433_probe()


if __name__ == "__main__":
    run()
