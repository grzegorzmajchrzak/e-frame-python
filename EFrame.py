import os
import sys
import random
import Display as display


class EFrame:

    def __init__(self, path):
        self.CONFIG_FILE = os.path.dirname(os.path.realpath(sys.argv[0]))+'/already_printed.txt'

        self.path = path
        self.display = display.Display()

        if os.path.isfile(self.CONFIG_FILE):
            self.already_visited_files = set(line.strip() for line in open(self.CONFIG_FILE))
        else:
            self.already_visited_files = {}

    def do_work(self):
        if not os.path.isdir(self.path):
            print("not a directory: ", self.path)
            raise

        success = self.do_work_internal()
        if not success:
            os.remove(self.CONFIG_FILE)
            self.already_visited_files = {}
            self.do_work_internal()

    def do_work_internal(self):
        file_list = []
        for r, d, f in os.walk(self.path):
            for file in f:
                if file.lower().endswith(".jpg"):
                    file_name = os.path.join(r, file)
                    if file_name not in self.already_visited_files:
                        file_list.append(file_name)
        if len(file_list) == 0:
            return False
        random.shuffle(file_list);
        for file_name in file_list:
            if self.try_to_use(file_name):
                return True
        return False

    def try_to_use(self, fileName):
        if not self.display.show(fileName):
            return False
        self.mark_as_used(fileName)
        return True

    def mark_as_used(self, file_name):
        with open(self.CONFIG_FILE, "a") as my_file:
            my_file.write(file_name)
            my_file.write("\n")
