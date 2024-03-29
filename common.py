def verify_file_overwrite(path):
    """Takes a filepath, checks if it exists, and asks the user if they
    want to overwrite it.

    Returns first path that doesn't exist or a path to be overwritten.
    """
    from os.path import isfile
    outpath = path
    while isfile(outpath):
        answer = raw_input('File {0} exists. Overwrite [Y/N]? '.format(outpath))
        if answer.lower() in ['y', 'yes']:
            break
        else:
            outpath = raw_input('Input path to new output file: ')
    return outpath

def get_files(path):
    """Return all files in given path with .partial. files last"""
    import os
    files = []
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            files.append((dirname, filename))
    # Put partial files last
    # A partial file is a file that may be missing some fields
    partials = []
    for entry in files:
        if 'partial' in entry[1]:
            idx = files.index(entry)
            partials.append(files.pop(idx))
    files.extend(partials)
    return files