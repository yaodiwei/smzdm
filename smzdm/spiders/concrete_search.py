# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
from scrapy import cmdline

from smzdm.items import SmzdmItem
from smzdm.pipelines import SmzdmPipeline


class ConcreteSearchSpider(scrapy.Spider):
    # 爬虫的名字
    name = 'concrete_search'

    # value:SmzdmItem
    SmzdmItemList = []

    def __init__(self):
        # 1.搜索的商品名称
        feed = ['奶粉']
        # 2.需要搜索的页数，一页为20个商品
        pages = 5
        # 3.过滤条件
        # 3.1表示商品的『值』数量必须 >= zhi_yes_limit
        zhi_yes_limit = 5
        # 3.2表示商品的『不值』数量必须 <= zhi_no_limit
        zhi_no_limit = -1
        # 3.3表示商品的『值』除以『不值』的比率必须 >= zhi_no_limit
        zhi_ratio_limit = -1
        # 3.4表示商品的『收藏』数量必须 >= start_limit
        start_limit = -1
        # 3.5表示商品的『评论』数量必须 >= comment_limit
        comment_limit = -1
        # 3.6需要排除的关键字
        exclude = ['婴儿', '幼儿', '宝宝']

        SmzdmPipeline.zhi_yes_limit = zhi_yes_limit
        SmzdmPipeline.zhi_no_limit = zhi_no_limit
        SmzdmPipeline.zhi_ratio_limit = zhi_ratio_limit
        SmzdmPipeline.start_limit = start_limit
        SmzdmPipeline.comment_limit = comment_limit
        SmzdmPipeline.exclude = exclude

        for index, f in enumerate(feed):
            feed[index] = parse.quote(f)
        self.start_urls = ['http://search.smzdm.com/?c=home&s=%s&p=%d&v=a' % (y, x) for x in range(1, pages + 1) for y
                           in feed]

    def parse(self, response):
        selector_feed_main_list = response.selector.xpath('//*[@id="feed-main-list"]')[0]
        selector_list_feed_main_list = selector_feed_main_list.xpath('./li')
        for selector in selector_list_feed_main_list:
            selector_item = selector.xpath('./div/div[2]')
            # 过滤文章
            if len(selector_item.xpath('./div[2]/div[2]/div/div/a')) == 0 or len(
                    selector_item.xpath('./h5/a[2]/div/text()')) == 0:
                print(
                    "发现一篇资讯 : 获取%s个赞，名字如下" % selector_item.xpath('./div[2]/div[1]/span[1]/span[1]/text()')[0].extract())
                print(selector_item.xpath('./h5/a[1]/text()')[0].extract())
                continue
            item = SmzdmItem()

            item['id'] = int(selector_item.xpath('./div[2]/div[1]/span[1]/span[1]/@data-article')[0].extract())
            item['title'] = selector_item.xpath('./h5/a[1]/text()')[0].extract().strip()
            if len(selector_item.xpath('./h5/a[2]/div/text()')) != 0:
                item['price'] = selector_item.xpath('./h5/a[2]/div/text()')[0].extract()
            desc_text_count = len(selector_item.xpath('./div[1]/text()').extract())
            if desc_text_count == 1 or selector_item.xpath('./div[1]/text()').extract()[0].strip() != '':
                item['desc'] = selector_item.xpath('./div[1]/text()')[0].extract().strip()
            elif desc_text_count >= 2 and selector_item.xpath('./div[1]/text()').extract()[1].strip() != '':
                item['desc'] = selector_item.xpath('./div[1]/text()')[1].extract().strip()
            if len(selector_item.xpath('./div[2]/div[1]/span[1]/span[1]/span[1]/span/text()')) != 0:
                item['zhi_yes'] = int(selector_item.xpath('./div[2]/div[1]/span[1]/span[1]/span[1]/span/text()')[
                    0].extract())
                item['zhi_no'] = int(selector_item.xpath('./div[2]/div[1]/span[1]/span[2]/span[1]/span/text()')[0].extract())
            item['start'] = int(selector_item.xpath('./div[2]/div[1]/span[2]/span/text()')[0].extract())
            # 待优化 item['comment'] = selector.xpath('./div[2]/div[1]/a/text()')[0].extract()
            item['comment'] = int(selector_item.xpath('./div[2]/div[1]/a/@title')[0].extract().split(' ')[1])
            item['time'] = selector_item.xpath('./div[2]/div[2]/span/text()')[0].extract().strip()
            item['channel'] = selector_item.xpath('./div[2]/div[2]/span/span/text()')[0].extract().strip()
            item['detail_url'] = selector.xpath('./div/div[1]/a/@href')[0].extract().strip()
            item['url'] = selector_item.xpath('./div[2]/div[2]/div/div/a/@href')[0].extract()
            item['img'] = selector.xpath('./div/div[1]/a/img/@src')[0].extract()
            # print(item)
            ConcreteSearchSpider.SmzdmItemList.append(item)
            yield item
        # print(ConcreteSearchSpider.SmzdmItemList)


if __name__ == "__main__":
    name = 'concrete_search'
    cmd = 'scrapy crawl {0}'.format(name)
    cmdline.execute(cmd.split())
