from dirmonitor import DirMonitor
import os

def callback(filepath):
    print(filepath + "has changed!")

dir_path = "C:\\Users\gxrb\Documents\WeChat Files\qq987958223\FileStorage\Image\\2020-10"
decoded_dir_path = "C:\\Users\\gxrb\\Desktop\\decode\\2020-10"
#解码目录不存在则创建
if not os.path.isdir(decoded_dir_path):
    os.makedirs(decoded_dir_path)
monitor = DirMonitor(target=dir_path, destination=decoded_dir_path, callback=callback)
monitor.start()