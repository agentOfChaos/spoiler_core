import random
import argparse
from threading import Thread
from urllib import request

from bs4 import BeautifulSoup, NavigableString



class SpoilerCore:

    tropepages = [
        "http://tvtropes.org/pmwiki/pmwiki.php/GameOfThrones/TropesAToB",
        "http://tvtropes.org/pmwiki/pmwiki.php/GameOfThrones/TropesCToD",
        "http://tvtropes.org/pmwiki/pmwiki.php/GameOfThrones/TropesEToF",
        "http://tvtropes.org/pmwiki/pmwiki.php/GameOfThrones/TropesGToK",
        "http://tvtropes.org/pmwiki/pmwiki.php/GameOfThrones/TropesLToO",
        "http://tvtropes.org/pmwiki/pmwiki.php/GameOfThrones/TropesPToS",
        "http://tvtropes.org/pmwiki/pmwiki.php/GameOfThrones/TropesTToZ"
    ]

    def __init__(self, maxwords=50):
        self.maxwords = maxwords
        self._crawlers = []
        self.reload_all_spoilers()

    def getRandomSpoiler(self):
        return random.choice(self.spoilers)

    def handleNewSpoiler(self, result):
        self.spoilers.append(result)

    def genReq(self, url):
        return request.Request(url)

    def reload_all_spoilers(self):
        self.spoilers = []
        self.completion = 0
        for link in self.tropepages:
            self.parse_tvtropes_link(link)
        for t in self._crawlers:
            t.join()

    def parse_tvtropes_link(self, url):
        t = Thread(target=self._parse_tvtropes_link, args=(url,))
        self._crawlers.append(t)
        t.start()

    def _parse_tvtropes_link(self, url):
        req = request.Request(url)
        with request.urlopen(req) as page:
            raw = page.read()
            self.htmlparser(raw)

    def htmlparser(self, code):
        def hasSpoiler(tag):
            return tag.find("span", class_="spoiler") is not None

        def recursivePrintout(tag):
            ret = ""
            for child in tag.descendants:
                if isinstance(child, NavigableString):
                    ret += child.string
            return ret.strip()

        soup = BeautifulSoup(code, "lxml")
        bullets = soup.find_all("li")
        for bullet in bullets:
            if hasSpoiler(bullet):
                spoilertxt = recursivePrintout(bullet)
                if len(spoilertxt.split(" ")) < self.maxwords or self.maxwords == 0:
                    self.spoilers.append(spoilertxt)


def parsecli():
    parser = argparse.ArgumentParser(description="GOT spoiler generator")
    parser.add_argument('-m','--max-words', help='Maximum spoiler length (number of words) (0: no limit)', type=int, default=50)
    return parser.parse_args()


if __name__ == "__main__":
    cli = parsecli()
    core = SpoilerCore(maxwords=cli.max_words)
    print(core.getRandomSpoiler())
