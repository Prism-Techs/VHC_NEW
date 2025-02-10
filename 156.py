import subprocess as sp

def find_usb():
    output = sp.getoutput("df -x squashfs")    
    poss=output.find("/media")    
    if poss == -1:
        return("false")
    else :
        out =output[poss:]
        return(out)
    
state = find_usb()
print(state)


    
