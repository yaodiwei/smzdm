# -*- coding: utf-8 -*-

import scrapy


class SmzdmItem(scrapy.Item):
    id = scrapy.Field()         #id
    title = scrapy.Field()      #标题
    price = scrapy.Field()      #价格
    desc = scrapy.Field()       #描述
    zhi_yes = scrapy.Field()    #点「值」的数量
    zhi_no = scrapy.Field()     #点「不值」的数量
    praise = scrapy.Field()     #文章「赞」的数量
    start = scrapy.Field()      #「收藏」的数量
    comment = scrapy.Field()    #「评论」的数量
    time = scrapy.Field()       #发布时间
    channel = scrapy.Field()    #购买渠道
    detail_url = scrapy.Field() #详情页面url
    url = scrapy.Field()        #商品链接
    img = scrapy.Field()        #商品图片

    def __str__(self):
        return 'SmzdmItem (%s) (%s) (值：%s) (%s)' % (self['title'], self['price'], self['start'], self['detail_url'])

    __repr__ = __str__
