#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import requests
import time

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

BASEURL = "http://192.168.0.4:5005/Wohnzimmer/"

playlists = {}
playlists["12-345-67-890-000"] = "Playlist 1"
playlists["11-222-33-444-555"] = "Playlist 2"

print playlists

# Welcome message
print "Welcome to the Sonos player"

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        cardId = "-".join(str(n) for n in uid)
        if cardId in playlists:
            print requests.get(BASEURL + "say/"+ playlists[cardId] + "/de/13").text
            print "Card ID %s, selecting playlist %s" % (cardId, playlists[cardId])
            print requests.get(BASEURL + "playlist/" + playlists[cardId]).text
            print "Setting volume back to 15"
            print requests.get(BASEURL + "volume/15").text

            time.sleep(5) 
        else:
            print "Could not match card id %s to any playlist" % cardId
            print requests.get(BASEURL + "say/No playlist found/8").text
    time.sleep(0.5)
