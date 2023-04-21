# bins.py - use  a raspberry pi to display which bin needs to go out
# Uses Wiltshire Council's waste collection calendar to provide dates

# Version_Major = 1
# Version_Minor = 0 
# Date = '20230421'
# Author = 'Lee Wiltshire'

# This solution is hacky. Use Safari html inspector to determine the
# value for Uprn (required line 55). Note that only valid services are 
# displayed - if you want them all, including garden waste, choose an address 
# that pays for the service.

# Process:
# Get today's date
# Get the bin dates for the year/month
# Use datetime to calculate the number of days from today to each event
# If -1 < num_days <= 1 then light the correct colour

# Added  in version 0.3:
# Make the whole program run as a continuous loop
# Version 0.4:
# Corrected a logic problem for month rollover
# Version 0.5:
# Added logic to turn off the output between 23:00 and 06:00
# Version 0.6:
# Corrected Version 5 logic
# Version 1.0: Put onto Github


import requests
import datetime
import blinkt
import time

has_run = False  # Use this flag to determine what to use
bright = 0.1
max_days = 7  # window to display

blinkt.set_clear_on_exit(False)	# Clear the display if the process ends
blinkt.set_all(0,0,0)
blinkt.set_brightness(bright)
blinkt.show()

while True:     # Saved-up problem - need to deal with year rollover at some time
    if has_run == False:    # Start of the day or first run today, so get all of the information
        has_run = True
        flash_flag = False     #Do we flash the bottom LED? (this might be something we do automagically anyway)
        count = 0
        blinkt.set_pixel(0, 64, 0, 0, bright)
        today = datetime.date.today()
        for mon in range(today.month, today.month + 2):
            # print('Month: ', mon)
            # print(today)
            url = 'https://ilforms.wiltshire.gov.uk/WasteCollectionDays/CollectionList'
            payload = {'Month': mon, 'Year': '2023', 'Postcode': 'YourPostcode', 'Uprn': '12 digit number'}
        
            # POST with form-encoded data
            req = requests.post(url, data=payload)
            # print(req.status_code)
            p = 0
            q = 0
            r = 0
        
            # Work through the month, and get the days
            while True:
                p = req.text.find('cal-cell-active', p)
                if p == -1:
                    break   # not found
                m = p #use this later
                q = req.text.find('rc-event-container', p + 1)
                r = req.text.find('</span></div>', q + 1)
                #print('-------------')
                #print(req.text[p-30:r+13])
                #print()
                #print('p = ', p, '  q = ', q, '  r = ', r)
                count += 1
                p = r + 1
                # Extract date and collection type
                j = req.text.find('data-cal-date="',m)
                adate = req.text[j+15:j+25]
                #print(adate[-2:], adate[5:7], adate[0:4])
                k = req.text.find('"event service-',j+25)
                aservice = req.text[k+15:k+18]
                x = datetime.date(int(adate[0:4]), int(adate[5:7]), int(adate[-2:]))
                
                #print(adate[-2:], adate[5:7], adate[2:4], aservice)
                delta = x - today
                
                if 0 <= delta.days <= max_days:
                    print('Get Ready!!')
                    print(x, aservice, delta.days)
                    if aservice == 'pod':     # Blue/black bin
                        r_val = 0
                        g_val = 0
                        b_val = 255
                    elif aservice == 'cgw':   # Green garden bin
                        r_val = 0
                        g_val = 255
                        b_val = 0
                    elif aservice == 'res':   # Grey (Brown) Rubbish bin
                        r_val = 175
                        g_val = 50
                        b_val = 0
                    else:
                        r_val = 255
                        g_val = 255
                        b_val = 255
        
                    blinkt.set_pixel(delta.days, r_val, g_val, b_val, bright)
                    blinkt.show()
                    if delta.days == 0:
                        flash_flag = True
                # We have done the display bit
                # Get the current value  for pixel zero (hot off the press)
                
            r_get, g_get, b_get, bri_get = blinkt.get_pixel(0)
            odd_even = True
            yesterday = today
            tc = datetime.datetime.now()
            ts = tc.second  #get the current seconds
    while True:     # Do forever until we get to tomorrow
        time.sleep(0.07)
        today = datetime.date.today()  
        if yesterday != today:      # Its a new day!!
            blinkt.set_all(0,0,0)
            blinkt.show()
            has_run = False
            break       # go back around, gather the data
        tn = datetime.datetime.now()
        tns = tn.second
        if tns != ts:
            ts = tns  # update the seconds
            if odd_even == True:
                odd_even = False
                blinkt.set_pixel(0, r_get, g_get, b_get, bri_get)
                # blinkt.show()
                # print('ON')
            else:
                odd_even = True
                blinkt.set_pixel(0, 0, 0, 0)
                # blinkt.show() 
                # print('OFF')
         
        x = datetime.datetime.now()
        if x.hour > 20 or x.hour < 6:
            # Turn the display off, rather than set all pixels to zero
            blinkt.set_brightness(0)
        else:
            blinkt.set_brightness(bright)
        blinkt.show()       
            
            #print('------------')
            
    # End of if has_run == False at top
# End of While True at top



