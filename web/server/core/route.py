import sys
import os
import json
import pykitti
import dateutil.parser
from math import degrees

def generate(date, drive):
    data = pykitti.raw("raw", date, drive)
    waypoints = []

    with open(os.path.join(data.data_path, "oxts/timestamps.txt")) as f:
        initial_timestamp = None
        previous_heading = None
        for i, line in enumerate(f):
            timestamp = dateutil.parser.parse(line)
            initial_timestamp = initial_timestamp or timestamp
            with open(os.path.join(data.data_path, "oxts/data/{:0>10}.txt".format(i))) as datafile:
                dataline = datafile.read()
            lat, lng, alt, roll, pitch, yaw, *_ = dataline.split(" ")
            delta = timestamp - initial_timestamp

            heading = degrees(- float(yaw)) - 90
            if previous_heading and abs(heading - previous_heading) > 180:
                if heading > previous_heading:
                    heading = heading - 360
                else:
                    heading = heading + 360
            previous_heading = heading

            waypoints.append({
                "millisecondsFromStart": delta.seconds * 1000 + delta.microseconds / 1000,
                "heading": heading,
                "coordinates": {
                    "lat": float(lat),
                    "lng": float(lng)
                }
            })

    with open("api/sources/KITTI-{0}-{1}/route.json".format(date, drive), "w") as outfile:
        json.dump({ "route": { "waypoints": waypoints }}, outfile, indent=2, sort_keys=True)


generate(sys.argv[1], sys.argv[2])
