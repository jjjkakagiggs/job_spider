# -*- coding: utf-8 -*-
import time
import random

import scrapy
from scrapy.shell import inspect_response
from scrapy import Request
from ..items import JobSpiderItem
import datetime as dt



class QcwyspiderSpider(scrapy.Spider):
    name = 'qcwySpider'
    allowed_domains = ['appapi.51job.com']

    keyword = '数据分析'
    current_page = 1
    max_page = 100

    start_urls = ['https://appapi.51job.com/api/job/search_job_list.php?postchannel=0000&&keyword=' + str(keyword) +
                  '&keywordtype=2&jobarea=000000&searchid=&famoustype=&pageno=1&pagesize=30&accountid=97932608&key'
                  '=a8c33db43f42530fbda2f2dac7a6f48d5c1c853a&productname=51job&partner=8785419449a858b3314197b60d5'
                  '4d9c6&uuid=6b21f77c7af3aa83a5c636792ba087c2&version=845&guid=bbb37e8f266b9de9e2a9fbe3bb81c3d0']

    headers = {
        'Accept': 'text / html, application / xhtml + xml, application / xml;',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'appapi.51job.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }

    def parse(self, response):
        """
                通过循环的方式实现一级页面翻页，并采集jobid构造二级页面url
                :param response:
                :return:
        """
        print('------------'+ str(self.current_page) + '--------------------')

        items = response.xpath('//item')
        for item in items:
            jobid = item.xpath('./jobid/text()').extract_first()
            url = '''https://appapi.51job.com/api/job/get_job_info.php?jobid={}&accountid=&key=&from=searchjoblist&jobtype=0100&productname=51job&partner=8785419449a858b3314197b60d54d9c6&uuid=6b21f77c7af3aa83a5c636792ba087c2&version=845&guid=bbb37e8f266b9de9e2a9fbe3bb81c3d0'''.format(jobid)
            yield Request(url=url,headers=self.headers,callback=self.parse_job)

        if self.current_page < self.max_page:
            self.current_page += 1
            next_page_url = '''https://appapi.51job.com/api/job/search_job_list.php?postchannel=0000&&keyword=Python&keywordtype=2&jobarea=000000&searchid=&famoustype=&pageno=1{}&pagesize=30&accountid=97932608&key=a8c33db43f42530fbda2f2dac7a6f48d5c1c853a&productname=51job&partner=8785419449a858b3314197b60d54d9c6&uuid=6b21f77c7af3aa83a5c636792ba087c2&version=845&guid=bbb37e8f266b9de9e2a9fbe3bb81c3d0'''.format(self.current_page)
            yield scrapy.Request(url=next_page_url, headers=self.headers, callback=self.parse)


    def parse_job(self, response):
        # inspect_response(response, self)
        today = dt.date.today()
        today = today.strftime('%Y-%m-%d')
        item = JobSpiderItem()
        item['jobid'] = response.xpath('/responsemessage/resultbody/jobid/text()').extract_first()
        item['jobname'] = response.xpath('/responsemessage/resultbody/jobname/text()').extract_first()
        item['coname'] = response.xpath('/responsemessage/resultbody/coname/text()').extract_first()
        item['issuedate'] = response.xpath('/responsemessage/resultbody/issuedate/text()').extract_first()
        item['degree'] = response.xpath('/responsemessage/resultbody/degree/text()').extract_first()
        item['cityname'] = response.xpath('/responsemessage/resultbody/cityname/text()').extract_first()
        item['funtypename'] = response.xpath('/responsemessage/resultbody/funtypecode/text()').extract_first()
        item['workyear'] = response.xpath('/responsemessage/resultbody/workyear/text()').extract_first()
        item['providesalary']  = response.xpath('/responsemessage/resultbody/providesalary/text()').extract_first()
        item['jobinfo']  = response.xpath('/responsemessage/resultbody/jobinfo/text()').extract_first()
        item['url'] = response.xpath('/responsemessage/resultbody/share_url/text()').extract_first()
        item['collect_date'] = today

        yield item

