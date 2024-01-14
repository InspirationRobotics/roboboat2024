

# find a better way to do this, but this will work for now

import os
import time

def setpwm(channel, pwm):
    os.system("cd ~/maestro-linux && ./UscCmd --servo " + str(channel) + "," + str(int(pwm*4)))



def main():
    
#     while True:
#        channel = input("channel")
#        pwm = input("pwm")
#
#        if pwm > 1750:
#            pwm = 1750
#        elif pwm < 1250:
#            pwm = 1250

#        setpwm(channel, pwm)

    setpwm(0, 1500)
    setpwm(1,1500)
    time.sleep(3)
    input("ready")
    setpwm(0, 1700)
    setpwm(1,1700)
    #while True:
        #val = input("pwm value")
    #    setpwm(1,val)



if __name__ == "__main__":
    main()
