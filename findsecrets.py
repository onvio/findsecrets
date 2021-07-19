import os
import sys
import re
import os
import jellyfish
from yaml import safe_load
from pathlib import Path
import argparse
import json
import shutil
import os

if sys.version_info < (3, 0):
    sys.stdout.write("Sorry, findsecrets requires Python 3.x\n")
    sys.exit(1)

parser = argparse.ArgumentParser('findsecrets.py', formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=40))
parser.add_argument('-f', '--folder', help='Source folder to scan', dest='folder', required=False)
parser.add_argument('-e', '--exclude', help='Comma separated list of files to exclude', dest='exclude', required=False)
parser.add_argument('-m', '--mask', help='Mask Secret Values', dest='mask', action='store_true', default=False)
parser.add_argument('-v', '--verbose', help='Verbose output in stdout', dest='verbose', action='store_true', default=False)
parser.add_argument('-r', '--reportpath', help='If specified, copy reports to specified folder', dest='reportpath', required=False)
args = parser.parse_args()

# Load Configs
def yamlconfig(configyml=Path('config.yml')):
    yamldict = safe_load(configyml.read_text())
    if not isinstance(yamldict, dict):
        return dict()

    if args.exclude:
        exclude_files = map(str.strip, args.exclude.split(','))
        for file in exclude_files:
            yamldict['exclude']['files'].append(file)

    return yamldict

config = yamlconfig()

if args.folder is not None:
    scanfolder = args.folder
else:
    try:
        scanfolder = config['scanfolder'][0]
    except:
        print("Findsecrets failed... Scanfolder not specified")
        parser.print_help()
        sys.exit(1)

keywordsdb = 'db/positivekeywords.txt'
foundsecrets = dict()


def validated_secret_value(key, value):
    excl_values_lcase = [i.lower() for i in config['exclude']['values']]

    # Checks values for potential ENV variables / False positives
    if len(value) < config['settings'][2]['min-value-length']:
        return False
    if any([x in value for x in excl_values_lcase]):
        return False
    if key in value:
        return False
    if value.endswith('}') or value.endswith(')') or value.endswith(';'):
        return False

    # Check if key somewhat compares value string using levenhstein distance
    # https://jellyfish.readthedocs.io/en/latest/comparison.html#levenshtein-distance

    ldistance = config['settings'][0]['levenshtein-distance']
    if jellyfish.levenshtein_distance(key, value) <= ldistance:
        return False

    # Extra checks within sensitive values
    if key in config['sensitivevalues']['sensitivevalues']:
        if 'http' or 'https' in value:
            return False
        regexp2 = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,100}"
        # https://regex101.com/r/v1qv1E/1
        if re.findall(regexp2, value, re.IGNORECASE):
            return True
        else:
            return False
    return True


def spiderfolder(scanfolder):
    try:
        len(os.listdir(scanfolder)) == 0
    except:
        print(f"{scanfolder} Directory not found or is empty")
        sys.exit(1)

    print(f'\nFindsecrets Running \nSpidering folder: {scanfolder}\n')
    filepaths = list()
    for root, dirs, files in os.walk(scanfolder, topdown=True):
        # Exclude Dirs
        dirs[:] = [d for d in dirs if d not in config['exclude']['folders']]
        # Exclude Extentions
        files = [file for file in files if not file.endswith(tuple(config['exclude']['extentions']))]
        # Exclude Filenames
        files = [file for file in files if not file.endswith(tuple(config['exclude']['files']))]
        # Exclude Large Filesizes
        for i in files:
            filesize = "%.0f" % (os.path.getsize(os.path.join(root, i)) / 1024)
            if int(filesize) <= int(config['settings'][1]['max-filesize-kb']):
                filepaths.append(os.path.join(root, i))
    print(f'{len(filepaths)} files will be scanned for secrets\n')
    return filepaths


def find_keywords_with_values_in_file(file):
    assignment = "(\\b|[ ._-])({})[ '\"]*(=>|=|:)[ '\"]*([^'\" ]+)"
    keywords = open(keywordsdb).read().splitlines()

    # alternative assignment = "(\b{})(=>|:|=)(.*)"
    assignment_pattern = assignment.format('|'.join(keywords))
    # assignment pattern example https://regex101.com/r/DzO3jR/1

    filename = str(file)
    matchesdict = dict()
    matchesdict[filename] = list()
    try:
        file = open(file, 'r', encoding='utf8')
    except:
        pass
    try:
        for line in file:
            line = line.strip()
            if line != '':
                matches = re.findall(assignment_pattern, line, re.IGNORECASE)
                if matches:
                    for i in matches:
                        key, _, value = i[1:]
                        if validated_secret_value(key.lower(), value.lower()):
                            if args.mask:
                                value = value[4:].rjust(len(value), "*")
                                value = value[:-4].ljust(len(value), "*")
                            key_value = key + ':' + value
                            matchesdict[filename].append(key_value)
    except:
        pass
    for file, secret in matchesdict.items():
        if len(secret) != 0 or None:
            foundsecrets.update({file: secret})
            if args.verbose:
                print(matchesdict)


def jsonreport(foundsecrets):
    jsonreport = 'report.json'
    jsonobject = {"vulnerabilities": []}

    for file, secrets in foundsecrets.items():
        with open(jsonreport, 'w'):
            secretsdb = {
                "File": file,
                "Secrets": secrets,
                "Severity": "High"
            }
            jsonobject['vulnerabilities'].append(secretsdb)

    with open(jsonreport, 'w') as f:
        json.dump(jsonobject, f, indent=4)


def seqhubreport(foundsecrets):
    seqhubreport = 'seqhubreport.json'
    jsonobject = {"vulnerabilities": []}

    for file, secrets in foundsecrets.items():
        if len(secrets) > 1:
            secrets = str(''.join('%s ' % secrets for secrets in secrets))
        else:
            secrets = secrets[0]
        with open(seqhubreport, 'w'):
            secretsdb = {
                "title": "Secret Found",
                "description": f"{file} contains: {secrets}",
                "severity": "High"
            }
            jsonobject['vulnerabilities'].append(secretsdb)

    with open(seqhubreport, 'w') as f:
        json.dump(jsonobject, f, indent=4)


def move_reports():
    reports = ['seqhubreport.json', 'report.json']
    for report in reports:
        shutil.move(os.path.join(os.getcwd(), report), os.path.join(args.reportpath, report))


filepaths = spiderfolder(scanfolder)
for scannedfile in filepaths:
    find_keywords_with_values_in_file(scannedfile)

jsonreport(foundsecrets)
seqhubreport(foundsecrets)

if args.reportpath:
    move_reports()
