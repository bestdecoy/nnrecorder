# offical lib
import subprocess
import time
import re
import os
import sys
from threading import Thread
# private lib
import huya
import shutil
from recorder import *
from config import *
from console import *
from monitor import *


class menu():
    def __init__(self):
        self.config = {}
        self.config = load_conf(self.config)  # copy config.json to config
        self.rids = mult_rids(self.config["rid"])
        self.sel_rids = []  # 用户选中的直播间号

    def live_stat(self):
        # print("\r# 此时的直播间参数为：\n")
        # print('\r# "rid"："\033[7m{}\033[0m"'.format(self.config["rid"]))
        # print('\r# 总数：{} 个\n'.format(len(self.rids)))
        # for i in [3, 2, 1, 0]: 
        #     print("\r（{}秒后清空以上消息。）".format(i),end="")
        #     time.sleep(1)

        os.system("cls")
        print("\r-> 以下是当前记录的直播间的开播情况：")
        print("\r# 在程序根目录下的config.json中的项rid修改直播间列表。")
        print("\r# 当前盘符{}的剩余容量为：{:.1f}MB，低于{}MB将会停止程序。\n".format((self.config["rc_save_path"][0]+":"),
                                                                                check_remain_space(self.config["rc_save_path"]),
                                                                                self.config["alert_space"]
                                                                            ))
        i = 0
        for i in range(len(self.rids)):
            live_info = check_info(self.rids[i])
            i += 1
            if live_info[0] != 0:
                print("\r[{}]".format(i), "\033[1;32m● 正在直播 \033[0m->",
                    "【{}】 - {}".format(live_info[2], live_info[1]))
            else:
                print("[{}]".format(i),"● 未在直播 ->",
                        "【{}】".format(live_info[2]))
            time.sleep(1)

    # # 选定后的菜单
    # def live_stat_rec(self):
    #     while(1):
    #         os.system("cls")
    #         print("\r-> 以下是当前记录的直播间的开播情况：")
    #         print("\r# 在程序根目录下的config.json中的项rid修改直播间列表。\n")
    #         i = 0
    #         for i in range(len(self.rids)):
    #             live_info = check_info(self.rids[i])
    #             i += 1
    #             if live_info[0] != 0:
    #                 print("\r[{}]".format(i), "\033[1;32m● 正在直播 \033[0m->",
    #                     "【{}】 - {}".format(live_info[2], live_info[1]))
    #                 if 
    #             else:
    #                 print("[{}]".format(i),"● 未在直播 ->",
    #                         "【{}】".format(live_info[2]))
    #             time.sleep(1)
    #         time.sleep(30)
        
    def select_live(self):
        live_i = input("\n\r-> 输入序号选择直播间进行录播/监控。\n")
        live_i = live_i.replace(" ", "").split(",")
        live_i = [(int(i)-1) for i in live_i]  # 将多个输入变成整型-1的index
        self.sel_rids = [self.rids[i] for i in live_i]  # 储存监控的直播间id

        # 判断live_i是否合法：

        for i in live_i:
            cmd = """monitor_{} = monitor(self.rids[{}], self.config["gap_time"]);monitor_{}.daemon = True;monitor_{}.start()""".format(self.rids[i], i, self.rids[i], self.rids[i])
            exec(cmd)
        # self.live_stat_rec()
        time.sleep(1)

        i_2 = 0
        live_info_temp = []
        while(1):
            os.system("cls")
            print("\r-> 以下是当前记录的直播间的开播情况：")
            print("\r# 在程序根目录下的config.json中的项rid修改直播间列表。\n")
            print("\r# 当前盘符{}的剩余容量为：{:.1f}MB，低于{}MB将会停止程序。\n".format((self.config["rc_save_path"][0]+":"),
                                                                                check_remain_space(self.config["rc_save_path"]),
                                                                                self.config["alert_space"]
                                                                            ))
            i = 0
            for i in range(len(self.rids)):
                if i_2 <= len(self.rids):
                    live_info = check_info(self.rids[i])
                    live_info_temp.append(live_info)
                else:
                    live_info = live_info_temp[i]
                i += 1
                i_2 += 1
                if live_info[0] != 0:
                    if os.path.exists((os.getcwd()+"/temp/rec_{}.log".format(live_info[2]))):
                        print("\r[{}]".format(i), "\033[1;32m● 正在直播 \033[0m->",
                        "【{}】 - {}".format(live_info[2], live_info[1]))
                        try:
                            f = open((os.getcwd()+"/temp/rec_{}.log".format(live_info[2])), "r")
                            t = f.readlines()
                            t = t[1].replace("\n", "")
                            f.close()
                            print('\033[7;36m',t,'\033[0m')
                        except:
                            pass
                    else:
                        print("\r[{}]".format(i), "\033[1;32m● 正在直播 \033[0m->",
                        "【{}】 - {}".format(live_info[2], live_info[1]))
                else:
                    if os.path.exists((os.getcwd()+"/temp/monitor_{}.log".format(live_info[2]))):
                        try:
                            f = open((os.getcwd()+"/temp/monitor_{}.log".format(live_info[2])), "r")
                            t = f.readlines()
                            t = t[1].replace("\n", "")
                            f.close()
                            print("\r[{}]".format(i),"● 未在直播 ->",
                                "【{}】".format(live_info[2]), t)
                        except:
                            print("\r[{}]".format(i),"● 未在直播 ->",
                            "【{}】".format(live_info[2]))
                    else:
                        print("\r[{}]".format(i),"● 未在直播 ->",
                            "【{}】".format(live_info[2]))
                    time.sleep(1)
            time.sleep(2)
            if i_2 >= 30:
                i_2 = 0
                live_info_temp = []  # 清空


        # monitor_head.join()
        # stop_input = input("-> 输入S停止录制。\n\n")
        # monitor_head.stop_rec()
        # time.sleep(4)
        # monitor_head.stop_thread()
        # stop_input = input("-> 输入S停止录制。\n\n")
        # monitor_1.stop_rec()
        # monitor_2.stop_rec()
        # time.sleep(4)
        # monitor_1.stop_thread()
        # monitor_2.stop_thread()


