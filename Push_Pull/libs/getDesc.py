from BeautifulSoup import BeautifulSoup
import urllib2


def get_desc(url):
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    return soup.find('span', attrs={"class": "hasCaption"}).text
