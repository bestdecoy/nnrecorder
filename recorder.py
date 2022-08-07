import subprocess
import time
import huya
import re
import os
import sys
import threading
import convert
import ctypes
from config import load_conf
from threading import Thread


# 杀ffmpeg进程
def kill_ff(pid):
    kill_ff = subprocess.Popen("taskkill /im {} /f".format(int(pid)), shell=True, stdout=subprocess.PIPE)
    kill_ff.kill()

def check_ff():
    ff_code = 0
    # print("-> Attention: 正在检查FFmpeg是否存在。", end="\n")
    config ={}
    config = load_conf(config)
    
    if os.path.exists(config["ff_url"]):
        # print("\r-> ffmpeg存在。", end="\n")
        ff_code = 1
    else:
        print("\033[0;31;40m", '\r-> Warning: 缺少关键程序，FFmpeg不存在！', "\033[0m", end="\n\n")
        print('1. 请确保ffmpeg.exe在config.json的指定路径"{}"下，或修改"ff_url"的记录。\n'.format(config["ff_url"]),
              '\r2. 参考做法：在config.json的键"ff_url"记录为"F:/ffmpeg/bin/ffmpeg.exe"，将ffmpeg.exe放入"F:/ffmpeg/bin/"。\n',
              '\n\r# 下载地址：https://github.com/BtbN/FFmpeg-Builds/releases 或 https://ffmpeg.org/download.html\n')
    return ff_code

