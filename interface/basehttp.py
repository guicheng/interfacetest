#!/usr/bin/env python
# -*- coding:utf-8 -*-

import ConfigParser
import json
# BaseHttp类
class BaseHttp:
    
    def __init__(self):
        config = ConfigParser.ConfigParser()
        # 从配置文件中读取接口服务器IP、域名，端口
        config.read('ini_file.ini')
        self.host = config.get('DEFAULT','host')
        self.header = eval(config.get('DEFAULT','header'))
    def set_host(self, host):
        self.host = host

    def get_host(self):
        return self.host

    def set_header(self,header):
        self.header = header
        
    def get_header(self):
        return self.header

