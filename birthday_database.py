# Version: 1.1-20191102

"""
TODO:
    - Check if something can be added from pythons datetime library to improve
    functionality.

ADD:
    - Show age while showing results.
    - Error handling.

ADDED:
    - A way through which one can search with a combination of year + month +
    date.
"""


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
        """
        Input Format:
        - To add something:
        add James Anderson 1999/11/22

        - To search something:
        search name James Anderson
        search year 1999
        search month 11
        search day 22
        search date 1999/11
        search date /11/22
        search date 1999/11/22
        """

        pattern1 = (r"(add) ([A-Za-z]+\s?[A-Za-z]*\s?[A-Za-z]*) "
                    r"(\d{4}/\d{2}/\d{2})")
        pattern2 = (r"(search) (id|name|year|month|day|date) "
                    r"([A-Za-z]+\s?[A-Za-z]*\s?[A-Za-z]*|"
                    # YYYY/MM/DD       or YYYY/MM  or /MM/DD   or YYYY or D
                    r"\d{4}/\d{2}/\d{2}|\d{4}/\d{2}|/\d{2}/\d{2}|\d{2,4}|\d)")

        # print(re.match(pattern1, userinput, flags=re.IGNORECASE))
        match1 = re.match(pattern1, userinput, flags=re.IGNORECASE)
        match2 = re.match(pattern2, userinput, flags=re.IGNORECASE)

        if match1:
            # print("p1", match.groups())
            cmd, name, dob = match1.groups()
            print(f"p1 {cmd=} {name=} {dob=}")
            return cmd, name, dob
        elif match2:
            # print("p2", match.groups())
            cmd, subcmd, query = match2.groups()
            print(f"p2 {cmd=} {subcmd=} {query=}")
            return cmd, subcmd, query

    def show_result(self, subcmd, query):
        found = False
        database = self.read()
        subcmd = subcmd.lower()
        split_at = 0

        if subcmd == "date":
            date_split = query.split("/")
            if date_split[0] == "":
                split_at = 1

        for userid in database:
                name, year, month, day = database[userid]
                tags = {"id": userid, "name": name, "year": year,
                        "month": month, "day": day}
                if subcmd != "date":
                    if tags[subcmd].lower() == query.lower():
                        print(userid, name, year, month, day)
                        found = True
                elif subcmd == "date":
                    if all(data in database[userid][1:]
                           for data in date_split[split_at:]):
                        print(userid, name, year, month, day)
                        found = True
        if not found:
            print(f"No user in database has {subcmd}: {query}")

    def handle_parsed_data(self, userinput):
        parsed_data = self.parse(userinput)
        usercmd = parsed_data[0]
        if usercmd == "add":
            cmd, name, dob = parsed_data
            print(f"Adding {name} {dob} in database.")
            userinfo = [name]
            dob_sep = dob.split("/")
            userinfo.extend(dob_sep)
            self.write(userinfo)
        elif usercmd == "search":
            cmd, subcmd, query = parsed_data
            print(f"Searching by {subcmd}: {query}")
            self.show_result(subcmd, query)

    def handle_userinput(self, userinput):
        if not userinput:
            print("Empty UserInput!")
        else:
            # print("Parsing:", userinput)
            self.handle_parsed_data(userinput)


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