import scrapy
from scrapy_splash import SplashRequest 
from ..items import SplashquotesItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/js/']
    
    def start_requests(self): 
        yield SplashRequest(self.start_urls[0], self.parse, 
            endpoint='render.html', 
            args={'wait': 10}, 
        )

    def parse(self, response):
        self.logger.debug("This is the parse page func")
        for sect in response.xpath('//div[@class="quote"]'):
            item = SplashquotesItem()
            item["text"] = sect.xpath('span[@class="text"]/text()').get()
            item["author"] = sect.xpath('span/small[@class="author"]/text()').get()
            tags = ''
            for t in sect.xpath('div[@class="tags"]/a/text()').extract():
                tags = tags + ' ' + t if len(tags) else t
            item['tags'] =  tags            
            item["url"] = response.url
            self.logger.info(item)
            yield item
            
        hh = response.xpath("//li[@class='next']/a/@href").extract()        
        if len(hh):
            self.logger.debug(hh[0])
            u = response.urljoin(hh[0])
            self.logger.debug('*****next url********: ' + u)                    
            # end copy
            #yield response.follow(url=u, callback=self.parse) 
            
            yield SplashRequest(response.urljoin(u), self.parse, 
                endpoint='render.html', 
                args={'wait': 1}, 
            )           
