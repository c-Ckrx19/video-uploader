from decouple import config
from tkinter import Tk, messagebox
from file_selection_dialog import FileSelectionDialog
from video_downloading import VideoDownload
from video_splitter import VideoSplitter
from ftp_uploader import FTPUploader
import os
import re
import multiprocessing


FTP_USERNAME = config('FTP_USERNAME')
FTP_PASSWORD = config('FTP_PASSWORD')
video_name_list = []
video_id = dict()  # {show_name: tvid}
parent_dir = ''


def select_download():
    global video_name_list
    global video_id
    global parent_dir
    #################
    # File selection
    #################
    root = Tk()
    root.geometry("370x180")
    file_selection = FileSelectionDialog(root)
    file_selection.run()
    root.mainloop()
    file_paths = file_selection.get_file_paths()
    try:
        parent_dir = file_paths[0].removesuffix(file_paths[0].split('/')[-1])
    except TypeError:
        return None
    except IndexError:
        return None
    ###################
    # Video downloading
    ###################
    print('Downloading...')
    video_downloader = VideoDownload(file_paths, parent_dir)
    video_name_list = video_downloader.run()
    video_name_list = [v_name.removesuffix('.mp4') for v_name in video_name_list]
    with open('视频id.txt', encoding='utf-8') as f:
        next(f)
        for line in f:
            temp_line = line.strip().split(',')
            video_id[temp_line[0]] = temp_line[1]
    print('Done.')


def split_upload(name, _video_id, _parent_dir):
    #################
    # Video splitting
    #################
    print('Splitting...')
    directories = []
    date = re.search(r'[\d]{4}\.[\d]{2}\.[\d]{2}', name)
    date = date.group(0)
    show_name = name.replace(date, '')
    date = date.replace('.', '')
    if show_name.endswith('期'):
        show_name = show_name.removesuffix('期')
        show_id = _video_id[show_name]
        directory = '{0}/{1}'.format(show_id, date)
        directories.append(directory)
        path = os.path.join(_parent_dir, directory)
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)
        stat_filename = _parent_dir + show_name + '/' + name + '.xlsx'
        video_split = VideoSplitter(_parent_dir + name + '.mp4',
                                    stat_filename)
        video_split.split()
        os.chdir(_parent_dir)
    elif show_name.endswith('-上') or show_name.endswith('-下'):
        part = show_name[-2:]
        show_name = show_name[:-2].removesuffix('期')
        show_id = _video_id[show_name]
        directory = '{0}/{1}{2}'.format(show_id, date, part)
        directories.append(directory)
        path = os.path.join(_parent_dir, directory)
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)
        try:
            stat_filename = _parent_dir + show_name + '/' + name[:-2] + '-上下.xlsx'
            video_split = VideoSplitter(_parent_dir + name + '.mp4',
                                        stat_filename,
                                        part)
            video_split.split()
        except FileNotFoundError:
            stat_filename = _parent_dir + show_name + '/' + name + '.xlsx'
            video_split = VideoSplitter(_parent_dir + name + '.mp4',
                                        stat_filename)
            video_split.split()
        os.chdir(_parent_dir)
    print('Done.')
    ############################
    # Video uploading to FTP server
    ############################
    print('Uploading...')
    ftp = FTPUploader('Your FTP server address', 'FTP server port', FTP_USERNAME, FTP_PASSWORD,
                      directories, _parent_dir)
    ftp.run()
    print('Done.')


if __name__ == '__main__':
    select_download()
    i = 0
    while i < len(video_name_list):
        p1 = multiprocessing.Process(target=split_upload,
                                     args=(video_name_list[i], video_id, parent_dir))
        try:
            p2 = multiprocessing.Process(target=split_upload,
                                         args=(video_name_list[i+1], video_id, parent_dir))
        except IndexError:
            p2 = multiprocessing.Process()
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        i += 2
