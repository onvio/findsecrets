import re
import os
import json

class KeywordScanner():
    """
    This class is for secret scanning based on keywords / key values.
    """
    def __init__(self):

        # to-do: move Config options
        keywordsfile = 'db\\positivekeywords.txt'
        self.keywords = open(keywordsfile).read().splitlines()
        self.excluded_value_chars = ['.', '[', 'none', 'true', 'false', 'null',
        'default', 'example', 'username', 'email', 'password', 'foobar']
        self.min_value_length = 4
        self.case_sensitive = False
        self.revision_file_regex = '([a-z0-9]{40}):([^:]+):'
        assignment = "(\\b|[ ._-])({})[ '\"]*(=|:)[ '\"]*([^'\" ]+)"

        ## Regex from gitty leaks. Explained here:

        #https://regex101.com/r/Nj32DK/1
        #https://regex101.com/r/ccEuyF/1

        self.assignment_pattern = assignment.format('|'.join(self.keywords))
        return 

    def validated_value(self, v):
        if v.strip():
            if len(v) < self.min_value_length:
                return False
            if self.excluded_value_chars:
                if not self.case_sensitive:
                    v = v.lower()
                if not any([x in v for x in self.excluded_value_chars]):
                    return True
            else:
                return True
        return False

    def find_keywords_with_values_in_file(self, file):
        lines = []
        filename = str(file)
        matches = {}
        matches[filename] = []
    # Read each lines from the file remove empty lines
        for line in open(file, 'r', encoding='utf8'):
            line = line.rstrip()
            if line != '':
    # Get all match groups within line string
                m = re.findall(self.assignment_pattern, line, re.IGNORECASE)
                if m:
                    for i in m:
                        key, _, value = i[1:]
                        if self.validated_value(value):
                            key_value = key + ':' + value
                            matches[filename].append(key_value)
                            # todo add file name, line number and ref (if git)
                            # todo argument / optioon to return filepaths if no matches found
        return matches