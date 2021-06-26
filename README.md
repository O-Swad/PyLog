# PyLog
A Python log parser that scales.

## Source code documentation
[pdoc](https://pdoc3.github.io/pdoc/) style documentation can be viewed on [source code documentation](https://o-swad.github.io/clarity-challenge/docs/clarity/).

## Assumptions:
    1. timestamp is always in milliseconds
    2. "last hour" is the last hour of the current system time not the last of the timestamps of the file
    3. The log file has a maximum of a line for each timestamp
    4. The size of log lines is variable
    5. Performance is a high priority

## Install
```commandline
tar -xzvf pylog.tar.gz
cd pylog
python3 -m clarity.app.app -h

```

## Run

1. **Asking for help**: `python3 -m clarity.app.app -h`
```
usage: app.py [-h] [--init_datetime INIT_DATETIME] [--end_datetime END_DATETIME] [--host HOST] [--connected_from CONNECTED_FROM]
              [--connected_to CONNECTED_TO] [--watch WATCH] [--buffer_size BUFFER_SIZE]
              logfile

A tool for parsing logfiles

positional arguments:
  logfile               Name of the log file for processing

optional arguments:
  -h, --help            show this help message and exit
  --init_datetime INIT_DATETIME
                        init datetime of the period for retrieving hosts
  --end_datetime END_DATETIME
                        end datetime of the period for retrieving hosts
  --host HOST           host name during the giving period
  --connected_from CONNECTED_FROM
                        Provides a list of hostnames connected from host (eg.:'lhotse') during the last hour
  --connected_to CONNECTED_TO
                        Provides a list of hostnames connected to host (eg.:'everest') the last hour
  --watch WATCH         collect input from the file by n seconds while it's being written and run indefinitely. Default = 3600 seconds
  --buffer_size BUFFER_SIZE
                        Size of RAM (KBytes) used for reading the file in chunks. 512 Kb by default
```

2. **Parse the data with a time_init, time_end**:
To get hosts connected to "Matina" between "1565647204351" and "1565733598341" timestamps
```commandline
python3 -m clarity.app.app --init_datetime 1565647204351 --end_datetime 1565733598341 --host Matina ../tests/input-file-10000.txt
```

```commandline
HOSTS CONNECTED to Matina in period 1565647204351 - 1565733598341
('Aadvik', 1)
('Evontae', 1)
('Sharekia', 1)
('Dadrianna', 1)
('Donathon', 1)
('Sarri', 1)
('Kristyan', 1)
('Adanya', 1)
('Victory', 1)
('Rilah', 1)
```
It is shown the hosts and the number of times connected to Matina.

3. **Unlimited Input Parser**:
To get hosts that were connected from "manaslu" and connected to "everest", and read "test-log-file.txt"
   every 10 seconds ("watch 10")
```commandline
python3 -m clarity.app.app --connected_from manaslu --connected_to everest --watch 10 test-log-file.txt
```
```commandline
TIMESTAMP one hour ago 1622971646787

HOSTS CONNECTED from manaslu
lhotse
dhaulagiri
annapurna
everest

HOSTS CONNECTED to everest
lhotse
manaslu
dhaulagiri
annapurna

HOST WITH MOST CONNECTIONS
('lhotse', 670777)
```
It is shown the hosts and the host that opened most connections with the number of connections (670777).


## Tests files
Log files for testing purposes can be generated using the files generate_connection.sh and 
log_generator.py. 

1. **Add a connection to a file**
   ```commandline
    ./generate_connection.sh -f "omar" -t "everest" -o "test-file"
   ```
   It adds a connection to "test-file" from "omar" to "everest" wit current UNIX timestamp in milliseconds
   ```
   1622974319223 omar everest
   ```
   
2. **Generate a test file (test-log-file.txt)**
```commandline
python3 log_generator.py
```
It will generate
a file with connections between several hosts. This file is mainly 
generated for testing time performance of the solution. It can be customized to generate hours of 
data in milliseconds:
```python
...

hours = 2  # two hours of data
now_time = int(time.time()*1000)  # milliseconds
last_time = now_time - 3600 * 1000 * hours
hosts = ['everest', 'annapurna', 'lhotse', 'manaslu', 'dhaulagiri']
separator = ' '

...
```

## Architecture of the solution
### UML diagram
![UML diagram](https://o-swad.github.io/clarity-challenge/docs/uml.jpg)

### Other alternative design inspired on compiler construction principles
To design a specific parser for log files (eg.: LogFileParser) for extracting data items represented
by each line, and not implementing parse funcionality in LogFile class. At the same time, to create
a log filterer class (eg.: LogFileFilterer) for filtering hosts given specific rules, and not
implementing filtering funcionality on LogFile class.

LogFileParser could be parametrized with different algorithms for parsing at runtime 
(Strategy design pattern).

## Algorithm for parsing
Connections are computed at the same time of reading file, using [Counter](https://docs.python.org/3/library/collections.html#collections.Counter) and 
a dict of lists ([defaultdict](https://docs.python.org/3/library/collections.html#collections.defaultdict)) 
from [collections](https://docs.python.org/3/library/collections.htm) package.
File is read with an iterator using [File Objects](https://docs.python.org/3/tutorial/inputoutput.html). 

*From python documentation*:
> For reading lines from a file, you can loop over the file object. 
> This is memory efficient, fast, and leads to simple code
> ```python
> for line in f:
>    print(line, end='')
> ```

My code:
````python
# Reading the file with an iterator to not load all data in RAM
with open(self._name) as file:
    for line in file:
````
See [Methods of File Objects](https://docs.python.org/3/tutorial/inputoutput.html#methods-of-file-objects)

##  Performance improvements ideas
1. Split large files into smaller files and computing each them separately and joining them in
one result. (Map-reduce strategy)
2. Indexing the text file by host and timestamp (two index files)
3. Using timestamp to seek to specific position when searching a period of time (eg.: Binary search)


