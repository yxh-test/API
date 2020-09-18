#Author:花花儿
import json

import xlrd
from 实战__框架三.common.public import filepath
from 实战__框架三.base.method import Requests
from 实战__框架三.utils.operationYaml import OperationYaml
from 实战__框架三.common.public import readContent


class ExcelVar:
	caseID = "测试用例ID"
	caseModel = "模块"
	caseName = "接口名称"
	caseUrl = "请求地址"
	casePre = "前置条件"
	method = "请求方法"
	paramsType = "请求参数类型"
	params = "请求参数"
	expect = "期望结果"
	isRun = "是否运行"
	headers = "请求头"
	statusCode = "状态码"


class OperationExcel():

	def getSheet(self):
		book=xlrd.open_workbook(filepath('data','bookAPI.xlsx'))
		return book.sheet_by_index(0)

	@property
	def getExcelDatas(self):
		# 获取excel表中所有的测试用例数据
		datas =[]
		title=self.getSheet().row_values(0)
		# 忽略首行：range从1开始
		for row in range(1,self.getSheet().nrows):
			# 获取每一行的值
			row_values = self.getSheet().row_values(row)
			datas.append(dict(zip(title,row_values)))
		return datas

	def runs(self):
		"""获取到可执行的测试用例"""
		run_list = []
		for item in self.getExcelDatas:
			isRun = item[ExcelVar.isRun]
			if isRun=='y':
				run_list.append(item)
			else:pass
		return run_list

	def case_lists(self):
		"""获取excel中所有的测试用例"""
		caselist=[]
		for item in self.getExcelDatas:
			caselist.append(item)
		return caselist

	def params(self,params):
		"""对非空的请求参数做反序列化处理"""
		if len(str(params).strip()) == 0:
			pass
		elif len(str(params).strip()) > 0:
			return json.loads(params)

		"""
		token值前后关联的思路：
		1、先依据前置测试条件找到关联的前置测试用例"
		2、执行前置测试用例
		3、获取它的结果信息
		4、拿它的结果信息替换对应测试点的变量
		"""

	def headers(self,headers):
		"""对请求头做反序列的处理"""
		if len(str(headers).strip()) == 0:
			pass
		elif len(str(headers).strip()) > 0:
			return json.loads(headers) # json.loads将字符串转成python格式的字典

	def case_prev(self,casePrev):
		"""
		前提条件：前置条件的名称就是需要提前执行测试用的caseID
		依据前置测试条件找到关联的前置测试用例
		:param casePrev: 前置测试条件
		:return:
		"""
		# for item in self.runs():
		for item in self.case_lists():# 此处login设置为不执行y，但是涉及到关联，所以需要执行测试。
			if item[ExcelVar.caseID] == casePrev:
				return item
		return None

	def preReplaceHeaders(self,preResult,headers):
		"""
		替换被关联测试点的请求头变量的值
		:param preResult:
		:return:
		思路：
		1、获取headers
		2、判断headers有没有token这个变量，有就替换这个变量值
		"""
		# for item in self.runs():
		# 	headers = item[ExcelVar.headers]
		# 	if '{token}' in headers:
		# 		headers = str(headers).replace('{token}',preResult)
		# 		return json.loads(headers)


		if '{token}' in headers:
			headers = str(headers).replace('{token}',preResult)
			return json.loads(headers)
		else:pass

	def runPreCase(self,preCase,headers):
		"""执行前置测试用例"""
		if self.case_prev(preCase) ==None:pass
		else:
			r = Requests().post(url=self.case_prev(preCase)[ExcelVar.caseUrl],
			             json=json.loads(self.case_prev(preCase)[ExcelVar.params]))
			preResult = r.json()['access_token']

			# 替换被关联测试点中请求头信息的变量
			# headers_str = json.dumps(self.headers(headers))  # 获取原始excel表中的headers,原始的headers是字符串，用headers()处理变成python格式的字典，用采用dumps变成字符串，多此一举。
			header = self.preReplaceHeaders(preResult, headers)
			return header


if __name__=='__main__':
	obj = OperationExcel()
	for item in obj.case_lists():
		print(item)

