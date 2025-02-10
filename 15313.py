import ctypes
import ctypes.util
import os
import subprocess as sp

state=os.system('df -x squashfs')
print(state)
out=str(state)
poss=out.find("media")
print("poss=",poss)
