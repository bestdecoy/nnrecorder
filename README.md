# nnrecorder - 南南录播姬 

# 1. 介绍
南南录播姬是一个可以对多个直播间进行自动监控/录制主流直播的Python脚本。

目前尚在开发中，仅支持Huya，未来增添更多直播平台以及GUI版。

## 1.1 使用截图
![使用截图](https://s1.ax1x.com/2023/04/30/p93vkcQ.png)
## 1.2 相关文件介绍
### 1.2.1 Config.json 参数说明
本脚本通过修改根目录下config.json不同键的值实现各项功能，功能如下：
|  参数   | 解释  |
|  ----  | ----  |
| ff_ua  | ffmpeg的user-agent |
| ff_url  | 使用者的ffmpeg地址 |
| rid  | 欲监控/录制的直播号，用","隔开，可带空格 |
| rc_save_path  | 录制文件存放地址 |
| slice_size  | 保存的单个文件大小(MB) |
| auto_record  | 是否自动录制(0 or 1) |
| gap_time  | 监控间隔时间(s) |
| convert_or_not  | 是否自动转码mp4(0 or 1)|
| remove_ori_flv  | 转码后是否自动删除flv(0 or 1)，不推荐 |
| alert_space  | 录像保存路径盘符余量警戒值，低于该值停止程序(MB) |
# 2. 使用
## 2.1 环境准备
1. Python >= 3.8

2. 第三方库：

* plyer

3. 第三方应用程序：

* ffmpeg：https://github.com/BtbN/FFmpeg-Builds/releases

*下载ffmpeg后在config.json中指定ffmpeg地址，参见：1.2.1。
# 3. 附录
## 3.1 其他地址
码云地址：https://gitee.com/bestdecoy/nnrecorder
## 3.2 引用
直播源链接来自项目：https://github.com/wbt5/real-url
