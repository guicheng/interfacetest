#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib
import json 
import requests

# 配置类
class ConfigHttp:
    '''用于封装http请求方法，http头设置'''

    def __init__(self, host,header):
        self.host = host
        self.headers = header  # http 头

#     封装HTTP GET请求方法
    def get(self, url, param):
        data =urllib.urlencode(param)  # 将参数转为url编码字符串
        url =  self.host + url  
        try:
            response = requests.get(url,params = data,headers=self.headers)
            responsetime = response.elapsed.total_seconds()
            if response.status_code == 200:
                print "get请求调用成功,请求参数为"+param
                print "--------------------------------------"
                
                return response.json(),responsetime
            else:
                print "get请求调用失败,请求参数为"+param
                print "--------------------------------------"
                
                return response.content,responsetime 
        except requests.exceptions.RequestException:
            print '没有返回结果，请检查接口'+param
            print "--------------------------------------"
            
            return None,responsetime

    # 封装HTTP POST请求方法
    def post(self, url, data):
        data = json.dumps(data)
        url =  self.host  + url 
        try:
            response = requests.post(url,data=data,headers=self.headers)
            responsetime = response.elapsed.total_seconds()
            if  response.status_code == 200:
                print "post接口调用成功,请求参数为:"+data
                print "--------------------------------------"
                return response.json(),responsetime
            else:
                print "post接口调用失败，请求参数为:"+data
                print "--------------------------------------"   
                return response.content(),responsetime             
        except requests.exceptions.RequestException:
            print('没有返回结果，请检查接口'+data)
            print "--------------------------------------"
            
            return None,responsetime

    # 封装HTTP xxx请求方法
    # 自由扩展