class recorder(threading.Thread):

    def __init__(self, rid):
        threading.Thread.__init__(self)
        self.config = {}
        self.config = load_conf(self.config)
        self.stop_ff = 0
        self.rid = rid
        self.rec_info = [""]

    def rec_ffpid(self):
        # 记录ffmpeg的pid
        tasklist = subprocess.Popen("tasklist", stdout=subprocess.PIPE, shell=True)
        pid = tasklist.stdout.read().decode("ansi")
        pid = re.findall("ffmpeg.exe([\s\S]*?) Co",pid)
        pid = [i.replace(" ", "") for i in pid]
        tasklist.kill()
        f = open((os.getcwd()+'/ffmpeg_pid.log'), 'a')
        f.write(pid[len(pid)-1]+'\n')
        f.close()        

    def kill_sub_ff(self, sub_pid):
        f = open((os.getcwd()+"/ffmpeg_pid.log"), "r")
        sub_ff_pid = f.readlines()
        f.close()
        counterpart_pid = 0
        for info in sub_ff_pid:
            counterpart_pid = re.findall("{}:([\s\S]*?)\n".format(int(sub_pid)), info)
            if len(counterpart_pid):
                break
        try:
            kill_ff(counterpart_pid[0])
        except:
            pass
                

    def run(self):
        self.recorder_base()

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
    
    # 利用异常关掉线程            
    # https://zhuanlan.zhihu.com/p/142781154
    def stop_thread(self): 
        thread_id = self.get_id() 
        live_info = huya.get_real_url(self.rid)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
			ctypes.py_object(SystemExit))
        print("\033[0;31;40m", '\r-> 用户终止录制线程，停止录制【{}】。'.format(live_info[2]), "\033[0m", end="\n\n") 
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print("-> 关闭线程{}失败。".format(thread_id))

    def recorder_base(self):

        MB = 1024*1024
        GB = MB * 1024

        # 导入config
        config = {}
        config = load_conf(config)

        rec_i = [0]
        last_save_path = ['', '']

        # taskkill /IM "ProcessName.exe" /F
        while(1):
            ff_record_url, liveTitle, liveName = huya.get_real_url(self.rid)
            if ff_record_url ==0 :
                print("\033[0;31;40m", '\r-> 主播已下播，停止录制。', "\033[0m", end="\n\n")
                self.stop_thread()  # 下播停止线程
            curr_time = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
            log_path = os.path.dirname(os.path.realpath(__file__)) + "/Record_{}-{}.log".format((time.strftime('%Y%m%d',time.localtime(time.time()))), liveName)
            dir_path = self.mkdir_new(liveName, config["rc_save_path"], log_path)
            # ff_save_file_name = config["rc_save_path"] + "虎牙-{}-{}-{}.flv".format(liveName, liveTitle, curr_time)
            ff_save_file_name = dir_path + "虎牙-{}-{}-{}.flv".format(liveName, liveTitle, curr_time)
            ff_url = config["ff_url"]
            # 必须带UA，否则403
            ff_ua = config["ff_ua"]

            # subprocess lib : https://docs.python.org/zh-cn/3/library/subprocess.html
            # 调用ffmpeg
            ff_i = '"{}" -user_agent "{}" -i "{}" -loglevel quiet -hide_banner -nostats -progress pipe:1 -c copy {} '.format(ff_url, ff_ua, ff_record_url, ff_save_file_name)
            ffmpeger = subprocess.Popen(
                ff_i, 
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)

            # stop_ff 关闭线程标识符，提前关闭ffmpeg
            if (self.stop_ff==1):
                ffmpeger.stdin.write('q'.encode("GBK"))  # 停止录制
                ffmpeger.kill()
                self.rec_info = [""]  # 清零缓冲区
                self.kill_sub_ff(ffmpeger.pid) # 杀ffmpeg
                break
            
            # 记录ffmpeg pid
            f = open((os.getcwd()+"/ffmpeg_pid.log"),"a")
            f.write(str(ffmpeger.pid)+":")
            f.close()
            self.rec_ffpid()    

            rec_i[0] += 1
            r_frame = [0]
            r_size = [0, 1]
            r_speed = [0]
            r_time = [0]
            progress_reader_thread = Thread(target=self.progress_reader, args=(ffmpeger, r_frame, r_size, r_speed, r_time))  # Initialize progress reader thread
            progress_reader_thread.start()  # Start the thread

            
            time.sleep(1)
            while(1):
                #导出输出进度
                self.rec_info[0] = "\r=> (第{}个)【{}】-> 录制帧数：{}， 录制大小：{:.2f}MB， 录制时间：{}， 录制速度：{}"\
                        .format(rec_i[0], liveName, r_frame[0], (r_size[0]/1024/1024), r_time[0], r_speed[0])
                f = open((os.getcwd()+"/temp/rec_{}.log".format(liveName)), "w")
                f.write(str(self.rec_info[0]))
                f.close()
                # print("\r# (第{}个)【{}】-> 录制帧数：{}， 录制大小：{:.2f}MB， 录制时间：{}， 录制速度：{}"\
                #         .format(rec_i[0], liveName, r_frame[0], (r_size[0]/1024/1024), r_time[0], r_speed[0]), end='')
                
                r_size[1] = r_size[0]  # 经过1.5s后大小还一样判断停止并重新开始尝试录制
                time.sleep(1.5)
                if (r_size[0] >= (int(config["slice_size"])* MB)) or (r_size[1]==r_size[0]) or (self.stop_ff==1):  # 控制大小和异常重启
                    ffmpeger.stdin.write('q'.encode("GBK"))  # 停止录制
                    ffmpeger.kill()
                    self.rec_info = [""]  # 清零缓冲区
                    # self.kill_sub_ff(ffmpeger.pid) # 杀ffmpeg
                    break

            try:
                ffmpeger.wait(2)
                f = open(log_path, "a")
                f.write("# {} 直播流下载完成，在'{}'\n".format(time.strftime('%Y%m%d %H:%M:%S',time.localtime(time.time())), ff_save_file_name) )
                f.close()
            except subprocess.TimeoutExpired:
                ffmpeger.kill() 
                self.rec_info = [""]  # 清零缓冲区


            # flv转mp4线程
            if config["convert_or_not"] == 1:
                convert_thread = Thread(target=convert.flv2mp4, 
                                        args=(ffmpeger, 
                                        ff_save_file_name, 
                                        log_path))
                convert_thread.start()
            
            # 是否删除原始flv
            if rec_i[0] != 1:
                if config["remove_ori_flv"] == 1:
                    self.delete_flv(last_save_path[0], log_path)
            last_save_path[0] = ff_save_file_name

            progress_reader_thread.join(2)

        # 关闭线程最后一个屏障
        if self.stop_ff == 1:
            ffmpeger.stdin.write('q'.encode("GBK"))  # 停止录制
            ffmpeger.kill()
            self.rec_info = [""]  # 清零缓冲区
            self.kill_sub_ff(ffmpeger.pid) # 杀ffmpeg
            thread_id = self.get_id() 
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,ctypes.py_object(SystemExit))
            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
                print("-> 关闭线程{}失败。".format(thread_id)) 

    # 监控ffmpeg状态
    def progress_reader(self, procs, r_frame, r_size, r_speed, r_time):  # r -> record
        # https://stackoverflow.com/questions/67386981/ffmpeg-python-tracking-transcoding-process
        while True:
            if procs.poll() is not None:
                break  # Break if FFmpeg sun-process is closed

            progress_text = procs.stdout.readline()  # Read line from the pipe

            # Break the loop if progress_text is None (when pipe is closed).
            if progress_text is None:
                break

            progress_text = progress_text.decode("utf-8")  # Convert bytes array to strings
            progress_text = progress_text.replace(" ", "")  # 除空格符

            # 查找参数
            if progress_text.startswith("frame="):
                r_frame[0] = int(progress_text.partition('=')[-1])  
            if progress_text.startswith("total_size="):
                r_size[0] = int(re.findall(r'total_size=([\s\S]*?)$', progress_text)[0])
            if progress_text.startswith("out_time="):
                r_time[0] = re.findall(r'out_time=([\S]*?)000', progress_text)[0]
            if progress_text.startswith("speed="):
                # print("#"*500, progress_text)
                r_speed[0] = re.findall(r'speed=([\S]*?)$', progress_text)[0]

    # 当文件夹为空时，创建存放单个主播的视频文件夹
    def mkdir_new(self, liveName, rs_path, log_path, liver="虎牙"):
        path = "{}{}-{}".format(rs_path, liver, liveName) # rs_path -> root_save_path
        if not (os.path.exists(path)):
            os.makedirs(path)
            f = open(log_path, "a")
            f.write("{} 文件夹已创建，在'{}'\n".format(time.strftime('%Y%m%d %H:%M:%S',time.localtime(time.time())), path) )
            f.close()
        return path + '/'

    # 是否删除原始flv
    def delete_flv(self, ff_save_file_name, log_path):
        try:
            os.remove(ff_save_file_name)
        except:
            print("删除flv失败")
        if os.path.exists(ff_save_file_name):
            f = open(log_path, 'a')
            f.write("# {} 原始flv删除失败！在'{}'\n" \
                .format(time.strftime('%Y%m%d %H:%M:%S',time.localtime(time.time())), 
                        ff_save_file_name) )
            f.close()
        else: 
            f = open(log_path, "a")    
            f.write("# {} 原始flv已删除，在'{}'\n" \
                        .format(time.strftime('%Y%m%d %H:%M:%S',time.localtime(time.time())), 
                                ff_save_file_name) )
            f.close()