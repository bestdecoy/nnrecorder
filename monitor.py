import time
import os
import threading
from numpy import record
import plyer
import platform
import ctypes
import sys
from sklearn import get_config
import huya
from recorder import *
from config import *

# 判断是否网络超时，尝试五次，超时退出程序。
def check_info(rid):
    i = 0
    while(1):
        live_info = huya.get_real_url(rid)
        if live_info[0]==0 and live_info[1]==0 and live_info[2]==0:
            # 重试
            for i in range(20):   
                i += 1
                print("\033[0;31;40m", '\r-> 网络连接失败，正在重试第{}次。'.format(i), "\033[0m") 
                live_info = huya.get_real_url(rid)
                if not (live_info[0]==0 and live_info[1]==0 and live_info[2]==0):
                    return live_info
                time.sleep(2)
            print("\033[0;31;40m", '\n\r-> 网络连接失败，请检查网络连接。'.format(i), "\033[0m") 
             # windows弹窗提醒
            if(platform.system()=='Windows'):
                plyer.notification.notify(
                    title="录制姬",
                    message="网络连接失败，请检查网络连接。".format(live_info[2]),
                    # app_icon="tubiao.ico",
                    timeout=1)
            sys.exit(0)
        break
    return live_info
            
# 监控线程
class monitor(threading.Thread):

    def __init__(self, rid, gap_time):
        threading.Thread.__init__(self)
        self.rid = rid
        self.gap_time = gap_time
        self.config = {}
        self.config = load_conf(self.config)
        self.stop_ff = [0]
        self.monitor_info = [""]  # 监控信息

    def run(self):
        self.monitor_live()
    
    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def stop_rec(self):
        self.stop_ff[0] = 1

    def stop_thread(self): 
        thread_id = self.get_id() 
        live_info = huya.get_real_url(self.rid)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
			ctypes.py_object(SystemExit))
        print("\n\033[0;31;40m", '\r-> 用户终止，停止监控【{}】。'.format(live_info[2]), "\033[0m", end="\n\n") 
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print("-> 关闭线程{}失败。".format(thread_id))

    # 监控直播
    def monitor_live(self):
        log_path = os.getcwd() + '/monitor-{}-'.format((time.strftime("%Y%m%d",time.localtime(time.time()))))
        i = 0
        print("\n")
        while(1):
            live_info = check_info(self.rid)
            i += 1
            if live_info[0] != 0:
                # windows弹窗提醒
                if(platform.system()=='Windows'):
                    plyer.notification.notify(
                        title="录制姬",
                        message="你监控的主播：【{}】开播啦！赶快去录制吧。".format(live_info[2]),
                        # app_icon="tubiao.ico",
                        timeout=1)
                self.monitor_info = [""]  # 开播，清除监控次数缓冲区
                # 如果开启了自动录制，上播后即开启录制。
                if self.config["auto_record"] == 1:
                    record_thread = recorder(self.rid)
                    record_thread.daemon = True
                    record_thread.start()   
                    # 只要开播就会进来while
                    while(1):  
                        if (self.stop_ff[0]==1):
                            time.sleep(1)
                            record_thread.stop_ff = 1
                            # 不要直接叫中断：record_thread.stop_thread() 
                            # 等待join
                            
                            record_thread.join()
                            print("\033[0;31;40m", '\r-> 用户终止，停止录制【{}】。'.format(live_info[2]), "\033[0m", end="\n\n")
                            
                            # thread_id = self.get_id() 
                            # live_info = huya.get_real_url(self.rid)
                            # res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
	                        #             ctypes.py_object(SystemExit))
                            # print("\033[0;31;40m", '\r-> 用户终止，停止录制【{}】。'.format(live_info[2]), "\033[0m", end="\n\n") 
                            # if res > 1:
                            #     ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
                            #     print("-> 关闭线程{}失败。".format(thread_id))
                            break
                        if not record_thread.is_alive():
                            self.monitor_live()  # 如果下播，递归自己继续监控

                break
            self.monitor_info[0]= "\r=> 监控【{}】{}次，每隔{}s刷新一次。".format(live_info[2], i, self.gap_time)

            f = open((os.getcwd()+"/temp/monitor_{}.log".format(live_info[2])), "w")
            f.write(str(self.monitor_info[0]))
            f.close()
            # print("\r# 监控【{}】{}次，每隔{}s刷新一次。".format(live_info[2], i, self.gap_time),end="")
            f = open((log_path+'{}.log'.format(live_info[2])), "a")
            f.write("# {} 监控主播【{}】第{}次 \n".format((time.strftime("%Y%m%d %H:%M:%S", time.localtime(time.time()))), live_info[2], i))
            f.close()
            time.sleep(int(self.gap_time))

