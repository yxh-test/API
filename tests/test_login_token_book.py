#Author:花花儿

from 实战__框架三.base.method import Requests
from 实战__框架三.common.public import writeContent, readContent
from 实战__框架三.utils.operationExcel import OperationExcel
from 实战__框架三.utils.operationExcel import ExcelVar
import pytest
import json

excel = OperationExcel()
obj = Requests()
@pytest.mark.parametrize('datas',excel.runs())

def test_login_book(datas):

	"""将前置执行测试用例封装成函数放在了operationExcel"""

	def case_assert_result(r):
		"""封装断言"""
		assert datas[ExcelVar.statusCode] == r.status_code
		assert datas[ExcelVar.expect] in json.dumps(r.json(), ensure_ascii=False)

	def ReUrl():
		# 上下参数关联，添加数据的bookID，后面要查看、修改、删除此bookID的书籍，因此，url需要替换掉bookID，用函数封装
		url = str(datas[ExcelVar.caseUrl]).replace('{bookID}', readContent())
		return url


	if datas[ExcelVar.method]=='get':
		if 'books' in datas[ExcelVar.caseUrl]:
			r = obj.get(url=datas[ExcelVar.caseUrl],
			            headers=excel.runPreCase(datas[ExcelVar.casePre],datas[ExcelVar.headers]))
			case_assert_result(r=r)
		else:
			r = obj.get(url=ReUrl(),
			            headers=excel.runPreCase(datas[ExcelVar.casePre],datas[ExcelVar.headers]))
			case_assert_result(r=r)


	elif datas[ExcelVar.method]=='post':
		r = obj.post(url=datas[ExcelVar.caseUrl],
		            json = excel.params(datas[ExcelVar.params]),
		            headers=excel.runPreCase(datas[ExcelVar.casePre],datas[ExcelVar.headers])) # 登录没有请求头，但是这个headers在这会干扰，在登录时也会执行前置测试点

		# 将bookID写到文件中，注意首先登陆的login post请求是不执行的，在excel中设置的是n
		writeContent(content=r.json()[0]['datas']['id'])
		case_assert_result(r=r)

	elif datas[ExcelVar.method]=='put':

		r=obj.put(url=ReUrl(),json=excel.params(datas[ExcelVar.params]),
		            headers =excel.runPreCase(datas[ExcelVar.casePre],datas[ExcelVar.headers]))
		case_assert_result(r=r)

	elif datas[ExcelVar.method]=='delete':

		r = obj.delete(url=ReUrl(),
		               headers=excel.runPreCase(datas[ExcelVar.casePre], datas[ExcelVar.headers]))
		case_assert_result(r=r)


if __name__=='__main__':
	# pytest.main(["-s","-v","test_login_token_book.py"])
	pytest.main(["-s", "-v", "test_login_token_book.py", "--alluredir", "./report/result"]) #  生成json数据
	import subprocess
	subprocess.call('allure generate report/result/ -o report/html --clean', shell=True)
	subprocess.call('allure open -h 127.0.0.1 -p  8088 ./report/html', shell=True)
