# raspberry-rfid-sonos-player
rfid reader via python; starting sonos playlist via node-sonos-http-api

RaspberryPi
- Runs this python script
- The script reads the RFID and maps it to a playlist item

node-sonos-http-api
- Running on some other server
- The script triggers a request to the node-sonos-http-api which starts the playlist.

Sonos
- Has the playlist
