import os

def print_warning(message, category=UserWarning):  # , filename='', lineno=-1):
    """Prettier printing of warning messages.
    Inputs
    ------
    - message (str):
        the warning message to be displayed
    - category:
        the warning category associated to the message.
        Default value:
            UserWarning
        Examples:
            UserWarning, SyntaxWarning, etc.
    """
    print ' %s: %s' % (category.__name__, message)


def create_folder(folder_name, path, sub_folders=None):
    """Creates a folder inside the specified location. Also subfolders can be
    specified.
    
    Inputs
    ------
    - folder_name (str):
        the name of the folder to be created.
    - path (str):
        the path to the location where the folder has to be created.
    - sub_folders (list):
        a list containing all the subfolders to be created inside the main
        folder (folder_name). If sub-sub-folders has to be created the
        complete path has to be specified.
        Examples: supposing the main folder is 'Root' and the subfolders are 'Sub_1'
        and 'Sub_2', and that the location of the folder 'Root' has to be
        'C:/temp' we have:
            create_folder('Root', 'C:/temp', ['Sub_1', 'Sub_2'])

        in case the sub-folders have sub-sub-folders we would have:
            create_folder('Root', 'C:/temp', ['Sub_1/Sub_Sub_1',
                                              'Sub_1/Sub_Sub_2'
                                              'Sub_2/Sub_Sub_1'])

        in this case the sub-folder Sub_1 has two sub-sub-folders
        'Sub_Sub_1' and 'Sub_Sub_2', whereas 'Sub_2' has one
        'Sub_Sub_1'.
    
    Returns
    -------
    - 0:
        returns 0 when the folder did not exist before.
    - 1:
        returns 1 if the folder already existed.
    Note: this is used later 
    """
    try:
        try:
            for sub_folder in sub_folders:
                os.makedirs('/'.join([path, folder_name, sub_folder]))
        except TypeError:
            os.makedirs('/'.join([path, folder_name]))
        return True
    except OSError:
        print '/'.join([path, folder_name])
        if os.path.isdir('/'.join([path, folder_name])):
            print_warning("The folder already exists! The simulation will " +
                          "overwrite the previous results.\n")
        cont = raw_input("Do you want to continue? yes/no > ")
        while cont.lower() not in ("yes", "no"):
            cont = raw_input("Do you want to continue? yes/no > ")
        if cont == "no":
            return False
        else:
            return True