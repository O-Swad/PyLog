import time
from collections import Counter, defaultdict
from clarity.logline.log_line import LogLine


class LogFile(object):
    """
    Class for managing log files
    """

    def __init__(self, name):
        # Name of the file
        self._name = name
        # Lines composed by timestamp host_from and host_to
        self._lines = list()
        # To compute hosts "connected from" in an efficient way
        self._hosts_from = Counter()
        # To access host "connected from" in an efficient way
        self._hosts_from_table = defaultdict(list)
        # To access host "connected to" in an efficient way
        self._hosts_to_table = defaultdict(list)
        # To compute the host that generates most connections
        self._hosts_most_connections = Counter()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def lines(self):
        return self._lines

    @lines.setter
    def lines(self, value):
        self._lines = value

    @property
    def host_from(self):
        return self._hosts_from

    @host_from.setter
    def host_from(self, value):
        self._hosts_from = value

    @property
    def host_from_table(self):
        return self._hosts_from_table

    @host_from_table.setter
    def host_from_table(self, value):
        self._hosts_from_table = value

    @property
    def host_to_table(self):
        return self._hosts_to_table

    @host_to_table.setter
    def host_to_table(self, value):
        self._hosts_to_table = value

    @property
    def host_most_connections(self):
        return self._hosts_most_connections

    @host_most_connections.setter
    def host_most_connections(self, value):
        self._hosts_most_connections = value

    def _parse_between(self, init_datetime, end_datetime, host_to):
        """
        Prepare internal data structures to get hosts connected to "host_to".
        Implements a reading algorithm based on iterators.
        (See https://docs.python.org/3/tutorial/inputoutput.html#methods-of-file-objects)
        @param init_datetime Beginning of the period in milliseconds
        @param end_datetime End of the period in milliseconds
        @param host_to Host for filtering connections to
        """
        try:

            # Reading the file with an iterator to not load all data in RAM
            with open(self._name) as file:
                for line in file:
                    tokenized_line = line.split()
                    log_line = LogLine(tokenized_line[0], tokenized_line[1], tokenized_line[2])
                    between_timestamps = init_datetime <= int(log_line.log_timestamp) <= end_datetime
                    is_host_to = log_line.host_dest == host_to
                    if between_timestamps and is_host_to:
                        self._hosts_from.update([log_line.host_ori])

        except IOError as error:
            print(error)

    def _parse_last_hour(self):
        """
        Prepare internal data structures to get hosts connected to, connected from and with most connections in
        the last hour.
        """
        # current time in milliseconds
        now_time = int(time.time() * 1000)
        one_hour_before = now_time - 3600000

        # To show information about the start timestamp of reference
        print(f"TIMESTAMP one hour ago {one_hour_before}")

        try:

            # Reading the file with an iterator, line by line, to not load all data in RAM
            with open(self._name) as file:
                for line in file:
                    tokenized_line = line.split()
                    log_line = LogLine(tokenized_line[0], tokenized_line[1], tokenized_line[2])
                    last_hour_timestamps = int(log_line.log_timestamp) >= one_hour_before  # miliseconds
                    if last_hour_timestamps:
                        self._hosts_from_table[log_line.host_ori].append(log_line.host_dest)
                        self._hosts_to_table[log_line.host_dest].append(log_line.host_ori)
                        self._hosts_most_connections.update([log_line.host_ori])

        except IOError as error:
            print(error)

    def get_host_connected_to_in_period(self, init_datetime: int, end_datetime: int, host_to: str) -> list:
        """
        get a list of hostnames connected to the given host during the given period
        :param init_datetime start time of the period
        :param end_datetime end time of the period
        :param host_to given host
        """
        self._parse_between(init_datetime, end_datetime, host_to)
        return self._hosts_from.most_common()

    def get_hosts_connected_to(self, host_to: str) -> list:
        """
        get a list of hostnames connected to a given host
        :param host_to: given host
        :param hosts: list of hosts in the last hour
        :return: list of hostnames connected to the given host
        """
        if len(self._hosts_to_table) == 0:
            self._parse_last_hour()

        return set(self._hosts_to_table[host_to])

    def get_hosts_connected_from(self, host_from: str) -> list:
        """
        get a list of hostnames connected from a given host
        :param host_from: given host
        :return: list of hostnames connected from the given host
        """
        if len(self._hosts_from_table) == 0:
            self._parse_last_hour()

        return set(self._hosts_from_table[host_from])

    def get_most_connections_host(self) -> list:
        """
        get the host which opened more connections (from hosts)
        :param hosts: list of hosts in the last hour
        :return: list of hostnames connected to the given host
        """
        return self._hosts_most_connections.most_common(1)

