import os

class DirFiles():
    files = []
    
    def __init__(self, dir_path):
        self.files = os.listdir(dir_path)
    
    def file_count(self):
        return len(self.files)
        

