
import os, subprocess, uuid
from pymediainfo import MediaInfo

# Data: Video file extensions.
video_exts = (
'264', '3g2', '3gp', '3gp2', '3gpp', '3gpp2', '3mm', '3p2', '60d', '787', '89', 'aaf', 'aec', 'aep', 'aepx',
'aet', 'aetx', 'ajp', 'ale', 'am', 'amc', 'amv', 'amx', 'anim', 'aqt', 'arcut', 'arf', 'asf', 'asx', 'avb',
'avc', 'avd', 'avi', 'avp', 'avs', 'avs', 'avv', 'axm', 'bdm', 'bdmv', 'bdt2', 'bdt3', 'bik', 'bin', 'bix',
'bmk', 'bnp', 'box', 'bs4', 'bsf', 'bvr', 'byu', 'camproj', 'camrec', 'camv', 'ced', 'cel', 'cine', 'cip',
'clpi', 'cmmp', 'cmmtpl', 'cmproj', 'cmrec', 'cpi', 'cst', 'cvc', 'cx3', 'd2v', 'd3v', 'dat', 'dav', 'dce',
'dck', 'dcr', 'dcr', 'ddat', 'dif', 'dir', 'divx', 'dlx', 'dmb', 'dmsd', 'dmsd3d', 'dmsm', 'dmsm3d', 'dmss',
'dmx', 'dnc', 'dpa', 'dpg', 'dream', 'dsy', 'dv', 'dv-avi', 'dv4', 'dvdmedia', 'dvr', 'dvr-ms', 'dvx', 'dxr',
'dzm', 'dzp', 'dzt', 'edl', 'evo', 'eye', 'ezt', 'f4p', 'f4v', 'fbr', 'fbr', 'fbz', 'fcp', 'fcproject',
'ffd', 'flc', 'flh', 'fli', 'flv', 'flx', 'gfp', 'gl', 'gom', 'grasp', 'gts', 'gvi', 'gvp', 'h264', 'hdmov',
'hkm', 'ifo', 'imovieproj', 'imovieproject', 'ircp', 'irf', 'ism', 'ismc', 'ismv', 'iva', 'ivf', 'ivr', 'ivs',
'izz', 'izzy', 'jss', 'jts', 'jtv', 'k3g', 'kmv', 'ktn', 'lrec', 'lsf', 'lsx', 'm15', 'm1pg', 'm1v', 'm21',
'm21', 'm2a', 'm2p', 'm2t', 'm2ts', 'm2v', 'm4e', 'm4u', 'm4v', 'm75', 'mani', 'meta', 'mgv', 'mj2', 'mjp',
'mjpg', 'mk3d', 'mkv', 'mmv', 'mnv', 'mob', 'mod', 'modd', 'moff', 'moi', 'moov', 'mov', 'movie', 'mp21',
'mp21', 'mp2v', 'mp4', 'mp4v', 'mpe', 'mpeg', 'mpeg1', 'mpeg4', 'mpf', 'mpg', 'mpg2', 'mpgindex', 'mpl',
'mpl', 'mpls', 'mpsub', 'mpv', 'mpv2', 'mqv', 'msdvd', 'mse', 'msh', 'mswmm', 'mts', 'mtv', 'mvb', 'mvc',
'mvd', 'mve', 'mvex', 'mvp', 'mvp', 'mvy', 'mxf', 'mxv', 'mys', 'ncor', 'nsv', 'nut', 'nuv', 'nvc', 'ogm',
'ogv', 'ogx', 'osp', 'otrkey', 'pac', 'par', 'pds', 'pgi', 'photoshow', 'piv', 'pjs', 'playlist', 'plproj',
'pmf', 'pmv', 'pns', 'ppj', 'prel', 'pro', 'prproj', 'prtl', 'psb', 'psh', 'pssd', 'pva', 'pvr', 'pxv',
'qt', 'qtch', 'qtindex', 'qtl', 'qtm', 'qtz', 'r3d', 'rcd', 'rcproject', 'rdb', 'rec', 'rm', 'rmd', 'rmd',
'rmp', 'rms', 'rmv', 'rmvb', 'roq', 'rp', 'rsx', 'rts', 'rts', 'rum', 'rv', 'rvid', 'rvl', 'sbk', 'sbt',
'scc', 'scm', 'scm', 'scn', 'screenflow', 'sec', 'sedprj', 'seq', 'sfd', 'sfvidcap', 'siv', 'smi', 'smi',
'smil', 'smk', 'sml', 'smv', 'spl', 'sqz', 'srt', 'ssf', 'ssm', 'stl', 'str', 'stx', 'svi', 'swf', 'swi',
'swt', 'tda3mt', 'tdx', 'thp', 'tivo', 'tix', 'tod', 'tp', 'tp0', 'tpd', 'tpr', 'trp', 'ts', 'tsp', 'ttxt',
'tvs', 'usf', 'usm', 'vc1', 'vcpf', 'vcr', 'vcv', 'vdo', 'vdr', 'vdx', 'veg','vem', 'vep', 'vf', 'vft',
'vfw', 'vfz', 'vgz', 'vid', 'video', 'viewlet', 'viv', 'vivo', 'vlab', 'vob', 'vp3', 'vp6', 'vp7', 'vpj',
'vro', 'vs4', 'vse', 'vsp', 'w32', 'wcp', 'webm', 'wlmp', 'wm', 'wmd', 'wmmp', 'wmv', 'wmx', 'wot', 'wp3',
'wpl', 'wtv', 'wve', 'wvx', 'xej', 'xel', 'xesc', 'xfl', 'xlmv', 'xmv', 'xvid', 'y4m', 'yog', 'yuv', 'zeg',
'zm1', 'zm2', 'zm3', 'zmv'
)

