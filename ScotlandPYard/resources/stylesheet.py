#!/usr/bin/env python

base = ''' QPushButton {{
              background-color: {};
              color: {};
              border-style: outset; 
              border-width: 1; 
              border-radius: 10px; 
              border-color: beige; 
              font: bold 14px; 
              min-width: 10em; 
              padding: 2px;
            }}
           
            QPushButton:hover{{
              background-color:{};
            }}
            
            QPushButton:disabled{{
              background-color:gray;
            }}
           
'''
stylesheet = {
    'Underground': base.format("red", "black", "darkred"),
    'Taxi': base.format("yellow", "black", "darkgoldenrod"),
    'Bus': base.format("blue", "black", "darkblue"),
    "2x": base.format("orange", "black", "darkorange"),
    "BlackTicket": base.format("black", "white", "gray")
}
