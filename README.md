# nnreco4der - 南南录播姬 

#### 介绍
南南录播姬是一个可以自动录制主流直播的Python脚本。

目前尚在开发中，仅支持Huya。

#### 使用截图
![使用截图](https://pic.rmb.bdstatic.com/bjh/a25876aa592316a6c981961c6511b2ae.png)

#### Config.json 参数说明

|  表头   | 表头  |
|  ----  | ----  |
| ff_ua  | ffmpeg的user-agent |
| ff_url  | 使用者的ffmpeg地址 |
| rid  | 欲监控/录制的直播号，用","隔开，可带空格 |
| rc_save_path  | 录制文件存放地址 |
| slice_size  | 保存的单个文件大小(MB) |
| auto_record  | 是否自动录制(0 or 1) |
| gap_time  | 监控间隔时间 |
| convert_or_not  | 是否自动转码mp4(0 or 1)|
| remove_ori_flv  | 转码后是否自动删除flv(0 or 1)，不推荐 |

#### 环境准备
Python >= 3.8

第三方库：
plyer
#### 其他
码云地址：https://gitee.com/bestdecoy/nnrecorder
#### 引用
直播源链接来自项目：https://github.com/wbt5/real-url
