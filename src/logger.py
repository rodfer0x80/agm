class Logger:
    def __init__(self):
        self.logfile = "./debug.log"
        with open(self.logfile, 'w') as h:
            h.write("")
        return None

    def log(self, log_msg=""):
        with open(self.logfile, 'a') as h:
            h.write(log_msg)
        return 0

