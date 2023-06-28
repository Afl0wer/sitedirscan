#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
A website sensitive directory detection tool.
__author__ = 'Af10wer'
"""
import os
import re
import sys
import time
import queue
import random
import signal
import threading
import contextlib

import requests,argparse,textwrap
from urllib.parse import urlparse

FILE_SUFFIX = [".jpg",".gif",".png",".css",".js"]
web_paths = queue.Queue()
path = ''
headers = {
	'User-Agent':'Mozilla/5.2 (Windows NT 11.0; Win64; x64) AppleWebKit/538.29 (KHTML, like Gecko) Chrome/100.1.3.4 Safari/526.33',
}

def collect_paths():
	for root,dirs,files in os.walk('.'):
		for f in files:
			if os.path.splitext(f)[1] in FILE_SUFFIX:
				continue
			path = os.path.join(root,f)
			if path.startswith('.'):
				path = path[1:]
			#print(path)
			web_paths.put(path)

@contextlib.contextmanager
def chdir(path):
	origin_dir = os.getcwd()
	os.chdir(path)
	try:
		yield
	finally:
		os.chdir(origin_dir)

def load_dirfile(restart=None):
	with open('dict.txt','r',encoding='utf-8') as f:
		dirlist = f.read()
		isrestart = False
		for item in dirlist.split():
			if restart is not None:
				if isrestart:
					web_paths.put(item)
				elif item ==restart:
					isrestart = True
					print(f'Restart dirlist from:{restart}')
			else:
				web_paths.put(item)
	return web_paths

def site_dir_detect():
	global path
	while not web_paths.empty():
		path = web_paths.get()
		parseurl = urlparse(base_url)
		reobj = re.compile(r'^/.*/')
		base_url_path = reobj.findall(parseurl.path)
		if path.startswith('/') and base_url.endswith('/'):
			url = f'{base_url[:-1]}{path}'
		elif path.startswith('/') and (base_url_path == []) and ('.' not in parseurl.path) and (parseurl.path != '/'):
			url = f'{base_url}{path}'
		elif path.startswith('/') and (base_url_path == []) and ('.' in parseurl.path):
			url = f'{parseurl.scheme}://{parseurl.netloc}{path}'
		elif path.startswith('/') and (base_url_path != []):
			url = f'{parseurl.scheme}://{parseurl.netloc}{base_url_path[0][:-1]}{path}'
		time.sleep(random.randint(0,1))
		try:
			res = requests.get(url,headers=headers)
			if res.status_code == 200:
				print('[%s] : %s' % (res.status_code,url))
				with open('result.txt','a') as f:
						f.write(f'{res.status_code}:{url}\n')
		except requests.exceptions.ConnectionError as e:
			print('An error occurred：',e)
	print('The result has been saved to the local file: result.txt')

def signal_handler(signal,frame):
    print('You terminated the program prematurely.')
    print('The currently scanned directory is :',path)
    sys.exit()

def run(thread):
	threads = []
	for i in range(thread):
		t = threading.Thread(target=site_dir_detect)
		t.setDaemon(True)
		threads.append(t)
		t.start()
		while True:
			alive = False
			for i in range(thread):
				alive = alive or threads[i].is_alive()
			if not alive:
				break

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description = 'Website Sensitive Directory Detection',
		formatter_class = argparse.RawDescriptionHelpFormatter,
		epilog = textwrap.dedent('''Example:
		directory_dectect.py --url http://xxx.com/ [--localdir D:\\dict]  [--restart /manager/html] [-t 5]
			''')
		)
	parser.add_argument('--url',required=True,help='Target website to scan.')
	parser.add_argument('--localdir',help='Specify a local directory to generate a custom dictionary.If not specified,use default dictionary.')
	parser.add_argument('--restart',help='When the network interrupt scan is aborted, specify the last completed directory to continue scanning.')
	parser.add_argument('-t','--thread',type=int,default=3,help='Specify the number of threads to scan, the default is 3.')

	args = parser.parse_args()
	base_url = args.url
	restart = args.restart
	#当未使用字典文件时，就指定目录生成自定义的字典
	if args.localdir:
		with chdir(args.localdir):
			collect_paths()
	# 如未指定本地文件目录生成自定义的字典，就使用默认目录字典
	else:
		load_dirfile(restart)
	print('>>> Press Ctrl + C, program can be terminated. <<<')
	signal.signal(signal.SIGINT,signal_handler)
	signal.signal(signal.SIGTERM,signal_handler)
	run(args.thread)



