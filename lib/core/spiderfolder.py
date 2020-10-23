import os

class SpiderFolder():
    """
    This class is used to recursively walk trough a directory and return filepaths.
    """
    def __init__(self):
        return

    def spiderfolder(self, folder):

        ## todo: Make this configurable and set default values
        
        recursion_level = 1
        excluded_folders = ['vendor']
        excluded_files = ['vendor']
        excluded_files_extentions = ['vendor']
        filepaths = []

        ## todo: Multi Threading 
        ## todo: Spider SMB Share
        ## todo: Do not spider exclusions 

        for root, dirs, files in os.walk(folder, topdown=True):
            dirs[:] = [d for d in dirs if d not in excluded_folders]
            for i in files:
                filepaths.append(os.path.join(root, i))
        return filepaths