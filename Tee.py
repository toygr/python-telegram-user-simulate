import sys
from datetime import datetime


class Tee:
    def __init__(self, filename):
        self.file = open(filename, "a", encoding="utf-8")
        self.stdout = sys.stdout

    def write(self, data):
        self.file.write(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  {data}\n")
        self.stdout.write(data)

    def flush(self):
        self.file.flush()
        self.stdout.flush()

    def isatty(self):
        try:
            return self.stdout.isatty()
        except AttributeError:
            return False
