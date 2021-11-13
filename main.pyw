from win32gui import GetForegroundWindow
import psutil
import time
from datetime import datetime
import win32process
import csv
import os
from win10toast import ToastNotifier

toast = ToastNotifier()
toast.show_toast("Activity Tracker", "Activity tracking has been turned on.")

os.chdir("C:/Users/petar/python_projects/activity_tracker")

def set_filename():
    today = datetime.now().strftime("%Y-%m-%d")
    return f"activity_{today}.csv"

process_time={}
in_btw_time = {}


for name in os.listdir():
    if name == set_filename():
        with open(name, "r", newline="") as file:
            rows = []
            for row in file:
                row = row.strip()
                rows.append(row.split(','))

            rows[1] = [int(val) for val in rows[1]]

            process_time = dict(zip(*rows))
  
while True:
    try:
        current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")
    except psutil.NoSuchProcess:
        pass
    except ValueError:
        pass
    else:
        if current_app not in in_btw_time:
            in_btw_time[current_app] = 0

        in_btw_time[current_app] = in_btw_time[current_app] + 1
        
        if in_btw_time[current_app] == 60:
            in_btw_time[current_app] = 0

            if current_app not in process_time.keys():
                process_time[current_app] = 0

            process_time[current_app] = process_time[current_app] + 1

        with open(set_filename(), "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(process_time.keys())
            writer.writerow(process_time.values())

        time.sleep(1)
