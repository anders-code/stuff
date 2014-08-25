#!/usr/bin/env python

import sys
from array import array

# this library is jacked up, should not have to do this
# I'll probably fork/rewrite it, saving the bits that work
# for now it is quick to start
from pyftdi.ftdi import Ftdi


f = Ftdi()

# reset the FTDI chip
# HA! this can interrupt a continous clock forever mode
# to do something new

f.open_mpsse(0x403, 0x6014)
f.usb_dev.reset()
f.close()
print "reset!"

# here's the normal open
f.open_mpsse(0x403, 0x6014)

if len(sys.argv) > 1:
  freq = int(sys.argv[1])
else:
  freq = 1000 # or whatever

print "set freq: %d" % (freq,)
f.set_frequency(freq)

# key #1 - must set pins to output
# this drives the TMS high also, will force JTAG reset in short order
# will drive clock pin high too! If you comment out the rest of the script
# you can test any of the GPIO with this
f.write_data(array('B', [0x80, 0xff, 0xff]))
f.write_data(array('B', [0x82, 0xff, 0xff]))

# continuous clock forever
# but you cannot command the FTDI until GPIO1 goes low
# which is never because it is an output driven to 1 above
# OR until we do a usb_dev.reset() - now best option
f.write_data(array('B', [0x95]))

# 8 sec burst method
# send 7d0 = 2000*8 clocks
# could use this method in a loop so that the frequency and other bits
# could be changed, periodically
#f.write_data(array('B', [0x9d, 0xd0, 0x07]))

# or try multiple commands:
#f.write_data(array('B', [0x9d, 0xd0, 0x07, 0x9d, 0xd0, 0x07]))

f.close()
