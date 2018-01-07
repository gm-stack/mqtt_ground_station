# mqtt_ground_station
MQTT based ground station code for auto_rx

Open `ground_station.kml` in Google Earth.

`gpsd2ge.py` reports current gpsd position into Google Earth.

`sondes.py` shows current sonde positions.

I'd suggest not using this yet - it's very much in development.

Todo:
- configurable server, auth support
- serve as webserver instead of file on disk?
- merge two scripts into one?
- cull older points to reduce number of track points
- different colours for balloons / chase car
- support for prediction service