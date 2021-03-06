import os
import sys

class DirFiles():
    files = []
    dir_path = ''
    
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.files = os.listdir(dir_path)
        self.files.sort(key = self.compare)
    
    def file_count(self):
        return len(self.files)
        
    def file_increments_list(self, start):
        return self.files[start:self.file_count():]
        
    def compare(self, file):
        file = self.path_name(file)
        if os.path.exists(file):
            return os.stat(file).st_ctime
        return 0
        
    def path_name(self, file):
        return self.dir_path + "/" + file


    