# API: Get text from file.
def txt_from_file(path):
    with open(path) as f:
        lines = f.read()
    return lines

# API: File exists.
def file_exists(path):
    return os.path.isfile(path)

# API: Get extension (None if doesn't exist).
def extension(path):
    ext = os.path.splitext(path)[1]
    if ext == '':
        ext = None
    else:
        ext = ext[1:]
    return ext

# API: Check if file is video (Checks extension only).
def is_video(path):
    return extension(path) in video_exts

# API: Check if file is video and exists.
def video_exists(path):
    return file_exists(path) and is_video(path)

# API: Convert milliseconds to format (e.g: 0:00:00.000)
def ms_to_format(value, ms=True):
    if value < 0:
        return '#error'

    txt_ms = str(value % 1000).zfill(3)
    value = value // 1000                  # Note: Remove milli-seconds
    txt_s = str(value % 60).zfill(2)
    value = value // 60                    # Note: Remove seconds.
    txt_m = str(value % 60).zfill(2)
    value = value // 60                    # Note: Remove minutes.
    txt_h = str(value).zfill(2)

    txt = txt_h + ':' + txt_m + ':' + txt_s
    if ms:
        txt = txt + '.' + txt_ms
    return txt

# API: Get script's containing directory.
def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))

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

# API: Run batch sequence in new shell (non-blocking).
def run_batch(cmds, path, pause=True):
    if pause:
        cmds.append('pause')
    with open(path, 'w') as f:
        for cmd in cmds:
            f.write(cmd)
            f.write('\n')
            
    subprocess.Popen('"' + path + '"')

# API: Generate random string.
def rand_str():
    return str(uuid.uuid4())

# API: Get video length (in ms)
def video_length(f):
    info = MediaInfo.parse(f)
    return info.tracks[0].duration

# API: Check if video has audio stream.
def has_audio(f):
    info = MediaInfo.parse(f)
    return any([track.track_type == 'Audio' for track in info.tracks])

# API: Check if video has audio stream.
def video_dimensions(f):
    info = MediaInfo.parse(f)
    track = [track for track in info.tracks if track.track_type == 'Video'][0]
    return (track.width, track.height)

# API: Check if video has audio stream.
def get_fps(f):
    info = MediaInfo.parse(f)
    track = [track for track in info.tracks if track.track_type == 'Video'][0]
    return track.frame_rate

if __name__ == '__main__':
    print(video_dimensions("C:/Users/hazem/Desktop/21-jump.mp4"))