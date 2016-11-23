#!/usr/bin/env python
# -*- coding:utf-8 -*-
import unittest
import xlrd
import json
import time
import sys
import random 
import db
import ConfigParser
import confighttp
import basehttp
import time

from htmlreport import HtmlReport
from reportlab.lib.colors import gold

config = ConfigParser.ConfigParser()
config.read('ini_file.ini')
status = config.get('RESULT','status')
dbhost = config.get('DB','db')
global save 
save = {}

run_mode = True

# 定义结构体
class DataStruct:
    '''于接收excel读取的测试数据,记录要写入测试报告的数据'''
    pass

test_data = DataStruct()
test_data.url = ''               # 接收接口url
test_data.params = {}            # 接收接口参数
test_data.expected_result = {}   # 接收预期结果
test_data.result = ''       # 接收测试结果
test_data.response = {}


# 测试用例(组)类
class TestInterfaceCase(unittest.TestCase):
    def setUp(self):
        self.config_http = confighttp.ConfigHttp(basehttp.BaseHttp().get_host(),basehttp.BaseHttp().get_header())
    def post(self):
        # 根据被测接口的实际情况，合理的添加HTTP头  
        response,respontime = self.config_http.post(test_data.url,test_data.params)
        test_data.time = respontime
        if response:
            try:
                self.assertEqual(response[status], test_data.expected_result, msg='exception')
                test_data.result = 'Pass'
                test_data.response = response
                print "返回参数为："+json.dumps(test_data.response,ensure_ascii=False)
                print "--------------------------------------"
                html_report.success_num = html_report.success_num + 1
            except AssertionError:
                test_data.result = 'Fail'
                test_data.response = response
                html_report.fail_num = html_report.fail_num + 1
        else:
            test_data.result = 'Error'
            test_data.response = {}
            html_report.error_num = html_report.error_num + 1
            return  
        if {} == response:
            test_data.result = 'Error'
            test_data.response = {}
            html_report.error_num = html_report.error_num + 1
            return
    def get(self):
        # 根据被测接口的实际情况，合理的添加HTTP头  
        response = self.config_http.get(test_data.url,test_data.params)
        if response:
            try:
                self.assertEqual(response[status], test_data.expected_result, msg='exception')
                test_data.result = 'Pass'
#                 test_data.response = json.dumps(response,ensure_ascii=False)
                test_data.response = response
                print "返回参数为："+json.dumps(test_data.response,ensure_ascii=False)
                print "--------------------------------------"
                
                html_report.success_num = html_report.success_num + 1
            except AssertionError:
                test_data.result = 'Fail'
                test_data.response = response
                html_report.fail_num = html_report.fail_num + 1
        else:
            test_data.result = 'Error'
            test_data.response = {}
            html_report.error_num = html_report.error_num + 1
            return  
        if {} == response:
            test_data.result = 'Error'
            test_data.response = {}
            html_report.error_num = html_report.error_num + 1
            return    
           
                


    def tearDown(self):
        pass
    
def saveresponse(index,response):
    if sheet1.row_values(index)[10]:
        key = json.loads(sheet1.row_values(index)[10])
        if key:
            try:
                for i in key:
                    saveparamas = response[i]
                    save.update({i:saveparamas})
            except Exception:
                print "返回结果中没有要保存的请求值:"+key
    return save




# 获取测试套件
def get_test_suite(index):
    test_suite = unittest.TestSuite()
    method = sheet1.row_values(index)[3] # 根据选择的用例，获取对应的测试用例方法
    test_suite.addTest(TestInterfaceCase(method))
    return test_suite

# 运行测试用例函数
def run_case(sheet, runner):
    
    html_report.case_total = 0

    if run_mode == True:  # 暂时定为只运行全部用例，以后需要运行部分用例再进行修改
        
#         try:
            # 获取用例个数
            test_case_num = sheet.nrows
        
            # 循环执行测试用例
            for index in range(1, test_case_num):
                test_data.name=sheet.row_values(index)[2]
#                 time.sleep(0.5)
                print "开始执行第"+str(index)+"用例:"+test_data.name
                print "--------------------------------------"
                
                test_data.url = sheet.row_values(index)[4]
                url = basehttp.BaseHttp().get_host() + test_data.url
                print "请求地址为："+url
                print "--------------------------------------"
                #请求参数的拼接
                test_data.params = {}
                
                #把固定参数添加到请求参数中
                try:
                    if sheet.row_values(index)[5]:
                        test_data.fixparams = json.loads(sheet.row_values(index)[5])   
                        test_data.params.update(test_data.fixparams)
                except Exception:
                    print "固定参数一栏所填的参数有问题"+test_data.fixparams
                    
                #读取配置文件中的数据库配置。从数据库中取数据，分为59和48两个服务器的数据库
                test_data.sqlresult = {}
                try:
                    if sheet.row_values(index)[6]:
                        test_data.sqlparamas = json.loads(sheet.row_values(index)[6],strict=False)
                        for i in test_data.sqlparamas:
                            data = db.connectmysql(dbhost, test_data.sqlparamas[i])
                            for j in data:
                #暂时写死，填写时把sql结果as result
                                result = str(j['result'])
                                
                                test_data.sqlresult.update({i:result})
                #如果含有从数据库读取的参数 则添加到请求参数中
                    test_data.params.update(test_data.sqlresult)
                except Exception:
                    print "数据库中读取参数一栏所填的参数有问题,具体参数为："+sheet.row_values(index)[6]
                
                test_data.uniresult = {}    
                try:
                    if sheet.row_values(index)[7]:
                        test_data.uniparamas = json.loads(sheet.row_values(index)[7])
                        for i in test_data.uniparamas:
                            test_data.uniresult.update({i:random.randint(1,1000000000000)})
                    test_data.params.update(test_data.uniresult)
                except Exception:
                    print "唯一值一栏所填写的参数有问题,具体参数为:"+sheet.row_values(index)[7]
                    
                #关联之前所存储的参数
                if sheet.row_values(index)[8]:
                    test_data.relatparams = json.loads(sheet.row_values(index)[8])
                    try:
                        for i in test_data.relatparams:
                            test_data.relatresult = {i:test_data.savelist[i]}
                            test_data.params.update(test_data.relatresult)
                    except Exception:
                        print "存储的参数有问题，当前存储参数为"+json.loads(test_data.savelist)
                        print "当前所需关联的参数为:"+i
                    
            
                test_data.expected_result = sheet.row_values(index)[11]
                test_suite = get_test_suite(index)
                runner.run(test_suite)
                test_data.savelist = saveresponse(index,test_data.response)
                sheet1.put_cell(index, 4 ,1, url, 0)
                sheet1.put_cell(index, 5, 1, json.dumps(test_data.params), 0)
                sheet1.put_cell(index, 9, 1, json.dumps(test_data.response,ensure_ascii=False), 0)
                sheet1.put_cell(index, 10, 1, test_data.result, 0)
                sheet1.put_cell(index, 13, 1, test_data.time,0)
                html_report.case_total = html_report.case_total + 1    # 测试用例数加1  
                



# 运行测试套件
if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # 记录测试开始时间
    start_time = time.time()

    runner = unittest.TextTestRunner()
    html_report = HtmlReport()

    # # 读取用例数据
    excel = xlrd.open_workbook(r'createaftersale.xlsx')
    sheet1 = excel.sheet_by_index(0)
    run_case(sheet1, runner)
    # 测试结束时间
    end_time = time.time()
    html_report.time_caculate(end_time - start_time)  # 计算测试消耗时间

    # 生成测试报告
    html_report.generate_html('test report', sheet1, 'report.html')