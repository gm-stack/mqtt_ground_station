#!/opt/local/bin/python3
import time
import json
from collections import defaultdict
import paho.mqtt.client

sonde_tracks = defaultdict(list)

def kml(sonde_data):
    pos_kml = """<StyleMap id="msn_track_%(id)s">
        <Pair>
            <key>normal</key>
            <styleUrl>#sn_track_%(id)s</styleUrl>
        </Pair>
        <Pair>
            <key>highlight</key>
            <styleUrl>#sn_track_%(id)s</styleUrl>
        </Pair>
    </StyleMap>
    <Style id="sn_track_%(id)s">
        <IconStyle>
            <scale>1.4</scale>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/shapes/track.png</href>
            </Icon>
            <hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
            <heading>%(heading).1f</heading>
        </IconStyle>
        <ListStyle>
        </ListStyle>
    </Style>
    <Placemark id="point">
        <name>%(type)s %(id)s</name>
        <LookAt>
            <latitude>%(lat).6f</latitude>
            <longitude>%(lon).6f</longitude>
            <altitude>0</altitude>
            <heading>0</heading>
            <tilt>0</tilt>
            <range>1000</range>
        </LookAt>
        <styleUrl>#sn_track_%(id)s</styleUrl>
        <Point>
            <coordinates>%(lon).6f,%(lat).6f,%(alt).1f</coordinates>
            <altitudeMode>absolute</altitudeMode>
        </Point>
    </Placemark>
""" % sonde_data[-1]

    track_kml = """<Style id="s_line">
        <LineStyle>
            <color>ffff8000</color>
            <width>3</width>
        </LineStyle>
    </Style>
    <Placemark>
        <name>Untitled Path</name>
        <styleUrl>#s_line</styleUrl>
        <LineString>
            <extrude>1</extrude>
            <tessellate>1</tessellate>
            <altitudeMode>absolute</altitudeMode>
            <coordinates>
            %s
            </coordinates>
        </LineString>
    </Placemark>
    """ % " ".join(["%(lon).6f,%(lat).6f,%(alt).1f" % loc for loc in sonde_data])

    return "%s\n%s" % (pos_kml, track_kml)

def write_kmls():
    sonde_kmls = [kml(sonde_tracks[sonde]) for sonde in sonde_tracks.keys()]

    kml_data = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
    <name>Chase Car.kml</name>
    %s
</Document>
</kml>
""" % "\n".join(sonde_kmls)

    with open("/tmp/sonde_loc.kml", 'w') as kml_file:
        kml_file.write(kml_data)


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
