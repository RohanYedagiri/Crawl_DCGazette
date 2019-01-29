import scrapy

class DcGazetteSpider(scrapy.Spider):
    name = "dcgazette"
    
    #start_urls = ['https://dcgazette.com/2019/']
    
    def start_requests(self):
        url = 'https://dcgazette.com/'
        year = getattr(self, 'year', None)
        if year is not None:
            url = url + year + '/'
        yield scrapy.Request(url, self.parse)
    
    def parse(self, response):
        # follow links to articles pages
        for href in response.xpath('//article/header/h3/a/@href'):
            yield response.follow(href, self.parse_article)

        # follow pagination links
        for href in response.xpath('//a[@class="next page-numbers"]/@href'):
            yield response.follow(href, self.parse)
            
            
    def parse_article(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()
        def extract_text_with_xpath(query):
            return response.xpath(query).extract()

        yield {
            'Title': extract_with_xpath('//h1[@class="entry-title"]/text()'),
            'Locale': extract_with_xpath('//meta[@property="og:locale"]/@content'),
            'Desc': extract_with_xpath('//meta[@property="og:description"]/@content'),
            'Textdata': extract_text_with_xpath('//div[@class="entry-content clearfix"]/div/descendant::*/text()')
        }
        
        
        
# response.xpath('//meta[@property="og:locale"]/@content/text()')