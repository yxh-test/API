#Author:花花儿
import yaml
from 实战__框架三.common.public import filepath


class OperationYaml:
	# def readyaml(self):
	# 	with open(filepath('data','login.yaml'),'r',encoding='utf-8') as f:
	# 		return list(yaml.safe_load_all(f)) # 针对单个的API，需要利用参数化，所以要读取全部转成列表

	def dictyaml(self, filedir='config', filename='books.yaml'):
		with open(filepath(filedir,filename),'r',encoding='utf-8') as f:
			return yaml.safe_load(f) # 此处返回的是字典，只有一组数据。yaml文件是根据“---”分隔多组数据的

if __name__=='__main__':
	obj = OperationYaml()
	for item in obj.dictyaml().items():
		print(item)