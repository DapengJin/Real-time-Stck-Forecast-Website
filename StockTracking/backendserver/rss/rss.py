# author: Chengtian Liu
import feedparser


def feed(ticker: str):
    rss_url = 'http://finance.yahoo.com/rss/headline?s=' + ticker
    # get rss
    feeds = feedparser.parse(rss_url)
    rss = dict()

    # rss title
    rss['title'] = feeds['feed']['title']
    # rss link
    rss['link'] = feeds['feed']['link']
    # rss subtitle
    rss['sub title'] = feeds['feed']['subtitle']
    # number of articles
    # print(feeds)
    n = len(feeds['entries'])
    rss['number'] = n
    rss['article'] = [dict() for i in range(n)]

    for i in range(n):
        rss['article'][i]['index'] = i
        rss['article'][i]['title'] = feeds['entries'][i]['title']
        rss['article'][i]['link'] = feeds['entries'][i]['link']
        rss['article'][i]['date'] = feeds['entries'][i]['published_parsed']
        rss['article'][i]['summary'] = feeds['entries'][i]['summary']

    return rss


# if __name__ == '__main__':
#     print(feed('AMZN'))