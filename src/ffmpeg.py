
from util import ms_to_format, rand_str
from collections import OrderedDict
from cc_assets import assets
from cc_constants import constants
from util_qt import asset_path
from util import extension, video_length, iter_name, get_fps, video_dimensions
from pprint import pprint

import os

# Variable: Temporary directory.
tmp_dir = asset_path(assets["tmp-dir"])

# Variable: Concat file path.
concat_file = os.path.join(tmp_dir, 'concat.txt')

# Variable: Template commands in dictionary.
templates_dict = {
    "keyframes" : OrderedDict([
        ('0', "ffprobe -skip_frame nokey -select_streams v:0 -show_entries frame=pkt_pts_time -of csv=print_section=0 $$$input$$$")
    ]),
    "check-audio" : OrderedDict([
        ('0', "ffprobe -i $$$input$$$ -show_streams -select_streams a -loglevel error")
    ]),
    "get-length" : OrderedDict([
        ('0', "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $$$input$$$")
    ]),
    "video-quick" : OrderedDict([
        ('0', "ffmpeg -hide_banner -loglevel info -noaccurate_seek"),
        ("start", "-ss $$$start$$$"),
        ("1", "-i $$$input$$$ -vcodec copy -acodec copy"),
        ("length", "-to $$$length$$$"),
        ("2", "-avoid_negative_ts make_zero $$$output$$$")
    ]),
    "video-encode" : OrderedDict([
        ('0', "ffmpeg -hide_banner -loglevel info"),
        ("start", "-ss $$$start$$$"),
        ("1", "-i $$$input$$$ -crf $$$crf$$$"),
        ("length", "-to $$$length$$$"),
        ("2", "$$$output$$$")
    ]),
    "concat" : OrderedDict([
        ('0', "ffmpeg -hide_banner -loglevel info -f concat -safe 0 -i $$$input$$$ -c copy $$$output$$$")
    ]),
    "mute" : OrderedDict([
        ('0', "ffmpeg -hide_banner -loglevel info -i $$$input$$$ -c copy -an $$$output$$$")
    ]),
    "filter" : OrderedDict([
        ('0', "ffmpeg -hide_banner -loglevel info -i $$$input$$$ -crf $$$crf$$$"),
        ('vf', "-vf $$$vf$$$"),
        ('af', "-af $$$af$$$"),
        ('1', "$$$output$$$")
    ]),
    "vf" : OrderedDict([
        ('fade', 'fade=t=in:st=0:d=$$$fade-length$$$,fade=t=out:st=$$$fade-offset$$$:d=$$$fade-length$$$'),
        ('crop', 'crop=$$$crop-width$$$:$$$crop-height$$$:$$$crop-x$$$:$$$crop-y$$$')
    ]),
    "af" : OrderedDict([
        ('afade', 'afade=t=in:st=0:d=$$$fade-length$$$,afade=t=out:st=$$$fade-offset$$$:d=$$$fade-length$$$')
    ]),
    "gif" : OrderedDict([
        ('0', "ffmpeg -hide_banner -loglevel info -i $$$input$$$ -vf fps=$$$fps$$$,scale=$$$width$$$:$$$height$$$:flags=lanczos,setpts=$$$playback$$$*PTS[v] -loop 0 $$$output$$$")
    ])
}

# API: Estimate video length.
def estimate_length(summary):
    in_length = video_length(summary['Path'])
    ms = 0

    for time in summary['Times']:
        if time[0] < 0 and time[1] < 0:
            ms += in_length
        elif time[0] < 0:
            ms += time[1]
        elif time[1] < 0:
            ms += (in_length - time[0])
        else:
            ms += (time[1] - time[0])

    return ms

# API: Replace into command.
def replace_into_cmd(cpy, dic):
    for key in dic.keys():
        cpy = cpy.replace("$$$" + key + "$$$", dic[key])
    return cpy

# API: Create command.
def create_cmd(name, to_replace=None, to_delete=None, sep=" "):
    # Note: Command dictionary.
    cmd_dic = templates_dict[name].copy()

    # Note: Remove unnecessary options.
    if to_delete != None:
        for name in to_delete:
            if cmd_dic.get(name) != None:
                cmd_dic.pop(name)

    # Note: Command string.
    cmd = sep.join(cmd_dic.values())

    # Note: Replace arguments.
    if to_replace != None:
        cmd = replace_into_cmd(cmd, to_replace)
    
    return cmd

