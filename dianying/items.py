# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class DianyingItem(Item):
    title = Field()
    type = Field()
    score1 = Field()
    score2 = Field()
    director = Field()
    starring = Field()
    zone = Field()
    showtime = Field()
    movie_long = Field()
    story = Field()
    image_urls = Field()
    images = Field()
    download = Field()
    size = Field()
