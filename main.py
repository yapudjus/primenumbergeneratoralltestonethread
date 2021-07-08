from datetime import timedelta
from decimal import Decimal
import signal
import os
import sys
import datetime
import time
import psutil
import platform


if platform.system() == 'Windows':
    import wmi
    import requests
    import zipfile
    print('running on windows')
    if not os.path.exists('.\\dependencies\\OpenHardwareMonitor\\'):
        os.makedirs('.\\dependencies\\OpenHardwareMonitor\\')
    if not os.path.exists('.\\dependencies\\OpenHardwareMonitor\\OpenHardwareMonitor.exe'):
        print('OHM isn\'t installed')
        url = 'https://openhardwaremonitor.org/files/openhardwaremonitor-v0.9.5.zip'
        r = requests.get(url, allow_redirects=True)
        open('.\\dependencies\\openhardwaremonitor.zip', 'wb').write(r.content)
        with zipfile.ZipFile('.\\dependencies\\openhardwaremonitor.zip', 'r') as zip_ref:
            zip_ref.extractall('.\\dependencies\\')
            print('OHM installed')
    os.system('start .\\dependencies\\OpenHardwareMonitor\\OpenHardwareMonitor.exe')

ToFind = sys.argv[1]
Next_save = int(sys.argv[2])
found = 0
teststr = 0
day = 0
Hour = 0
Minute = 0
Second = 0
hashrate = 0
prime = []
hashrate_calc_1 = 0
hashraye_calc_2 = datetime.datetime.now()
time.sleep(1)
hashrate_calc_3 = datetime.datetime.now()
begin_time = datetime.datetime.now()

with open('data.dat', 'rt') as myfile:  # Open data.dat for reading
    for myline in myfile:              # For each line, read to a string,
        exec(myline)                  # and execute the string

test = int(teststr)

line_count = 0
file = open("prime.txt", "r")
for line in file:
    if line != "\n":
        line_count += 1
file.close()

if line_count != found:
    print('detected an error during last save, numbers might not be accurate, prime numbers detected :',
          line_count, ', primes on last save :', found, ', timer might not be accurate')
    time.sleep(5.0)
    begin_time = begin_time + \
        datetime.timedelta(days=0, hours=0, minutes=0, seconds=5)
    found = line_count


TotalTime = datetime.timedelta(
    days=day, hours=Hour, minutes=Minute, seconds=Second)

# with open('prime.txt', 'rt') as myfile:  # Open prime.txt for reading
#     for myline in myfile:              # For each line, read to a string,
#         prime.append(myline)

# try:
#     while True:
#         prime.remove("\n")
# except ValueError:
#     pass


def Average(lst):
    return sum(lst) / len(lst)


def bye():
    global ElapsedTime
    global TotalTime
    # try:
    #     while True:
    #         prime.remove("\n")
    # except ValueError:
    #     pass
    ElapsedTime = (datetime.datetime.now() - begin_time)
    TotalTime += ElapsedTime
    print('elapsed time is ', ElapsedTime)
    print('saving.')
    textfile = open("prime.txt", "a")
    for ToWrite in prime:
        textfile.write(str(ToWrite) + "\n")
    textfile.close()
    print('saving..')
    os.remove("data.dat")
    textfile = open("data.dat", "w")
    textfile.write('teststr = ')
    textfile.write(str(test))
    textfile.write("\n")
    textfile.write('found = ')
    textfile.write(str(found))
    textfile.write("\n")
    # textfile.write("years = int('")
    # textfile.write(str(TotalTime.seconds % 60))
    # textfile.write("')\n")
    # textfile.write("month = int('")
    # textfile.write(str(TotalTime.seconds % 60))
    # textfile.write("')\n")
    textfile.write('day = int(')
    textfile.write(str(TotalTime.days))
    textfile.write(")\n")
    textfile.write('Hour = int(')
    textfile.write(str(TotalTime.seconds // 3600))
    textfile.write(")\n")
    textfile.write("Minute = int('")
    textfile.write(str(int(TotalTime.seconds / 60 % 60)))
    textfile.write("')\n")
    textfile.write("Second = int('")
    textfile.write(str(TotalTime.seconds % 60))
    textfile.write("')\n")
    textfile.close()
    print('saved')
    if platform.system() == 'Windows':
        os.system("taskkill /im OpenHardwareMonitor.exe")


def get_cpu_temp():
    global cpu_temps
    if platform.system() != 'Windows':
        t = psutil.sensors_temperatures()
        for x in ['cpu-thermal', 'cpu_thermal']:
            if x in t:
                return t[x][0].current
        print("Warning: Unable to get CPU temperature!")
        return 0
    else:
        cpu_temps = []
        w = wmi.WMI(namespace="root\OpenHardwareMonitor")
        sensors = w.Sensor()
        for sensor in sensors:
            if sensor.SensorType == u'Temperature' and 'CPU' in sensor.Name:
                cpu_temps.append(float(sensor.Value))
        return(Average(cpu_temps))


def signal_handler(signum, frame):
    signal.signal(signum, signal.SIG_IGN)  # ignore additional signals
    bye()  # give your process a chance to clean up
    sys.exit(0)


# register the signal with the signal handler first
signal.signal(signal.SIGINT, signal_handler)


while found != int(ToFind):
    ElapsedTime = (datetime.datetime.now() - begin_time)
    test += 1
    flag = 0
    for check in range(1, test, 1):
        hashrate_calc_1 += 1
        if hashrate_calc_1 == 100000:
            hashrate_calc_2 = datetime.datetime.now()
            hashrate = hashrate_calc_1 / \
                (hashrate_calc_2.timestamp()-hashrate_calc_3.timestamp())
            hashrate_calc_3 = datetime.datetime.now()
            hashrate_calc_1 = 0
        if (test % check) == 0:
            flag += 1
        if flag == 2:
            break
    if flag == 1:
        found += 1
        Next_save -= 1
        prime.append(test)
        print(test, 'is prime | found', found, '/', ToFind, '| time elapsed in this run is', ElapsedTime, '| total time is',
              TotalTime + ElapsedTime, '| hashrate is', round(Decimal(hashrate/1000000), 5), 'MH/s | next save in', Next_save, 'prime numbers found | CPU temps are', round(Decimal(get_cpu_temp()), 2), '°C')

    if Next_save == 0:
        # print('saving.')
        textfile = open("prime.txt", "a")
        for ToWrite in prime:
            textfile.write(str(ToWrite) + "\n")
        textfile.close()
        prime = []
        Next_save = int(sys.argv[2])

bye()
