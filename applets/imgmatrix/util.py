
import os, sys

# API: Alter name of file.
def alter_name(f, ext=None, suffix=''):
    name, orig_ext = os.path.splitext(f)
    name += suffix
    name += ('.' + ext) if ext != None else orig_ext
    return name

# API: Create an enumarated (non-existing) file-name.
def iter_name(f, ext=None, suffix=''):
    i = 1

    while True:
        iter_suffix = suffix + ' (' + str(i) + ')'
        name = alter_name(f, ext, iter_suffix)
        
        if not os.path.exists(name):
            break
        
        i += 1

    return name