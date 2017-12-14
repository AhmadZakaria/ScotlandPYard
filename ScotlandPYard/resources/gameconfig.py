#!/usr/bin/env python

base = 'background-color: {}; color: {}; border-style: outset; border-width: 1; border-radius: 10px; border-color: beige; font: bold 14px; min-width: 10em; padding: 2px;'

stylesheet = {
    'Underground': base.format("red", "black"),
    'Taxi': base.format("yellow", "black"),
    'Bus': base.format("green", "black"),
    "2x": base.format("orange", "black"),
    "BlackTicket": base.format("black", "white")
}
