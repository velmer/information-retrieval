# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from ri_lab_01.settings import DEADLINE
from datetime import datetime

class RiLab01DeadlinePipeline(object):

    def process_item(self, item, spider):
        date_str_format = '%d/%m/%Y %H:%M:%S'
        item_datetime = datetime.strptime(item.get('date'), date_str_format)
        deadline_datetime = datetime.strptime(DEADLINE, date_str_format)
        if (item_datetime < deadline_datetime):
            raise DropItem("Expired deadline (%s) for %s" % (item.get('date'), item.get('url')))
        return item

class RiLab01TextFilterPipeline(object):

    def process_item(self, item, spider):
        ads_separator = '\r\n'
        text_index = 0
        item['text'] = item['text'].split(ads_separator)[text_index]
        return item
