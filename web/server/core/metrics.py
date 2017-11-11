import sys
import os
import json
import pykitti
import dateutil.parser

def generate(date, drive):
    metrics = []

    def metric(id, value):
        metrics.append({
            "metricUid": id,
            "timestamp": ms,
            "value": float(value)
        })

    data = pykitti.raw("raw", date, drive)

    with open(os.path.join(data.data_path, "oxts/timestamps.txt")) as f:
        initial_timestamp = None
        for i, line in enumerate(f):
            timestamp = dateutil.parser.parse(line)
            initial_timestamp = initial_timestamp or timestamp
            with open(os.path.join(data.data_path, "oxts/data/{:0>10}.txt".format(i))) as datafile:
                dataline = datafile.read()
            lat, lng, alt, roll, pitch, yaw, vn, ve, vf, vl, vu, \
                ax, ay, az, af, al, au, wx, wy, wz, wf, wl, wu, *_ = \
                dataline.split(" ")
            delta = timestamp - initial_timestamp
            ms = delta.seconds * 1000 + delta.microseconds / 1000

            metric("alt", alt)
            metric("roll", roll)
            metric("pitch", pitch)
            metric("yaw", yaw)
            metric("af", af)
            metric("al", al)
            metric("au", au)
            metric("vf", vf)
            metric("vl", vl)
            metric("vu", vu)
            metric("wf", wf)
            metric("wl", wl)
            metric("wu", wu)

    with open("api/sources/KITTI-{0}-{1}/metrics.json".format(date, drive), "w") as outfile:
        json.dump(
            metrics,
            outfile,
            indent=2,
            sort_keys=True
        )

generate(sys.argv[1], sys.argv[2])
