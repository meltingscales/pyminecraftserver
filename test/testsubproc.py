import os
import subprocess
import time

if __name__ == '__main__':
    if os.name == 'nt':
        myproc = subprocess.Popen(['notepad.exe', os.path.abspath(__file__)])
    else:
        myproc=subprocess.Popen(['gedit', os.path.abspath(__file__)])

    time.sleep(2)

    myproc.kill()

    print(myproc)
