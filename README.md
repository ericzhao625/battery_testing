# battery_testing

Code for controlling all things battery related.
Made for my own learning purposes and practice, as well as to help with Midnight Sun Solar Car development.

Largely inspired/learned/copied from here: https://github.com/mbA2D/Test_Equipment_Control



# Required setup notes (to document in an actual setup file):

Coded and tested on Python 3.8.0

pyvisa:
  pip install:
    - pyvisa
    - pyvisa-py
    - psutil
    - zeroconf
   NI-VISA backend
    - https://www.ni.com/en-ca/support/downloads/drivers/download/packaged.ni-visa.460225.html
    
E-load BK Precision 8600:
  - no extra downloads required
  - SCPI commands
  
PSU BK Precision 9103:
  - USB Virtual COM driver: https://l.bkprecision.com/products/power-supplies/9103-320w-multi-range-42v-20a-dc-power-supply.html
  - Uses their own "non-standard" serial protocol, check programming manual for commands: https://bkpmedia.s3.amazonaws.com/downloads/programming_manuals/en-us/9103_9104_series_programming_manual.pdf