def main():
    m = menu()
    # 检查ffmpeg
    ff_code = check_ff()
    if ff_code == 0: sys.exit(0)  # 无ffmpeg退出


    m.live_stat()
    m.select_live()
    # print("\r-> 是否修改直播间参数？（Y or N, 默认不修改）")
    # y_or_n = input()
    # if y_or_n.replace(" ", "") == "":y_or_n = "N" 
    # try:
    #     y_or_n = y_or_n.upper()
    # except:
    #     print("\r -> 输入有误！\n")
    #     sys.exit(0)
    # if y_or_n == "Y":
    #     i_rid_value = input("\r-> 输入欲修改的房间号：")  # i_rid_value -> input rid value
    #     try:
    #         m = modify_conf("rid", i_rid_value)  # m -> modify
    #         config = {}
    #         config = load_conf(config)
            
    #     except:
    #         sys.exit(0)
    # else:
    #     print('\r-> 不修改房间号，此时的"rid"："{}"\n'.format(config["rid"]))
    
    # live_code = huya.get_real_url(config["rid"])

    # time.sleep(2)
    # live_stat_str = ['未开播','正在直播']
    # live_stat = 0  # 开播状态码 
    # if live_code[0] == 0:
    #     live_stat = 0
    # else:
    #     live_stat = 1

    # 创建监控直播间线程
    # 若没直播，监控

    # gap_time = config["gap_time"]  # 监控间隔时间
    # print("\n\r-> 正在监控【{}】直播间，目前{}。\n".format(live_code[2], live_stat_str[live_stat]))
    # if config["auto_record"] == 1:print("\r-> 自动录制已开启。")
    # monitor_head = monitor(config["rid"], gap_time)
    # monitor_head.daemon = False
    # monitor_head.start()
    # # monitor_head.join()
    # time.sleep(20)

    # monitor_head.stop_rec()
    # monitor_head.join()


    # live_code = huya.get_real_url(config["rid"])  # 直播后，重新获取直播间信息

    # if config["auto_record"] ==1 and live_stat ==0:  # 此时live_stat保存的是第一次检查直播状态的信息，不是当下
    #     print("\r-> 自动录制已开启。")
    #     print("\033[7;36m,","\r-> # 自动录制中:\n".format(live_code[2]), "\033[0m",
    #     "\r# 自动录制中：",
    #     "\r# 房间号：{}\n".format(config["rid"]),
    #     "\r# 录像存放地址：{}\n".format(config["rc_save_path"]))
    #     recorder()
    # else:
    #     if live_code[0] !=0 :
    #         print("\033[7;36m,","\r-> 【{}】正在直播，请检查config是否有误:\n".format(live_code[2]), "\033[0m",
    #             "\r# 房间号：{}\n".format(config["rid"]),
    #             "\r# 录像存放地址：{}\n".format(config["rc_save_path"]),
    #             "\r# 单个录像大小：{}MB\n".format(config["slice_size"]),
    #             "\n\r-> 是否开始录制？(Y or N，默认或任意输入开始)")
    #         y_or_n = input() 
    #         try:
    #             y_or_n = y_or_n.upper()
    #         except:
    #             pass
    #         if y_or_n != "N":
    #             recorder()
    #         else:
    #             print("-> 已退出程序。\n")
    #             sys.exit(0)   
            
    #     else:
    #         print("\n","\r\033[0;31;40m", "\r-> 主播未开播或出错。", "\033[0m")

if __name__ == "__main__":
    if os.path.exists((os.getcwd()+'/sub_pid.log')):
        os.remove((os.getcwd()+'/sub_pid.log'))
    try:
        shutil.rmtree(os.getcwd() + "/temp")
        os.mkdir(os.getcwd() + "/temp")
    except:pass
    try:
        os.mkdir(os.getcwd() + "/temp")
    except:
        pass
    tasklist = subprocess.Popen("tasklist", stdout=subprocess.PIPE, shell=True)
    pid = tasklist.stdout.read().decode("ansi")
    pid = re.findall("ffmpeg.exe([\s\S]*?) Co",pid)
    pid = [i.replace(" ", "") for i in pid]
    tasklist.kill()
    f = open((os.getcwd()+'/ffmpeg_pid.log'), 'w')
    for i in pid:
        f.write(i+'\n')
    f.close()

    main()


 
 
