import scrapy

class EbaygpuSpider(scrapy.Spider):
    name = "ebaygpu"
    #allowed_domains = ["www.ebay.com"]
    start_urls = ['https://www.ebay.com/sch/i.html?_from=R40&_nkw=GTX+1080+ti&_sacat=0&LH_BIN=1&rt=nc&LH_ItemCondition=3000']

    def parse(self, response):
        product_links = response.xpath('//a[@class="s-item__link"]/@href').getall()
        
        for url in product_links:
            yield scrapy.Request(url, callback=self.parse_page)
        
        next_page = response.xpath('//a[@aria-label="Go to next search page"]/@href').get()
        
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_page(self, response):
        product_title = response.xpath('//h1[@class="x-item-title__mainTitle"]/span/text()').get()
        
        product_price = response.xpath('//div[@class="x-price-primary"]/span/text()').get()
        
        product_image = response.xpath('//div[@class="ux-image-filmstrip-carousel"]//img/@src').getall()
        product_image = ' | '.join(product_image)
        
        product_specifics = response.xpath('//div[@class="ux-layout-section-module-evo"]//div[@class="ux-labels-values__labels"]')
        product_allspec = []
        for container in product_specifics:
            label = ''.join(container.xpath('.//text()').getall())
            value = ''.join(container.xpath('./following-sibling::div[1][@class="ux-labels-values__values"]//text()').getall())
            product_allspec.append(label + ' ' + value)
        product_allspec = ' | '.join(product_allspec)
        
        yield {
            'product_title': product_title,
            'product_price': product_price,
            'product_image': product_image,
            'product_allspec': product_allspec
        }