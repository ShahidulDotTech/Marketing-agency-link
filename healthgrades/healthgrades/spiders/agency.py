import scrapy
from scrapy.loader import ItemLoader
from healthgrades.items import HealthgradesItem
from scrapy_playwright.page import PageMethod 

# make the header elements like they are in a dictionary
def get_headers(s, sep=': ', strip_cookie=True, strip_cl=True, strip_headers: list = []) -> dict():
    d = dict()
    for kv in s.split('\n'):
        kv = kv.strip()
        if kv and sep in kv:
            v=''
            k = kv.split(sep)[0]
            if len(kv.split(sep)) == 1:
                v = ''
            else:
                v = kv.split(sep)[1]
            if v == '\'\'':
                v =''
            # v = kv.split(sep)[1]
            if strip_cookie and k.lower() == 'cookie': continue
            if strip_cl and k.lower() == 'content-length': continue
            if k in strip_headers: continue
            d[k] = v
    return d

# spider class
class DoctorSpider(scrapy.Spider):
    name = 'agency'
    allowed_domains = ['clutch.co']
    url = 'https://clutch.co/us/agencies/digital-marketing?page={}'

# change the header of bot to look like a browser
    def start_requests(self):
        h = get_headers(
            '''
            accept: */*
            accept-encoding: gzip, deflate, br
            accept-language: en-US,en;q=0.9
            origin: https://clutch.co
            referer: https://clutch.co/
            sec-ch-ua: ".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"
            sec-ch-ua-mobile: ?0
            sec-ch-ua-platform: "Windows"
            sec-fetch-dest: empty
            sec-fetch-mode: cors
            sec-fetch-site: cross-site
            user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36
            x-hubspot-messages-uri: https://clutch.co/us/agencies/digital-marketing?page=1
            '''
        )

        for i in range(1, 508): # Change the range to the page numbers. more improvement can be done
            # GET request. url to first page
            yield scrapy.Request(self.url.format(i), headers =h, meta=dict(
                playwright = True,
                playwright_include_page = True,
                playwright_page_methods =[PageMethod('wait_for_selector', 'a.website-link__item')] # for waiting for a particular element to load 
            )) 

    def parse(self, response):
        boxes = response.css('li.provider.provider-row')
        for box in boxes:

            l = ItemLoader(item  = HealthgradesItem(), selector = box)

            l.add_css('name', 'h3.company_info a')
            l.add_css('href', 'a.website-link__item::attr(href)')
            l.add_css('project_size', 'div.list-item.custom_popover:nth-child(1) span)
            l.add_css('rate', 'div.list-item.custom_popover:nth-child(2) span)
            l.add_css('project_size', 'div.list-item.custom_popover:nth-child(3) span)
            l.add_css('project_size', 'div.list-item.custom_popover:nth-child(4) span)


            yield l.load_item()












