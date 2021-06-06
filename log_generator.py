import time
import random

hours = 2  # two hours of data
now_time = int(time.time()*1000)  # milliseconds
last_time = now_time - 3600 * 1000 * hours
hosts = ['everest', 'annapurna', 'lhotse', 'manaslu', 'dhaulagiri']
separator = ' '
counter = 0

with open('test-log-file.txt', 'a') as log_file:
    for log_timestamp in range(last_time, now_time):
        host_ori, host_dest = random.sample(hosts, 2)
        tokens = (str(log_timestamp), host_ori, host_dest)
        line = separator.join(tokens) + '\n'
        log_file.write(line)

        counter += 1

print('Líneas: ' + str(counter))
