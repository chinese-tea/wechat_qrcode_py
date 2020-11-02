from dirmonitor import DirMonitor
import os
import time

def callback(filepath):
    print(filepath + "has changed!")

mdir = time.strftime("%Y-%m", time.localtime())
dir_path = "C:\\Users\gxrb\Documents\WeChat Files\qq987958223\FileStorage\Image\\"+mdir
decoded_dir_path = "C:\\Users\\gxrb\\Desktop\\decode\\"+mdir
#解码目录不存在则创建
if not os.path.isdir(decoded_dir_path):
    os.makedirs(decoded_dir_path)
monitor = DirMonitor(target=dir_path, destination=decoded_dir_path, callback=callback)
monitor.start()