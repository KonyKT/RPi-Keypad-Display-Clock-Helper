import RPi.GPIO as GPIO
import dht11
import time
import datetime
import lcddriver
import Keypad
from Watek import Thrd
# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = lcddriver.lcd()
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)

ROWS = 4        # number of rows of the Keypad
COLS = 4        #number of columns of the Keypad
keys =  [   '1','2','3','A',    #key code
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D'     ]
rowsPins = [36,38,40,29]        #connect to the row pinouts of the keypad
colsPins = [31,33,35,37]        #connect to the column pinouts of the keypad

instance =dht11.DHT11(pin=13)

buzzer = 15
GPIO.setup(buzzer,GPIO.OUT)

global state
godzina = [6,6,6,6]

def budzik():
    display.lcd_clear()
    display.lcd_display_string("Wpisz godzine",1)
    time.sleep(2)
    display.lcd_clear()
    display.lcd_display_string("*-ok  #-anuluj",2)
    data = []
    keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS)    #creat Keypad object
    keypad.setDebounceTime(50)      #set the debounce time
    flag = 0
    global state
    while(True):
        key = keypad.getKey()
        if(key!= keypad.NULL):
            if( key.isnumeric()):
                godzina[flag%4] = key
                display.lcd_display_stringg(key,1,3+flag%4)
                flag = flag+1
            elif(key == '#'):
                return 0
            elif(key == '*'):
                if(int(godzina[0]) > 2 or int(godzina[2]) > 5):
                    display.lcd_display_string("Zla godzina",1)
                    print(godzina[0],godzina[1],godzina[2],godzina[3])
                    time.sleep(2)
                elif (int(godzina[0]) == 2 and int(godzina[1]) > 3):
                    display.lcd_display_string("Zla godzina",1)
                    print(godzina[0],godzina[1],godzina[2],godzina[3])
                    time.sleep(2)
                else:
                    state = 1
                    return 0
                break
            else:
                continue
    return 0
    
def buzz():
    display.lcd_clear()
    display.lcd_display_string("Buzzer test", 1)
    GPIO.output(buzzer,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(buzzer,GPIO.LOW)
    starter()

if __name__ == '__main__':
    print("startuje")
    state = 0
    display.lcd_display_string("Witam konsumenta",1)
    try:
        GPIO.output(buzzer,GPIO.LOW)
        keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS)    #creat Keypad object
        keypad.setDebounceTime(50)      #set the debounce time
        t = Thrd(idd=10,sleep_interval=100)
        t.start() 
        while(True):
            if  (state == 1):
                dt = datetime.datetime.now()
                H = str(godzina[0] + godzina[1])
                M = str(godzina[2] + godzina[3])
                h = dt.strftime("%H")
                m = dt.strftime("%M")
                if(H == h and M == m):
                    print("ALARM")
                    t.kill()
                    key = 'alarm'
                    t = Thrd(idd=key,sleep_interval=3)
                    t.start()
                    while(True):
                        key = keypad.getKey()
                        if(key != keypad.NULL):
                            if(key == '#'):
                                t.kill()
                                break
                    display.lcd_clear()
                    time.sleep(1)
                    t = Thrd(idd=10,sleep_interval=100)
                    t.start()
                    print("ALARM")
                    state = 0
                    godzina = [9,9,9,9]
            key =  keypad.getKey()
            if(key != keypad.NULL):
                if(key == 'A'):
                    t.kill()
                    t = Thrd(idd=key,sleep_interval=1)
                    t.start() 
                elif(key == 'B'):
                    t.kill()
                    t = Thrd(idd=key,sleep_interval=10)
                    t.start() 
                elif(key == 'C'):
                    t.kill()
                    budzik()
                    t = Thrd(idd=10,sleep_interval=100)
                    print(state)
                    print(godzina)
                    t.start()
                elif(key == 'D'):
                    t.kill()
                    t = Thrd(idd=key,sleep_interval=100)
                    t.start()
                    t.join()
                    t = Thrd(idd=10,sleep_interval=100)
                    t.start()
                else:
                    continue

    except (key != keypad.NULL):
        print("GOWNO")

    
    except KeyboardInterrupt:
     print("Cleanup")
     GPIO.cleanup()
     display.lcd_clear()





