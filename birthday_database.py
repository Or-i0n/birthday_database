# Version: 1.0-20191031

import json


class Database:
    """Contains methods to read and write from database."""

    def __init__(self):
        self.filename = "birthdays.json"

    def read(self):
        """Reads data from database, if not found creates a new file."""
        try:
            with open(self.filename) as infile:
                json.load(infile)
        except FileNotFoundError as nofile:
            print("File not found! Creating new one.")
            with open(self.filename, "w") as outfile:
                json.dump([], outfile)

    def write(self, data):
        """Writes data to database."""
        with open(self.filename, "w") as outfile:
            json.dump(data, outfile)

dbs = Database().read()
