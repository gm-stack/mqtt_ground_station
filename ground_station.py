#!/opt/local/bin/python3
import time
import gps

gps_track = []

def write_kml():
    pos_kml = """<StyleMap id="msn_track">
        <Pair>
            <key>normal</key>
            <styleUrl>#sn_track</styleUrl>
        </Pair>
        <Pair>
            <key>highlight</key>
            <styleUrl>#sh_track</styleUrl>
        </Pair>
    </StyleMap>
    <Style id="sn_track">
        <IconStyle>
            <scale>1.2</scale>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/shapes/track.png</href>
            </Icon>
            <hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
            <heading>%(track).1f</heading>
        </IconStyle>
        <ListStyle>
        </ListStyle>
    </Style>
    <Style id="sh_track">
        <IconStyle>
            <scale>1.4</scale>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/shapes/track.png</href>
            </Icon>
            <hotSpot x="32" y="32" xunits="pixels" yunits="pixels"/>
            <heading>%(track).1f</heading>
        </IconStyle>
        <ListStyle>
        </ListStyle>
    </Style>
    <Placemark id="point">
        <name>Chase Car</name>
        <LookAt>
            <latitude>%(lat).6f</latitude>
            <longitude>%(lon).6f</longitude>
            <altitude>0</altitude>
            <heading>0</heading>
            <tilt>0</tilt>
            <range>1000</range>
        </LookAt>
        <styleUrl>#msn_track</styleUrl>
        <Point>
            <coordinates>%(lon).6f,%(lat).6f,%(alt).1f</coordinates>
            <altitudeMode>absolute</altitudeMode>
        </Point>
    </Placemark>
""" % gps_track[-1]

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
            <tessellate>1</tessellate>
            <altitudeMode>absolute</altitudeMode>
            <coordinates>
            %s
            </coordinates>
        </LineString>
    </Placemark>
    """ % " ".join(["%(lon).6f,%(lat).6f,%(alt).1f" % loc for loc in gps_track])

    kml = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
    <name>Chase Car.kml</name>
    %s
    %s
</Document>
</kml>
""" % (pos_kml, track_kml)

    with open("/tmp/ground_station.kml", 'w') as kml_file:
        kml_file.write(kml)

gpsd = gps.gps(mode=gps.WATCH_ENABLE)
for msg in (msg for msg in gpsd if msg['class'] == 'TPV'):
    if msg['mode'] == 3:
        print(msg)
        gps_track.append(msg)
        write_kml()
