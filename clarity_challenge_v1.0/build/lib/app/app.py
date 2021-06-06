import argparse
import time
from clarity.facade.clarity_challenge_facade import ClarityChallengeFacade


class App(object):

    def __init__(self, arguments):
        self._arguments = arguments

    def run(self):
        """
        Entry point to the program
        """
        # for running indefinitely if 'watch' is passed
        if self._arguments.watch:
            while True:
                self.watch(self.main(), int(self._arguments.watch))
        else:
            self.main()

    def main(self):
        """
        pipeline for running the main processes
        :param arguments: arguments from command line
        """
        facade = ClarityChallengeFacade(self._arguments.logfile)
        between_period = self._arguments.init_datetime and self._arguments.end_datetime and self._arguments.host
        watch_from_to = self._arguments.watch and self._arguments.connected_from and self._arguments.connected_to

        if between_period:
            facade.get_host_connected_to_in_period(self._arguments.init_datetime, self._arguments.end_datetime, self._arguments.host)
        elif watch_from_to:
            facade.get_hosts_connected_from(self._arguments.connected_from)
            facade.get_hosts_connected_to(self._arguments.connected_to)
            facade.get_most_connections_host()

    def watch(self, func, seconds=3600):
        """
        wrapper for running another function and wait n seconds
        :param func: function to run
        :param seconds: seconds to wait. 3600 seconds by default
        """
        func
        time.sleep(seconds)


if __name__ == "__main__":

    options_parser = argparse.ArgumentParser(description='A tool for parsing logfiles')
    options_parser.add_argument('logfile', help="Name of the log file for processing")
    options_parser.add_argument('--init_datetime', help="init datetime of the period for retrieving hosts")
    options_parser.add_argument('--end_datetime', help="end datetime of the period for retrieving hosts")
    options_parser.add_argument('--host', help="host name during the giving period")

    options_parser.add_argument('--connected_from', help="Provides a list of hostnames connected from host (eg.:'lhotse')"
                                                       "during the last hour")
    options_parser.add_argument('--connected_to', help="Provides a list of hostnames connected to host (eg.:'everest') "
                                                     "the last hour")
    options_parser.add_argument('--watch', help="collect input from the file by n seconds while it's being written and "
                                                "run indefinitely. Default = 3600 seconds")
    args = options_parser.parse_args()

    app = App(args)
    app.run()



