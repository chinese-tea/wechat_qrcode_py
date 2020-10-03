from dirmonitor import DirMonitor
import os

def callback(filepath):
    print(filepath + "has changed!")

dir_path = "F:\WWW\qrcode_py\\test"
decoded_dir_path = dir_path + "\\decode"
#解码目录不存在则创建
if not os.path.isdir(decoded_dir_path):
    os.mkdir(decoded_dir_path)
monitor = DirMonitor(target=dir_path, destination=decoded_dir_path, callback=callback)
monitor.start()