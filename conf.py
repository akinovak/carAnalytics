import os
import logging
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class Configuration:

    def __init__(self):
        self.logger_path = os.path.join(ROOT_DIR, 'logger.log')
        self.server_timeout = 18000
        self.client_timeout = 5
        self.log = logging
        self.log.basicConfig(filename=self.logger_path, level=logging.DEBUG)


ctx = Configuration()

