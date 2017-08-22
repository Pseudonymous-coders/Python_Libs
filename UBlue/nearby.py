import time
import bluetooth

def search():
    devices = bluetooth.discover_devices(duration=10, lookup_names = True)
    return devices

if __name__=="__main__":
    while True:
        results = search()
        if (results!=None):
            for addr, name in results:
                print "{0} - {1}".format(addr, name)
            print "Thats it..."
        else:
            print "None Found..."
            #endfor
        #endif
        time.sleep(2)
    #endwhile