# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem


class SmzdmPipeline(object):

    # 3.过滤条件
    # 3.1表示商品的『值』数量必须 >= zhi_yes_limit
    zhi_yes_limit = -1
    # 3.2表示商品的『不值』数量必须 <= zhi_no_limit
    zhi_no_limit = -1
    # 3.3表示商品的『值』除以『不值』的比率必须 >= zhi_no_limit
    zhi_ratio_limit = -1
    # 3.4表示商品的『收藏』数量必须 >= start_limit
    start_limit = -1
    # 3.5表示商品的『评论』数量必须 >= comment_limit
    comment_limit = -1
    # 3.6需要排除的关键字
    exclude = []


    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])

        if SmzdmPipeline.zhi_yes_limit > -1 and item['zhi_yes'] < SmzdmPipeline.zhi_yes_limit:
            raise DropItem("zhi_yes_limit: %d, target: %s" % (SmzdmPipeline.zhi_yes_limit, str(item)))
        if SmzdmPipeline.zhi_no_limit > -1 and item['zhi_no'] > SmzdmPipeline.zhi_no_limit:
            raise DropItem("zhi_no_limit: %d, target: %s" % (SmzdmPipeline.zhi_no_limit, item))
        if SmzdmPipeline.zhi_ratio_limit > -1 and (item['zhi_yes'] / item['zhi_no']) > SmzdmPipeline.zhi_ratio_limit:
            raise DropItem("zhi_ratio_limit: %d, target: %s" % (SmzdmPipeline.zhi_ratio_limit, item))
        if SmzdmPipeline.start_limit > -1 and item['zhi_start'] < SmzdmPipeline.zhi_start_limit:
            raise DropItem("zhi_start_limit: %d, target: %s" % (SmzdmPipeline.zhi_start_limit, item))
        if SmzdmPipeline.comment_limit > -1 and item['zhi_commen'] <= SmzdmPipeline.comment_limit:
            raise DropItem("zhi_comment_limit: %d, target: %s" % (SmzdmPipeline.zhi_comment_limit, item))
        if len(SmzdmPipeline.exclude) > 0 and SmzdmPipeline.containsKeyword(item['title']):
            raise DropItem("exclude: %s, target: %s" % (str(SmzdmPipeline.exclude), item))
        print("符合条件:" + str(item))
        return item

    @classmethod
    def containsKeyword(cls, title):
        for keyword in cls.exclude:
            if keyword in title:
                return True
        return False