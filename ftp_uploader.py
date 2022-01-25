from ftplib import FTP
from copy import deepcopy
import os


class FTPUploader:
    def __init__(self, host, port, username, password, directories=None, parent_dir=''):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.directories = directories
        self.parent_dir = parent_dir
        self.ftp = FTP()

    def login(self):
        self.ftp.connect(self.host, self.port)
        self.ftp.login(self.username, self.password)

    def run(self):
        self.login()
        ftp_parent_dir = self.ftp.pwd()
        directory_names = deepcopy(self.ftp.nlst())
        for dir in self.directories:
            first_level, second_level = dir.split('/')
            if first_level not in directory_names:
                self.ftp.mkd(first_level)
                directory_names.append(first_level)
            self.ftp.cwd(first_level)
            self.ftp.mkd(second_level)
            self.ftp.cwd(second_level)
            video_dir = os.path.join(self.parent_dir, dir)
            files = os.listdir(video_dir)
            os.chdir(video_dir)
            for file in files:
                with open(file, 'rb') as f:
                    self.ftp.storbinary('STOR {}'.format(file), f)
            os.chdir(self.parent_dir)
            self.ftp.cwd(ftp_parent_dir)
        self.ftp.quit()