# Function: Quote.
def quote(s):
    return '"' + s + '"'

# Function: Make any file argument.
def file_arg(ext, path=None, name=None):
    if name == None:
        name = rand_str()

    file_name = name + '.' + ext

    if path == None:
        path = tmp_dir
    
    file_name = os.path.join(path, file_name)

    return file_name

# Function: Generate trimming commands.
def cmd_trim(summary, cmds):
    to_replace = {"input" : quote(summary["Path"])}

    # Note: Accurate (encode) or quick (at keyframes).
    if summary["Type"] == 'Video' and summary["Re-encode"] == 'No':
        cmd_name = "video-quick"
        ext = extension(summary["Path"])
    else:
        cmd_name = "video-encode"
        ext = summary['Extension'] if summary.get('Extension') != None else constants["ffmpeg"]["def-ext"]
        to_replace["crf"] = summary["CRF"] if summary.get('CRF') != None else constants["ffmpeg"]["def-crf"]

    out_files = []

    # Note: Tuning start times when cutting at keyframes.
    if cmd_name == 'video-encode':
        times = summary['Times']
        for i in range(len(times)):
            times[i][0] += constants["ffmpeg"]["tune-keyframe-start"]

    # Note: For each time bound.
    for time in summary["Times"]:
        to_del = []

        if time[0] == -1 and time[1] == -1:
            out_files.append(summary["Path"])
        else:
            if time[0] == -1:
                to_del.append('start')
            elif time[1] == -1:
                to_del.append('length')

            out_files.append(file_arg(ext))
            to_replace["output"] = quote(out_files[-1])
            
            to_replace["start"] = ms_to_format(time[0])
            to_replace["length"] = ms_to_format(time[1] - time[0])

            cmds.append(create_cmd(cmd_name, to_replace, to_del))

    return out_files

# Function: Generate concatenate comamnd.
def cmd_concat(cmds, in_files):
    txt = ''
    
    if len(in_files) > 1:
        out_file = file_arg(extension(in_files[0]))

        # Note: Creating 'concat.txt' file.
        for i in range(len(in_files)):
            txt += "file '" + in_files[i] + "'\n"
        with open(concat_file, 'w') as f:
            f.write(txt)

        # Note: Create 'concat' command.
        cmds.append(create_cmd('concat', to_replace={
            'input' : quote(concat_file),
            "output" : quote(out_file)                     
        }))
    else:
        out_file = in_files[0]

    return out_file

# Function: Generate a simplistic relay command.
def cmd_relay(name, cmds, in_file):
    out_file = file_arg(extension(in_file))
    cmds.append(create_cmd(name, {
        "input" : quote(in_file),
        "output" : quote(out_file)
    }))
    return out_file

# Function: Generate mute command.
def cmd_mute(summary, cmds, in_file):
    if summary["Type"] == 'Video' and summary["Mute"] == "Yes":
        out_file = cmd_relay('mute', cmds, in_file)
    else:
        out_file = in_file
    return out_file

# Function: Generate filter command.
def cmd_filter(summary, cmds, in_file):
    to_del_filters = []

    # Note: Check whether to apply 'fade' filter.
    if summary['Fade'] == '0':
        to_del_filters += ['fade', 'afade']

    # Note: Check whether to apply 'crop' filter.
    if summary['Crop (W)'] == '100' and summary['Crop (H)'] == '100':
        to_del_filters += ['crop']

    # Note: Get video dimensions.
    vid_dim = video_dimensions(summary['Path'])

    # Note: To-replace filters.
    to_replace_filters = {
        'fade-length' : summary['Fade'],
        'fade-offset' : str(((estimate_length(summary) + constants["ffmpeg"]["tune-fade-offset"]) / 1000) - float(summary['Fade'])),
        'crop-width' : str(int((float(summary['Crop (W)']) / 100) * float(vid_dim[0]))),
        'crop-height' : str(int((float(summary['Crop (H)']) / 100) * float(vid_dim[1]))),
        'crop-x' : str(int((float(summary['Crop (X)']) / 100) * float(vid_dim[0]))),
        'crop-y' : str(int((float(summary['Crop (Y)']) / 100) * float(vid_dim[1]))),
    }

    # Note: Create filters.
    vf = create_cmd('vf', to_replace_filters, to_del_filters, sep=',')
    af = create_cmd('af', to_replace_filters, to_del_filters, sep=',')

    # Note: Delete options.
    to_del = []
    if (vf == ''):
        to_del.append('vf')
    if (af == ''):
        to_del.append('af')

    # Note: Check if any filters have been applied.
    if vf != '' or af != '':
        out_file = file_arg(extension(in_file))
        to_replace = {
            'input' : quote(in_file),
            'output' : quote(out_file),
            'crf' : summary["CRF"] if summary.get('CRF') != None else constants["ffmpeg"]["def-crf"],
            'vf' : vf,
            'af' : af
        }
        cmds.append(create_cmd('filter', to_replace, to_del))
    else:
        out_file = in_file

    return out_file

