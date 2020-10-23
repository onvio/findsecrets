import os
import sys

if sys.version_info < (3, 0):
    sys.stdout.write("Sorry, findsecrets requires Python 3.x\n")
    sys.exit(1)

from lib.core import ArgumentParser
from lib.core import SpiderFolder
from lib.core import KeywordScanner
from lib.core import Controller


class Program(object):
    def __init__(self):

        # todo: Get Default Options / Arguments
        self.arguments = ArgumentParser().parseDefaultConfig()

        ## todo: move to Controller Class
        
        # Get filepaths
        self.filepaths = (SpiderFolder().spiderfolder(self.arguments[0]))

        for i in self.filepaths:
            print(KeywordScanner().find_keywords_with_values_in_file(i))

if __name__ == "__main__":
    main = Program()