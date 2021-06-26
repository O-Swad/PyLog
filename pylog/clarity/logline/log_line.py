class LogLine(object):

    """
    Class to encapsulate lines of the log
    """

    def __init__(self, log_timestamp, host_ori, host_dest):
        self._log_timestamp = log_timestamp
        """ timestamp """
        self._host_ori = host_ori
        """host from"""
        self._host_dest = host_dest
        """host to"""

    @property
    def log_timestamp(self):
        return self._log_timestamp

    @log_timestamp.setter
    def log_timestamp(self, value):
        self._log_timestamp = value

    @property
    def host_ori(self):
        return self._host_ori

    @host_ori.setter
    def host_ori(self, value):
        self._host_ori = value

    @property
    def host_dest(self):
        return self._host_dest

    @host_dest.setter
    def host_dest(self, value):
        self._host_dest = value

    def __str__(self):
        return self.log_timestamp + ' ' + self.host_ori + ' ' + self.host_dest
