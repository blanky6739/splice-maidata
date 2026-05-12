import re
import test_file

difficulties = (None, "easy", "basic", "advanced",
                "expert", "master", "remaster", "utage")


class maidata():
    def __init__(self, simai_dict):
        self.header = {}
        self.charts = {}
        for var, value in simai_dict.items():
            if (num := re.search(r'(\d+)$', var)) is not None:
                if int(num.group()) not in self.charts:
                    self.charts[int(num.group())] = {}
                self.charts[int(num.group())][var] = value
            else:
                self.header[var] = value

        remove = []
        for level, info in self.charts.items():
            if f"inote_{level}" not in info:
                remove.append(level)

        for level in remove:
            del self.charts[level]

    @classmethod
    def from_file(cls, file):
        file = file.strip("'")
        with open(file, "r") as f:
            return cls.from_binary(f.read())

    @classmethod
    def from_binary(cls, binary):
        binary = [x.split("=") for x in binary.split("&") if x != ""]
        return cls({k: v.rstrip("\n") for k, v in binary})

    @property
    def utage_count(self):
        return sum(x == 7 or x >= 15 for x in self.charts)

    def remove_diff(self, diff):
        self.charts.pop(difficulties.index(diff))

    def update(self, other):
        self.header.update(other.header)
        for level, info in other.charts.items():
            self.charts[level] = info

    def update_multiple(self, others):
        self.header.pop("shortid")
        self.header.pop("cabinet")
        self.header.pop("version")

        utage_count = 0
        for other in others:
            for other in others:
                utage_count += sum(x.utage_count for x in other.charts)
        # if utage count > 1, put them all in 15:22
        for other in others:
            self.header.update(other.header)
            # check which values should be ignored or deleted
            # get longest equivalent string for each title
            for level, info in other.charts.items():
                # if other is an utage and utage count == 1, put it in the utage slot else 15:22
                # set difficulty to its special name for multiplayer and same name utage versions
                # otherwise, put it in index 8:15 by adding 7
                # change song diff to incl std or dx version
                pass


file = test_file.files[0]
maidata.from_file(file)
