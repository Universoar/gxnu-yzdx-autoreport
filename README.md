# 广西师范大学-易班-易知独秀-自动体温上报脚本

本项目仅供技术交流，使用者有责任和义务保证自己上传的打卡数据真实可靠。
因本人已经离校，此项目不再维护。

## 使用

- 在Python运行时中使用
```
# 安装依赖
pip install requests

# 运行
python main.py
```
- 直接到[这里](https://github.com/Universoar/gxnu-yzdx-autoreport/releases)下载二进制文件运行

## 关于多用户

运行一次程序后，修改程序目录下的data.json即可。格式为
```
[{"username": "xxxxx", "password": "xxxxx"},
{"username": "xxxxx", "password": "xxxxx"},
...,
{"username": "xxxxx", "password": "xxxxx"}
]
```