# Function: Generate GIF command.
def cmd_gif(summary, cmds, in_file):
    to_replace = {}

    if summary['Type'] == 'GIF':
        out_file = file_arg('gif')

        to_replace['fps'] = str(min(float(summary['FPS']), float(get_fps(summary['Path']))))
        to_replace['playback'] = str(1 / float(summary['Playback']))
        to_replace['width'] = '-1' if summary.get('Width') == None else summary['Width']
        to_replace['height'] = '-1' if summary.get('Height') == None else summary['Height']

        to_replace['input'] = quote(in_file)
        to_replace['output'] = quote(out_file)
        
        cmds.append(create_cmd('gif', to_replace))
    else:
        out_file = in_file

    return out_file

# Function: Finalize (with a 'cp' command).
def finalize(summary, cmds, in_file):
    out_file = iter_name(summary['Path'], ext=extension(in_file), suffix=' - Cookie')
    cmds.append(constants['cmd']['copy'] + ' ' + quote(in_file) + ' ' + quote(out_file))

# Function: Set default options.
def default_opts(summary):
    if summary.get('Extension') == '':
        summary['Extension'] = constants["ffmpeg"]["def-ext"]

    if summary.get('CRF') == '':
        summary['CRF'] = constants["ffmpeg"]["def-crf"]
    
    if summary.get('Fade') == '':
        summary['Fade'] = constants["ffmpeg"]["def-fade"]

    if summary.get('FPS') == '':
        summary['FPS'] = get_fps(summary['Path'])

    if summary.get('Playback') == '':
        summary['Playback'] = constants["ffmpeg"]["def-playback"]

    if summary.get('Width') == '' or summary.get('Height') == '':
        summary['Width'] = constants["ffmpeg"]["def-width"]
        summary['Height'] = None

    if summary.get('Crop (W)') == '':
        summary['Crop (W)'] = '100'

    if summary.get('Crop (H)') == '':
        summary['Crop (H)'] = '100'

    if summary.get('Crop (X)') == '':
        summary['Crop (X)'] = '0'

    if summary.get('Crop (Y)') == '':
        summary['Crop (Y)'] = '0'

# API: Empty temporary directory.
def clean_tmp_dir():
    for f in os.listdir(tmp_dir):
        del_f = os.path.join(tmp_dir, f)
        os.remove(del_f)

# API: Options to commands.
def options_to_cmds(summary):
    cmds = []

    clean_tmp_dir()

    default_opts(summary)

    f = cmd_trim(summary, cmds)
    print('\n\nTrim: ')
    pprint(f)
    f = cmd_concat(cmds, f)
    print('\n\nConcat: ')
    pprint(f)
    f = cmd_filter(summary, cmds, f)
    print('\n\nFilter: ')
    pprint(f)
    f = cmd_mute(summary, cmds, f)
    print('\n\nMute: ')
    pprint(f)
    f = cmd_gif(summary, cmds, f)
    print('\n\nGIF: ')
    pprint(f)

    finalize(summary, cmds, f)

    print('\n\nCMD: ')
    pprint(cmds)

    # for i in range(len(cmds)):
    #     cmds[i] = "echo " + cmds[i]

    return cmds

if __name__ == "__main__":
    summary = {'Type': 'GIF', 'Height' : '345', 'FPS' : '20', 'Playback' : '1.2', 'Fade': '1', 'Times': [[0, 10555], [0, 3000]], 'Path': 'C:/Users/hazem/Desktop/cure-for-wellness.mkv'}
    options_to_cmds(summary)