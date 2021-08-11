#Very, very simple monitor for activity analytics purposes. Just configure it and run it in the host computer. 

from os import write
from socket import gethostname
from win32gui import GetWindowText, GetForegroundWindow, GetCursorPos
from time import sleep
from datetime import datetime, timedelta
from Cfg import Config


#Just initiates the startup of the file
def init():
    hstnm = gethostname()
    write_file("Desktop Usage Analytics -------- Startup for machine " + str(hstnm), Config.LOG_PATH)
    
#Writes logs to the file
def write_file(content, file):
    with open(file,"a") as f:
        time = datetime.now()
        f.writelines(time.strftime("%d/%m/%Y %H:%M:%S ") + content +"\n")

#Main function

def main():
    #Temp vars
    init()

    last_window = ""
    old_cur_pos = ""
    # Main loop
    while Config.CONTINUE:
        window = GetWindowText(GetForegroundWindow())
        cur_pos = GetCursorPos()
        if (window != last_window and last_window != ""):
            write_file(Config.WINDOW_CHANGE_MSG +window,Config.LOG_PATH)
        
        last_window = window

        if(cur_pos == old_cur_pos):
            Config.IDLE_SECS += 1
        else:
            Config.IDLE_SECS = 0

        old_cur_pos = cur_pos

        if(Config.IDLE_SECS == Config.NUM_SECS):
            write_file(Config.INACTIVE_USER_MSG +str(Config.NUM_SECS),Config.LOG_PATH)
            Config.TOTAL_IDLENESS += Config.NUM_SECS
            Config.IDLE_SECS = 0

        sleep(Config.SECONDS)

try:
    main()
except KeyboardInterrupt:
    write_file(Config.ABORTED_EXEC_MSG, Config.LOG_PATH)
    write_file(Config.FINAL_INACTIVITY_MSG + str(timedelta(seconds=Config.TOTAL_IDLENESS)),Config.LOG_PATH)