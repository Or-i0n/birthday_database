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
                return json.load(infile)
        except FileNotFoundError as nofile:
            print("File not found! Creating new one.")
            with open(self.filename, "w") as outfile:
                json.dump({}, outfile)
            return self.read()


    def write(self, data):
        """Writes data to database."""
        database = self.read()
        userid = len(database) + 1
        newdata = {userid: data}
        database.update(newdata)
        print(f"{newdata=}")

        with open(self.filename, "w") as outfile:
            json.dump(database, outfile)

        print("Database:", self.read())


class App(Database):

    def __init__(self):
        super().__init__()


    def parse(self, userinput):
        pattern1 = (r"(-a) ([A-Za-z]+\s?[A-Za-z]*\s?[A-Za-z]*) "
                    r"(\d{4}/\d{2}/\d{2})")
        pattern2 = (r"(-y|-m|-d) (\d{2,4})"
                    r"|([A-Za-z]+\s?[A-Za-z]*\s?[A-Za-z]*)")

        # print(re.match(pattern1, userinput, flags=re.IGNORECASE))
        if match := re.match(pattern1, userinput, flags=re.IGNORECASE):
            # print("p1", match.groups())
            cmd, name, dob = match.groups()
            print(f"p1 {cmd=} {name=} {dob=}")
            return cmd, name, dob
        elif match := re.match(pattern2, userinput, flags=re.IGNORECASE):
            # print("p2", match.groups())
            if (cmd := match.group(1)) and (query := match.group(2)):
                print(f"p2-c1 {cmd=} {query=}")
                return cmd, query
            elif name := match.group(3):
                print(f"p2-c2 {name=}")
                return name

    def handle_data(self, userinput):
        parsed_data = self.parse(userinput)

        if len(parsed_data) == 3:
            cmd, name, dob = parsed_data
        elif len(parsed_data) == 2:
            cmd, query = parsed_data
        elif len(parsed_data) == 1:
            name = parsed_data

        if cmd == "-a":
            print(f"Adding {name} {dob} in database.")
            self.write([name, dob])



    def handle_userinput(self, userinput):
        if not userinput:
            print("Empty UserInput!")
        else:
            print("Parsing:", userinput)
            self.handle_data(userinput)


# tests = ["", "-a John Doe 1999/01/01", "-add Sudhanshu Mohan Joshi 1954/11/11",
#          "ADD James Hammond 1111/11/11", "Radha Mohan", "Ram", "-year 1794",
#          "-y 1999"
#         ]
# app = App()

# # Testing app
# for test in tests[:]:
#     app.handle_userinput(test)
#     print()

app = App()

while True:
    app.handle_userinput(input("\nEnter: "))