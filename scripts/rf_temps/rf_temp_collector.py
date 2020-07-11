#!/usr/bin/env python3
"""
Reads in a piped stream of JSON data, tries to feed into InfluxDB directly
"""
import sys
import json
from json.decoder import JSONDecodeError
from subprocess import Popen, PIPE, STDOUT
from queue import Queue, Empty
from datetime import datetime
import pandas as pd
from kavalkilu import InfluxDBLocal, InfluxDBNames, InfluxTblNames, Log, DateTools


ON_POSIX = 'posix' in sys.builtin_module_names
logg = Log('rf-collector', log_dir='weather', log_to_db=True)

influx = InfluxDBLocal(InfluxDBNames.HOMEAUTO)
dt = DateTools()
# device id to device-specific data mapping
mappings = {
    9459: {
        'name': 'freezer'
    },
    210: {
        'name': 'unknown'
    }
}

# Map the names of the variables from the various sensors to what's acceptable in the db
possible_measurements = {
    'temperature_C': 'temp',
    'humidity': 'humidity'
}

logg.debug('Initializing stream reader...')
interval = datetime.now()
split_s = 120   # Log every 10 mins
data_df = pd.DataFrame()

cmd = ['/usr/local/bin/rtl_433', '-F', 'json']
p = Popen(cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, close_fds=ON_POSIX)
q = Queue()
pulse = 0
while True:
    line = None
    try:
        src, line = q.get(timeout=1)
    except Empty:
        pulse += 1
    else:
        # Got line
        pulse -= 0
    print(line)
    data = None
    try:
        data = json.loads(line)
    except JSONDecodeError as e:
        logg.error_with_class(e, f'Error {e} decoding {line.strip()}')
        continue

    if data is not None:
        # Begin extraction process
        if data['id'] in mappings.keys():
            # Device is known... record data
            measurements = {}
            for k, v in possible_measurements:
                if k in data.keys():
                    measurements[v] = data[k]
            if len(measurements) > 0:
                # Write to dataframe
                measurements.update({
                    'location': mappings[data['id']]['name'],
                    'timestamp': data['time']
                })
                data_df = data_df.append(pd.DataFrame(measurements, index=[0]))
        else:
            logg.info(f'Unknown device found: {data["model"]}: ({data["id"]})')
    if (datetime.now() - interval).total_seconds() > split_s:
        # Gone over the time limit. Try to log all the non-duplicate info to database
        data_df = data_df.drop_duplicates()
        logg.debug(f'Logging interval reached. Sending over {data_df.shape[0]} points to db.')
        influx.write_df_to_table(InfluxTblNames.TEMPS, data_df, tags='location',
                                 value_cols=['temp', 'humidity'], time_col='timestamp')
        # Reset our info
        interval = datetime.now()
        data_df = pd.DataFrame()

logg.debug('Collection ended. Closing Influx connection')
influx.close()
logg.close()
