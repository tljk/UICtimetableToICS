# UIC课表转日历

#### 介绍
因为懒得一个个添加，所以写了个一键程序  
原理是读取课表的html文件再以ics的格式输出  
包含提醒

#### 安装教程

1.  python 3
2.  bs4，tkinter，datetime

#### 使用说明

1.  登录mis，访问[https://mis.uic.edu.hk/mis/student/tts/timetable.do](https://mis.uic.edu.hk/mis/student/tts/timetable.do)，另存为html，确认打开是有课表的
2.  运行main，打开html，保存ics
3.  导入ics到日历
