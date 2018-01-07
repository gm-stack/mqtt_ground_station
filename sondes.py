#!/opt/local/bin/python3
import time
import json
from collections import defaultdict
import fastkml
from shapely.geometry import Point, LineString
import paho.mqtt.client

sonde_tracks = defaultdict(list)
ns = '{http://www.opengis.net/kml/2.2}'

def pos_kml(last_sonde_data):
    sonde_icon_style = fastkml.styles.IconStyle(
        ns=ns, 
        icon_href="http://maps.google.com/mapfiles/kml/shapes/track.png", 
        scale=2.0,
        heading=last_sonde_data['heading'])

    sonde_style = fastkml.styles.Style(
        ns=ns,
        styles=[sonde_icon_style])

    sonde_placemark = fastkml.kml.Placemark(
        ns=ns, 
        id=last_sonde_data['id'],
        name=last_sonde_data['id'],
        description="%(type)s %(id)s" % last_sonde_data,
        styles=[sonde_style])

    sonde_placemark.geometry = fastkml.geometry.Geometry(
        ns=ns,
        geometry=Point(last_sonde_data['lon'], last_sonde_data['lat'], last_sonde_data['alt']),
        altitude_mode='absolute')

    return sonde_placemark

def track_kml(sonde_data):
    sonde_track_line_style = fastkml.styles.LineStyle(
        ns=ns,
        color="ffff8000",
        width=3.0)

    sonde_track_style = fastkml.styles.Style(
        ns=ns,
        styles=[sonde_track_line_style])

    sonde_line = fastkml.kml.Placemark(
        ns=ns,
        id=sonde_data[-1]['id'],
        name="%(type)s %(id)s" % sonde_data[-1],
        styles=[sonde_track_style])

    line_data = [(loc['lon'], loc['lat'], loc['alt']) for loc in sonde_data]
    if len(line_data) == 1:
        line_data.append(line_data[0])

    sonde_line.geometry = fastkml.geometry.Geometry(
        ns=ns,
        geometry=LineString(line_data),
        altitude_mode='absolute',
        extrude=True,
        tessellate=True)

    return sonde_line

def write_kmls():
    kml_root = fastkml.kml.KML()

    kml_doc = fastkml.kml.Document(
        ns=ns,
        name="Sonde Data")

    for sonde in sonde_tracks.keys():
        kml_doc.append(pos_kml(sonde_tracks[sonde][-1]))
        kml_doc.append(track_kml(sonde_tracks[sonde]))

    kml_root.append(kml_doc)

    with open("/tmp/sonde_loc.kml", 'w') as kml_file:
        kml_file.write(kml_doc.to_string())


def on_message(client, userdata, message):
    payload = json.loads(message.payload)
    print(payload)
    sonde_tracks[payload['id']].append(payload)
    write_kmls()


mqtt_client = paho.mqtt.client.Client()
mqtt_client.connect('localhost', 1883)
mqtt_client.on_message = on_message
mqtt_client.subscribe("sonde/#")
while True:
    mqtt_client.loop()
