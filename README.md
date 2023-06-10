# sitedirscan
一款敏感目录探测小工具
## 👋Feature:

- 可指定本地文件目录生成待扫描的自定义目录列表进行探测
- 如未指定本地文件目录，就使用默认目录字典进行探测
- 多线程探测，可指定线程数量
- 按ctrl+c可提前终止探测，并返回扫描中断位置
- 因手动终止或网络中断等原因导致程序提前终止时，支持断点续扫
- 设置网络请求频率随机延时以应对反爬机制

***
##  ✨Help menu:
![Help_Menu](https://github.com/Afl0wer/sitedirscan/blob/main/help_menu.gif "Help Menu")  
## 🚀Usage:
- 指定要进行目录扫描的web地址，加载默认字典并以默认线程数(3)开始扫描：  
  
  `directory_dectect.py --url http://www.xxx.com/`
---
- 指定要进行目录扫描的web地址,并指定本地文件目录以遍历生成自定义的文件目录列表，并以默认线程数(3)开始探测：  
  
  `directory_dectect.py --url http://www.xxx.com/ --localdir D:\\dict`
---
- 指定要进行目录扫描的web地址,加载默认字典并指定上次扫描中断的位置(文件目录)继续扫描：  
  
  `directory_dectect.py --url http://www.xxx.com/ --restart /manager/html`
---
- 指定要进行目录扫描的web地址,加载默认字典并以设置的线程数开始扫描：  
  
  `directory_dectect.py --url http://www.xxx.com/ -t 5`
## ⚡️Example：
![example_image](https://github.com/Afl0wer/sitedirscan/blob/main/example_image.png "example image")  
