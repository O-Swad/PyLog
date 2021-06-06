from __future__ import annotations
from clarity.logfile.log_file import LogFile


class ClarityChallengeFacade(object):
    """
    Facade for decoupling "main" program from LogFile logic
    """

    def __init__(self, file_name):
        self._file_name = file_name
        self._log_file = LogFile(file_name)

    def get_host_connected_to_in_period(self, init_datetime: int, end_datetime: int, host_to: str):
        """
        Get a list of hostnames connected to the given host during the given period
        :param init_datetime start time of the period
        :param end_datetime end time of the period
        :param host_to given host
        """
        hosts = []
        hosts = self._log_file.get_host_connected_to_in_period(int(init_datetime), int(end_datetime), host_to)
        self._print_hosts(hosts, f"HOSTS CONNECTED to {host_to} in period {init_datetime} - {end_datetime}",
                          f"There is no hosts connected to {host_to} in period {init_datetime} - {end_datetime}")

    def get_hosts_connected_to(self, host_to: str):
        """
        Run 'process' for getting a list of hosts connected to a given host
        :param host_to given host
        """
        hosts = self._log_file.get_hosts_connected_to(host_to)
        self._print_hosts(hosts,  f"HOSTS CONNECTED to {host_to}",  f"There is no hosts connected to {host_to}")

    def get_hosts_connected_from(self, host_from: str):
        """
        Run 'process' for getting a list of hosts connected from a given host
        :param host_from given host
        """
        hosts = self._log_file.get_hosts_connected_from(host_from)
        self._print_hosts(hosts, f"HOSTS CONNECTED from {host_from}",  f"There is no hosts connected from {host_from}")
    
    def get_most_connections_host(self):
        """
        Run 'process' for host which generated most connections
        """
        hosts = self._log_file.get_most_connections_host()
        self._print_hosts(hosts, f"HOST WITH MOST CONNECTIONS", f"There is no connections")

    @staticmethod
    def _print_hosts(hosts, hosts_message, no_hosts_message):
        if hosts:
            print(f'\n{hosts_message}')
            for host in hosts:
                print(host)
        else:
            print(f'\n{no_hosts_message}')



