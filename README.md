Python 采集Gameguyz首页数据并调用SNS(sina,tqq) API,使用BeautifulSoup,simplejson,bluga.

webthumb目录主要抓取网站URL并且生成图片

http://webthumb.bluga.net/home
 帐号信息同下
http://www.thumbalizr.com/
  Your User ID: deapge  
  Your Password: wezomem3z
  Your API-Key: 4d23ae20d040dbbd365e51829310bfd5
 
 
外部调用的时候,请调用 webthumb.py generateThumb()方法,生成图片

修改weibo/sinaweibo.py 
APP_KEY = '2631518870' # app key
APP_SECRET = 'da2e24628eda1a1812cae87f9c5cb5ed' # app secret
CALLBACK_URL = 'http://weibo.com/u/3364942534' # callback url