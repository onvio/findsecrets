from optparse import OptionParser, OptionGroup
from lib.utils.default_config_parser import DefaultConfigParser

class ArgumentParser(object):
    """
    Get and set all default options if there are any 
    Overwite default options with arguments given 
    Return a dict/array for the Controller Class
    """
    def __init__(self):
        self.parseDefaultConfig() 

    def parseDefaultConfig(self):
        options = []
        config = DefaultConfigParser()
        configPath = "default.conf"
        config.read(configPath)

        # Get/Set Default Options from Config Values
        options.append(config.safe_get("general", "spiderfolder", None))

        # todo: return key/value array instead of only value
        return options

        # todo: Overwrite default values with arguments (if there are any)
    def parseArguments(self):
        usage = "Usage: testingzzz"
        parser = OptionParser(usage, epilog='''testzzzz.''')

        # Spiderfolder Arguments
        spiderfolder = OptionGroup(parser, 'spiderfolder Settings')
        spiderfolder.add_option('--sf', '--spiderfolder', action='store', dest='wordlist',
                              help='Folder to spider',
                              default='samples')

        ## from reposcanner
        # parser.add_argument('-r', '--repo', help='Repo to scan', dest='repo', required=True)
        # parser.add_argument('-c', '--count', help='Number of commits to scan (default all)', dest='count', default=sys.maxsize, type=int)
        # parser.add_argument('-e', '--entropy', help='Minimum entropy to report (default 4.3)', dest='entropy', default=4.3, type=float)
        # parser.add_argument('-l', '--length', help='Maxmimum line length (default 500)', dest='length', default=500, type=int)
        # parser.add_argument('-b', '--branch', help='Branch to scan', dest='branch' )
        # parser.add_argument('-v', '--verbose', help='Verbose output', dest='verbose', action='store_true', default=False)
        # args = parser.parse_args()


        ## From GittyLeaks
        # p = argparse.ArgumentParser(
        #     description='Discover where your sensitive data has been leaked.')
        # p.add_argument('-user', '-u',
        #             help='Provide a github username, only if also -repo')
        # p.add_argument('-repo', '-r',
        #             help='Provide a github repo, only if also -user')
        # p.add_argument('-link', '-l',
        #             help='Provide a link to clone')
        # p.add_argument('-delete', '-d', action='store_true',
        #             help='If cloned, remove the repo afterwards.')
        # p.add_argument('--find-anything', '-a', action='store_true',
        #             help='flag: If you want to find anything remotely suspicious.')
        # p.add_argument('--search-only-head', '-o', action='store_true',
        #             help='If flag given, only search HEAD not all commit history.')
        # p.add_argument('--case-sensitive', '-c', action='store_true',
        #             help='flag: If you want to be specific about case matching.')
        # p.add_argument('--excluding', '-e', nargs='+',
        #             help='List of words that are ignored occurring as value.')
        # p.add_argument('--verbose', '-v', action='store_true',
        #             help='If flag given, print verbose matches.')
        # p.add_argument('--no-banner', '-b', action='store_true',
        #             help='Omit the banner at the start of a print statement')
        # p.add_argument('--no-fancy-color', '-f', action='store_true',
        #             help='Do not colorize output')

        parser.add_option_group(spiderfolder)
        options, arguments = parser.parse_args()
        return options
