from dac_lib_soft import mup4728
import time
dac = mup4728(0x61)#
dac.INNER_LED(2100)
while(1):
    a=1

