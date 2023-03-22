
import os, sys

# API: Get script's containing directory.
def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))

# API: Quote.
def quote(s):
    return '"' + s + '"'

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

# API: Replace dictionary into a string.
def replace_dic_into_str(cpy, dic, ch):
    for key in dic.keys():
        cpy = cpy.replace(ch + key + ch, dic[key])
    return cpy

# API: Write to file.
def write_file(filename, txt):
    with open(filename, 'w') as f:
        f.write(txt)
