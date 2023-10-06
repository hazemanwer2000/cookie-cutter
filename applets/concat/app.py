
import sys, os, subprocess
from util import *

# CMD and arguments.
cmd = "ffmpeg -f concat -safe 0 -i $$$input$$$ -c copy $$$output$$$"
args = sys.argv[1:]

# Paths.
cwd = os.getcwd()
root_dir = get_script_dir()
tmp_dir = os.path.join(root_dir, 'tmp')
concat_file = os.path.join(tmp_dir, 'concat.txt')
bat_file = os.path.join(tmp_dir, 'run.bat')
out_file = iter_name(args[0], suffix=' - Concat')

# Real paths of arguments.
for i in range(len(args)):
    if not os.path.isabs(args[i]):
        args[i] = os.path.join(cwd, args[0])

# Concat file.
txt = ''
for i in range(len(args)):
    txt += "file '" + args[i] + "'\n"
write_file(concat_file, txt)

# Batch file.
txt = ''
txt += replace_dic_into_str(cmd, {
    'input' : quote(concat_file),
    'output' : quote(out_file)    
}, '$$$') + '\n'
# txt += 'pause' + '\n'
write_file(bat_file, txt)

# Execute.
subprocess.run(bat_file)