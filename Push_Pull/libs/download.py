import os
from BeautifulSoup import BeautifulSoup
import urllib2


def download_videos(input_file, out_file):
    items = []

    with open(input_file, "r") as filer:
        urls = filer.readlines()
        urls = [rl.strip("\n") for rl in urls]
    print urls

    for url in urls:
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html)
        desc = soup.find('span', attrs={'class': 'hasCaption'}).text
        name = os.popen("you-get -i " + url + "-f -o " + out_file).readlines()[1][12:].replace("\n", "")
        items.append((name + ".mp4", name, desc))
        print "File: \"" + name + ".mp4\"\nName: \"" + name + "\" \nDesc: \"" + desc + "\"\n"

    return items
