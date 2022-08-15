import subprocess
import time

def flv2mp4(proc, path, log_path):
# def flv2mp4(proc, path, log_path, rm_bool):
    if proc.poll is not None:
        # 转换路径
        path_flv = path
        path_mp4 = path.replace("flv", "mp4")

        # -y 强制转换 
        # -loglevel quiet -hide_banner -nostats 不输出任何信息
        # https://superuser.com/questions/326629/how-can-i-make-ffmpeg-be-quieter-less-verbose
        ff_i = '"F:/ffmpeg/bin/ffmpeg" -loglevel quiet -hide_banner -nostats -i "{}" -y -c copy "{}"'.format(path_flv, path_mp4) 
        convert = subprocess.Popen(ff_i, shell=True, stdout=subprocess.PIPE)
        convert.wait()
        convert.kill()

        if convert.poll() is not None:
            try:
                f = open(log_path, "a")
                f.write("# {} 转码已完成，在'{}'\n".format(time.strftime('%Y%m%d %H:%M:%S',time.localtime(time.time())), path_mp4) )
                f.close()
            except:
                print("日志写入失败，请检查。")