import fnmatch
import os
import sys
import threading
import atexit
from queue import Queue
import time
import re
from file_util import DirFiles
import qrdecode
import wechat_image_decode


class DirMonitor():
    _interval = 1.0

    def __init__(self, callback=None, target=None, destination=None):
        if not target:
            raise Exception("target path cannot be None!")
        self.target_dir = target if not target[-1] == "/" else target[:-1]
        self.destination = destination if not destination[-1] == "/" else destination[:-1]
        self._times = {}
        self._files = []
        self._running = False
        self._lock = threading.Lock()
        self.ignore_path = os.path.join(self.target_dir, ".gitignore")
        self.callback = callback or self._callback
        self._threads = []
        self.working_thread = threading.Thread(target=self._monitor)
        self.working_thread.setDaemon(True)
        self._threads.append(self.working_thread)

        atexit.register(self._exiting)

    def _monitor(self):
        self._update_ignore()
        old_dir_files = DirFiles(dir_path = self.target_dir)
        while True:
            new_dir_files = DirFiles(dir_path = self.target_dir)
            file_increment = new_dir_files.file_count() - old_dir_files.file_count()
            if file_increment > 0 :
                file_increments_list = new_dir_files.file_increments_list(old_dir_files.file_count())
                for file in file_increments_list:
                    if file[-4:] != '.dat':
                        continue
                        
                    dat_file_path = new_dir_files.path_name(file)
                    new_file_path = self.destination + "\\" + file
                    #先把dat解码成图片
                    decoded_img_path = wechat_image_decode.decode_dat(dat_file_path, new_file_path)
                    #然后再识别图片内容是否是群二维码
                    decode = qrdecode.decode(decoded_img_path)
                    #只保留是群二维码的图片，不是的删除
                    if decode.find('https://weixin.qq.com/g/') != -1:
                        print("[%s]new add qrcode %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), decoded_img_path))
                    else:
                        os.remove(decoded_img_path)
                old_dir_files = new_dir_files
            #queue = Queue()
            #queue.put(self.target_dir)
            # Check modification times on all files under local_dir.
            #while not queue.empty():
                #dir_path = queue.get()
                #for item in os.listdir(dir_path):
                    # item_path = os.path.join(dir_path, item)
                    # if not self._ignored(item_path):
                        # if os.path.isdir(item_path):
                            # queue.put(item_path)
                        # elif self._modified(item_path):
                            # if item == ".gitignore":
                                # self._update_ignore()
                            # thread = threading.Thread(target=self.callback, args=(item_path,))
                            # thread.start()
                            # self._threads.append(thread)                                                 
            time.sleep(1)

    def _ignored(self, item_path):
        if os.path.isdir(item_path):
            item_path += "/"
        for pattern in self.ignore_pattern:
            regex = fnmatch.translate(pattern)
            if re.search(regex, item_path[len(self.target_dir)+1:]):
                return True
        return False

    def _update_ignore(self):
        self.ignore_pattern = []
        if os.path.isfile(self.ignore_path):
            with open(self.ignore_path, "r+") as file:
                pattern = re.compile(r"^\s*[#\n]")
                lines = file.readlines()
                for line in lines:
                    if not pattern.match(line):
                        self.ignore_pattern.append(line[:-1])
        self.ignore_pattern.append(".git/")

    def start(self, interval=1.0):
        if interval < self._interval:
            self._interval = interval

        self._lock.acquire()
        if not self._running:
            prefix = 'monitor (pid=%d):' % os.getpid()
            print('%s Starting change monitor.' % prefix, file=sys.stderr)
            print("Monitor directory %s." % self.target_dir)
            self._running = True
            self.working_thread.start()
        self._lock.release()

    def _exiting(self):
        for thread in self._threads:
            thread.join()

    def _modified(self, path):
        try:
            if not os.path.isfile(path):
                return False

            # Check for when file last modified.
            mtime = os.stat(path).st_mtime
            if path not in self._times:
                self._times[path] = mtime
                return False
            elif mtime != self._times[path]:
                self._times[path] = mtime
                return True
        except:
            return True

        return False

    def track(self, path):
        if not path in self._files:
            self._files.append(path)

    def _callback(self):
        pass








