import scrapy

from scrapy.loader import ItemLoader

from ..items import NbfaeItem
from itemloaders.processors import TakeFirst


class NbfaeSpider(scrapy.Spider):
	name = 'nbfae'
	start_urls = [
		'https://nbf.ae/umbraco/surface/partials/pressreleases?page=1&nodeId=7680&keyword=&year=&language=en',
		'https://nbf.ae/umbraco/surface/partials/pressreleases?page=1&nodeId=7866&keyword=&year=&language=en'
	]

	def parse(self, response):
		post_links = response.xpath('//article/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@class="content"]/h1/text()').get()
		description = response.xpath('//div[@class="content"]//text()[normalize-space() and not(ancestor::ul | ancestor::h1 | ancestor::time | ancestor::a)]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="content"]//time/text()').get()

		item = ItemLoader(item=NbfaeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
