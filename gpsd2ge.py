#!/opt/local/bin/python3
import time
import gps
import fastkml
from shapely.geometry import Point, LineString

gps_track = []

ns = '{http://www.opengis.net/kml/2.2}'

def chasecar_point():
    last_point = gps_track[-1]

    chasecar_icon_style = fastkml.styles.IconStyle(
        ns=ns, 
        icon_href="http://maps.google.com/mapfiles/kml/shapes/track.png", 
        scale=2.0,
        heading=last_point['track'])

    chasecar_style = fastkml.styles.Style(
        ns=ns,
        styles=[chasecar_icon_style])

    chasecar_placemark = fastkml.kml.Placemark(
        ns=ns, 
        id="chasecar_head",
        name='Chase Car',
        description='Chase Car Position',
        styles=[chasecar_style])

    chasecar_placemark.geometry = fastkml.geometry.Geometry(
        ns=ns,
        geometry=Point(last_point['lon'], last_point['lat'], last_point['alt']),
        altitude_mode='absolute')

    return chasecar_placemark

def chasecar_track():
    chasecar_track_line_style = fastkml.styles.LineStyle(
        ns=ns,
        color="ffff8000",
        width=3.0)

    chasecar_track_style = fastkml.styles.Style(
        ns=ns,
        styles=[chasecar_track_line_style])

    chasecar_line = fastkml.kml.Placemark(
        ns=ns,
        id="chasecar_path",
        name="Chase Car Path",
        description="Chase Car Path",
        styles=[chasecar_track_style])

    line_data = [(loc['lon'], loc['lat'], loc['alt']) for loc in gps_track]
    if len(line_data) == 1:
        line_data.append(line_data[0])

    chasecar_line.geometry = fastkml.geometry.Geometry(
        ns=ns,
        geometry=LineString(line_data),
        altitude_mode='absolute',
        tessellate=True)

    return chasecar_line

def write_kml():
    kml_root = fastkml.kml.KML()

    kml_doc = fastkml.kml.Document(
        ns=ns,
        name="Chase Car")
    kml_doc.append(chasecar_point())
    kml_doc.append(chasecar_track())

    kml_root.append(kml_doc)

    with open("/tmp/gps_loc.kml", 'w') as kml_file:
        kml_file.write(kml_doc.to_string())

gpsd = gps.gps(mode=gps.WATCH_ENABLE)
for msg in (msg for msg in gpsd if msg['class'] == 'TPV'):
    if msg['mode'] == 3:
        print(msg)
        gps_track.append(msg)
        write_kml()
