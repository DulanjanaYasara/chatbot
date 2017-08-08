import scrapy


class firstSpider(scrapy.Spider):
    name = "first"
    allowed_domains = ["stackoverflow.com"]
    start_urls = ["https://stackoverflow.com/search?q=%5Bwso2%5D%2C%5Bwso2esb%5D"]

    def prase(self, reponse):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
