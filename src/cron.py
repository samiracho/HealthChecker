import threading
import time
from config import Config
from check import Check
import os
import signal


class Cron(object):

    def __init__(self, server, interval=300):
        """
        :param server: Bottle server reference
        :param interval: Interval in seconds
        """
        self.interval = interval
        self.server = server
        thread = threading.Thread(target=self.run_background, args=())
        thread.daemon = True
        thread.start()

    def run_background(self):
        """
        We trigger the health checks periodically in a background process
        """
        while True:

            config_path = os.getenv('HK_CONFIG_PATH', "resources/config.yaml")
            cfg = Config(path=config_path)

            if not cfg.data:
                print("ERROR: No health-checks valid config found. Please check syntax.")
            else:
                try:
                    print(time.strftime("%c")+" Checking endpoints")
                    chk = Check(cfg.data)
                    chk.check_endpoints()
                    chk.send_notifications()
                    print(time.strftime("%c") + " Endpoints checked")
                except Exception as e:
                    print("ERROR: Killing application. Reason:\n"+str(e))
                    #os.kill(os.getpid(), signal.SIGTERM)
                    #sys.exit()
                    self.server.stop()

            time.sleep(self.interval)
