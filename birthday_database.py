# Version: 1.0-20191031

import json
import re


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


class App(Database):

    def __init__(self):
        pass


    def parse(self, userinput):
        pattern1 = r"(add) (\w+\s?\w*\s?\w*) (\d{4}/\d{2}/\d{2})"
        # print(re.match(pattern1, userinput, flags=re.IGNORECASE))
        if match:= re.match(pattern1, userinput, flags=re.IGNORECASE):
            print("cmd:", match.group(1), "name:", match.group(2), "dob:",
                match.group(3))

    def handle_userinput(self, userinput):
        if not userinput:
            print("Empty UserInput!")
        else:
            print("Adding", userinput)
            self.parse(userinput)


tests = ["", "add John Doe 1999/01/01", "add Sudhanshu Mohan Joshi 1954/11/11",
         "ADD James Hammond 1111/11/11"
        ]
app = App()

# Testing app
for test in tests:
    app.handle_userinput(test)
