# Version: 1.2-20191106

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
from http import client


class Database:
    """Contains methods to read and write from database."""

    def __init__(self):
        self.host = "www.jsonblob.com"
        self.source = "/api/jsonBlob/7ce393ec-069e-11ea-b8b2-c9f8c41f7504"

    def read(self):
        """Reads data from database."""
        try:
            conn = client.HTTPSConnection(self.host)
            conn.request("GET", self.source)
            return json.load(conn.getresponse())
        except json.decoder.JSONDecodeError as database_error:
            print("Unable to load database!")
            quit()

    def write(self, data):
        """Writes data to database."""
        database = self.read()
        userid = len(database) + 1
        newdata = {userid: data}
        database.update(newdata)
        print(f"{newdata=}")

        conn = client.HTTPSConnection(self.host)
        conn.request("PUT", self.source, json.dumps(database))

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
        match1 = re.match(pattern1, userinput)
        match2 = re.match(pattern2, userinput)

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
                    if tags[subcmd] == query:
                        print(userid, name, year, month, day)
                        found = True
                elif subcmd == "date":
                    if all(data in database[userid][1:]
                           for data in date_split[split_at:]):
                        print(userid, name, year, month, day)
                        found = True
        if not found:
            print(f"No user in database has {subcmd}: {query}")

    def handle_and_parse(self, userinput):
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
        elif userinput:
            userinput_split = userinput.split()
            print(userinput_split)
            cmd = userinput_split[0]
            if cmd not in ("add", "search"):
                print(f"Command: '{cmd}' is invalid! Enter either 'add' or "
                      "'search'.")
            elif cmd == "add" and len(userinput_split) == 1:
                print("Input Format:-\nTo add something:\nadd James Anderson "
                      "1999/11/22")
            elif cmd == "add" and len(userinput_split) > 1:
                name = userinput_split[1]
                # print(re.match(r"\d+|\w+\d+|\d+\w+", name))
                incorrect_name = re.match(r"\d+|\w+\d+|\d+\w+", name)
                correct_date = re.match(r"add [A-Za-z]+\s?[A-Za-z]*\s?" +
                                        r"[A-Za-z]* " +
                                        r"\d{4}/\d{2}/\d{2}", userinput)
                if incorrect_name:
                    print("Name can't contain digits.")
                elif not correct_date:
                    print("Date format is not correct.")
                elif correct_date:
                    # Check year month and day
                    year, month, day = correct_date.split("/")
                    if int(year) > 9999:
                        print("Year can't be greater than 9999!")
                    elif int(month) > 12:
                        print("Month can't be greater than 12!")
                    elif int(day) > 31:
                        print("Day can't be greater than 31!")
                else:
                    # print("Parsing:", userinput)
                    self.handle_and_parse(userinput)
            elif cmd == "search" and len(userinput_split) == 1:
                print("Input Format:-\n- To search something:\n"
                      "search id 3\n"
                      "search name James Anderson\n"
                      "search year 1999\n"
                      "search month 11\n"
                      "search day 22\n"
                      "search date 1999/11\n"
                      "search date /11/22\n"
                      "search date 1999/11/22")
            elif cmd == "search" and len(userinput_split) > 1:
                subcmd = userinput_split[1]
                if subcmd not in ("id", "name", "year", "month", "day", "date"):
                    print(f"Command: search {subcmd} is not valid! "
                          f"Enter: search name/year/month/day/date (any one)")
                else:
                    self.handle_and_parse(userinput)








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