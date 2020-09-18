#Author:花花儿
import datetime
import os

def filepath(filedir='data',filename='books.yaml'):
	"""

	:param filedir: 相对于项目根目录的文件目录路径
	:param filename: 文件名称
	:return: 文件的整路径
	"""
	return os.path.join(
		os.path.dirname(os.path.dirname(__file__)),
		filedir,
		filename)

def writeContent(content):
	"""写bookID，将添加书籍的ID存入到bookID中"""
	# print('写的时间：',datetime.datetime.now()) # 调试信息
	with open(filepath(filedir='data',filename='bookID'),'w') as f:
		f.write(str(content))

def readContent():
	"""读取bookID，将添加书籍的ID作为查看书籍的ID，上下文参数传递"""
	# print('读的时间：', datetime.datetime.now()) # 调试信息，读的时间需要在写的时间之后
	with open(filepath(filedir='data',filename='bookID'),'r') as f:
		return f.read()

