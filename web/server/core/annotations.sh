import sys
import os
import pykitti
import json
import xml.etree.ElementTree
import numpy as np
from numpy import cos, sin

annotations = []

def rotation(theta):
    tx, ty, tz = theta

    Rx = np.array([
        [1, 0, 0,  0],
        [0, cos(tx), -sin(tx), 0],
        [0, sin(tx), cos(tx), 0],
        [0, 0, 0, 1]
    ])

    Ry = np.array([
        [cos(ty), 0, -sin(ty), 0],
        [0, 1, 0, 0],
        [sin(ty), 0, cos(ty), 0],
        [0, 0, 0, 1]
    ])

    Rz = np.array([
        [cos(tz), -sin(tz), 0, 0],
        [sin(tz), cos(tz), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    return np.dot(Rx, np.dot(Ry, Rz))

def translation(delta):
    tx, ty, tz = delta
    T = np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1],
    ])
    return T

def bboxrect(frame, box, camera):
    tx = float(frame.find("tx").text)
    ty = float(frame.find("ty").text)
    tz = float(frame.find("tz").text)
    T = translation([tx, ty, tz])

    rx = float(frame.find("rx").text)
    ry = float(frame.find("ry").text)
    rz = float(frame.find("rz").text)
    R = rotation([rx, ry, rz])

    base_points = [
        np.array([ box["l"] / 2,  box["w"] / 2,  box["h"] / 2, 1]),
        np.array([ box["l"] / 2,  box["w"] / 2, -box["h"] / 2, 1]),
        np.array([ box["l"] / 2, -box["w"] / 2,  box["h"] / 2, 1]),
        np.array([ box["l"] / 2, -box["w"] / 2, -box["h"] / 2, 1]),
        np.array([-box["l"] / 2,  box["w"] / 2,  box["h"] / 2, 1]),
        np.array([-box["l"] / 2,  box["w"] / 2, -box["h"] / 2, 1]),
        np.array([-box["l"] / 2, -box["w"] / 2,  box["h"] / 2, 1]),
        np.array([-box["l"] / 2, -box["w"] / 2, -box["h"] / 2, 1])
    ]

    points = [T.dot(R.dot(p)) for p in base_points]
    camera_points = [camera["T"].dot(p) for p in points]
    projected = [camera["K"].dot(np.array([p[0] / p[2], p[1] / p[2], 1])) for p in camera_points]

    # for p in projected:
    #     print("PROJECTED", p)

    # raise "XX"

    x = [p[0] for p in projected]
    y = [p[1] for p in projected]

    bbox = [
        min(x),
        min(y),
        max(x),
        max(y)
    ]

    sx = 1242
    sy = 375

    return {
        "upperLeft": {
            "x": bbox[0] / sx,
            "y": bbox[1] / sy
        },
        "lowerRight": {
            "x": bbox[2] / sx,
            "y": bbox[3] / sy
        }
    }

def project(timestamps, start, frames, box, camera, color):
    return [
        {
            "timestamp": ms(timestamps, timestamps[start + index]),
            "boundingBox": {
                "rect": bboxrect(frame, box, camera),
                "color": color
            }
        } for index, frame in enumerate(frames)
    ]

def annotation(id, type, source, start, end, frames):
    annotations.append({
        "uid": id,
        "type": type,
        "source": source,
        "startTime": start,
        "endTime": end,
        "frames": frames
    })

def ms(timestamps, timestamp):
    delta = timestamp - timestamps[0]
    return delta.seconds * 1000 + delta.microseconds / 1000

def read_matrix(line):
    head, *raw_tail = line.split(" ")
    tail = [float(item) for item in raw_tail]
    return np.array([
        [tail[0], tail[1], tail[2], 0],
        [tail[3], tail[4], tail[5], 0],
        [tail[6], tail[7], tail[8], 0],
        [0, 0, 0, 1]
    ])

def read_projection_matrix(line):
    head, *raw_tail = line.split(" ")
    tail = [float(item) for item in raw_tail]
    return np.array([
        [tail[0], tail[1], tail[2], 0],
        [tail[3], tail[4], tail[5], 0],
        [tail[6], tail[7], tail[8], 0],
    ])

def map_object_type(in_type):
    return {
        "Car": "car",
        "Cyclist": "cyclist",
        "Pedestrian": "pedestrian",
        "Tram": "tram",
        "Truck": "truck",
        "Van": "van"
    }.get(in_type, "unspecified")

def map_object_color(in_type):
    return {
        "Car": "yellow",
        "Cyclist": "green",
        "Pedestrian": "white",
        "Tram": "magenta",
        "Truck": "red",
        "Van": "orange"
    }.get(in_type, "white")

def map_object_source(tracklet):
    return {
        "Cyclist": "dnn",
    }.get(tracklet.find("./objectType").text, "software")

def generate(date, drive):
    data = pykitti.raw("raw", date, drive)

    timestamps = data.timestamps

    root = xml.etree.ElementTree.parse(os.path.join(data.data_path, "tracklet_labels.xml")).getroot()
    tracklets = [node for node in root.findall("./tracklets/item")]

    for index, tracklet in enumerate(tracklets):
        first_frame = int(tracklet.find("./first_frame").text)
        last_frame = first_frame + int(tracklet.find("./poses/count").text) - 1
        frames = tracklet.findall("./poses/item")

        box = {
            "w": float(tracklet.find("./w").text),
            "h": float(tracklet.find("./h").text),
            "l": float(tracklet.find("./l").text)
        }

        color = map_object_color(tracklet.find("./objectType").text)
        source = map_object_source(tracklet)
        params = {
            "timestamps": timestamps,
            "start": first_frame,
            "frames": frames,
            "box": box,
            "color": color
        }

        annotation(
            "tracklet-{0}".format(index),
            map_object_type(tracklet.find("./objectType").text),
            source,
            ms(timestamps, timestamps[first_frame]),
            ms(timestamps, timestamps[last_frame]),
            {
                "front-left-bw": project(
                    camera={
                        "T": data.calib.T_cam0_velo,
                        "K": data.calib.K_cam0
                    },
                    **params
                ),
                "front-right-bw": project(
                    camera={
                        "T": data.calib.T_cam1_velo,
                        "K": data.calib.K_cam1
                    },
                    **params
                ),
                "front-left-color": project(
                    camera={
                        "T": data.calib.T_cam2_velo,
                        "K": data.calib.K_cam2
                    },
                    **params
                ),
                "front-right-color": project(
                    camera={
                        "T": data.calib.T_cam3_velo,
                        "K": data.calib.K_cam3
                    },
                    **params
                )
            }
        )

    with open("api/sources/KITTI-{0}-{1}/annotations.json".format(date, drive), "w") as outfile:
        json.dump(
            annotations,
            outfile,
            indent=2,
            sort_keys=True
        )

generate(sys.argv[1], sys.argv[2])
