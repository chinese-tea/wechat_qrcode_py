from dirmonitor import DirMonitor

def callback(filepath):
    print(filepath + "has changed!")

monitor = DirMonitor(target="F:\WWW\qrcode_py\\test", callback=callback)
monitor.start()