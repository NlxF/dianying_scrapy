#coding:utf-8

BOT_NAME = 'dianying'

SPIDER_MODULES = ['dianying.spiders']
NEWSPIDER_MODULE = 'dianying.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'dianying (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'scrapy.contrib.pipeline.images.ImagesPipeline': 100,
    'dianying.pipelines.DianyingPipeline': 200,
}

DOWNLOADER_MIDDLEWARES = {
    'dianying.random_user_agent.RandomUserAgentMiddleware': 400,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
}

IMAGES_STORE = 'D:\pycode\dianying\static\images'
IMAGES_EXPIRES = 90
# IMAGES_THUMBS = {
#     'small': (24, 24),
#     'big': (100, 150),
# }

#禁用cookie
COOKIES_ENABLED = False

# 250 ms of delay
DOWNLOAD_DELAY = 0.15
#AGENT
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36",
    "Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 ",
]

#Django相关
import sys,os
pro_dir = 'D:\pycode\dianying'
sys.path.append(pro_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'dianying.settings'

SECRET_KEY = '1jqkg@o5%r&=q+0cr_vw$=09%c%5^u_0#2--$a36-u-g^&194y'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dianying',
        'USER': 'root',
        'PASSWORD': 'toor',
        'HOST': '127.0.0.1'
    }
}