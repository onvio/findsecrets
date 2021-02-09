import os
import sys
import re
import os
import jellyfish
from yaml import safe_load
from pathlib import Path

if sys.version_info < (3, 0):
    sys.stdout.write("Sorry, findsecrets requires Python 3.x\n")
    sys.exit(1)

## Load Configs
def yamlconfig(configyml = Path('config.yml')):
    yamldict = safe_load(configyml.read_text())
    if not isinstance(yamldict, dict):
        return {}
    return yamldict

config = yamlconfig()
scanfolder = config['scanfolder'][0]
keywordsdb = 'db/positivekeywords.txt'

def validated_secret_value(key, value):
    excluded_value_chars_lowercase = [each_string.lower() for each_string in config['exclude']['values']]

    ## Checks for values
    if len(value) < config['settings'][2]['min-value-length']:
        return False
    if any([x in value.lower() for x in excluded_value_chars_lowercase]):
        return False
    if key.lower() in value.lower():
        return False

    ## Check if key string somewhat compares with value string using levenhstein distance
    ## https://jellyfish.readthedocs.io/en/latest/comparison.html#levenshtein-distance

    if jellyfish.levenshtein_distance(key, value) <= config['settings'][0]['levenshtein-distance']:
        return False

    ## Check if special value contains alphanumeric 8-70 string with specialchars
    if key.lower() == 'token' or key.lower() == 'password' or key.lower() == 'value':
        regexp = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,100}')
        if regexp.search(value): 
            return True
        else:
            return False
    return True

def spiderfolder(scanfolder):

    filepaths = []
    for root, dirs, files in os.walk(scanfolder, topdown=True):
        ## Exclude Dirs
        dirs[:] = [d for d in dirs if d not in config['exclude']['folders']]
        ## Exclude Extentions
        files = [ file for file in files if not file.endswith( tuple(config['exclude']['extentions']) ) ]
        ## Exclude Filenames
        files = [ file for file in files if not file.endswith( tuple(config['exclude']['files']) ) ]
        ## Exclude Large Filesizes
        for i in files:
            filesize = "%.0f" % (os.path.getsize(os.path.join(root, i)) / 1024)
            if int(filesize) <= int(config['settings'][1]['max-filesize-kb']):
                filepaths.append(os.path.join(root, i))
    return filepaths

def find_keywords_with_values_in_file(file):
        assignment = "(\\b|[ ._-])({})[ '\"]*(=>|=|:)[ '\"]*([^'\" ]+)"
        keywords = open(keywordsdb).read().splitlines()
    
        # alternative assignment = "(\b{})(=>|:|=)(.*)"
        assignment_pattern = assignment.format('|'.join(keywords))
        # assignment pattern example https://regex101.com/r/DzO3jR/1

        filename = str(file)
        matchesdict = {}
        matchesdict[filename] = []
        try:
            file = open(file, 'r', encoding='utf8')
        except:
            pass

        # Read each lines from the file & remove empty lines
        try:
            for line in file:
                line = line.strip()
                if line != '':
            # Get all match groups within line string
                    matches = re.findall(assignment_pattern, line, re.IGNORECASE)
                    if matches:
                        for i in matches:
                            key, _, value = i[1:]
                            if validated_secret_value(key, value):
                                key_value = key + ':' + value
                                matchesdict[filename].append(key_value)
                    # print(f"file read error: {file}")
        except:
            pass
        for key, value in matchesdict.items():
            if len(value) != 0 or None:
                print(key, value)

filepaths = spiderfolder(scanfolder)

for scannedfile in filepaths:
    find_keywords_with_values_in_file(scannedfile)