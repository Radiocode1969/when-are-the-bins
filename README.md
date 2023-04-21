# when-are-the-bins

Something simple in Python 3 to display when Wiltshire Council intends to collect refuse bins
using a Pimoroni Blinkt! RGB LED hat and a Raspberry Pi Zero W that is already connected to your network.

Very hacky with no warranty given. It interrogates the Wiltshire Council website with a pre-formed
query then processes the output to illuminate LEDs on the Blinkt!, giving a week+ of notice for
each bin type:
Green - Garden Recycling
Blue - Blue cardboard and metal
Orange - Household waste
The flashing LED is today, with the relevant colour, or White if today is bin-free.
.
LEDs are off between 23:00 and 06:00 every day, and the information is updated just after midnight.
(Yes, I know I could cache the query results but it isn't unknown for Wiltshire Council to change
bin dates at short notice due to crew availability or poor weather.)

TODO:
1. Fix year rollover (Low priority)
2. Port to Pico W
