项目名称: 视频下载、分割及上传程序

版本：3.0

作者：Zhirui

测试环境：Python 3.9.7

项目简介：
读取视频数据统计文件中的开始时间和结束时间，截取给定的时间区间内的视频片段。

注意事项：
1. 视频数据统计文件必须是.xlsx格式，视频必须是.mp4格式。
2. Python 3.10.0不支持moviepy。
3. 待切割的视频名及id在“视频id.txt”中需以“{视频},{tvid}”的形式储存。

使用方法：
1. 将所有视频数据统计文件放在同一级文件夹中。
2. 打开Windows PowerShell（Windows）或者Terminal/终端（MacOS）。
3. 如果没有安装过moviepy, 输入pip3 install moviepy --user或者pip install moviepy --user， 按回车，等待安装完成。
4. 导航至split.py所在的文件夹。使用指令："cd (split.py所在文件夹的绝对路径)"，如"cd C:\Users\abc\Desktop\folder1"。
5. 输入"python main.py"或者"python3 main.py"，按回车。
6. 选择存有交付视频url的.xlsx文件，并等待完成。