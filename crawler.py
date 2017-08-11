import urllib.request
from bs4 import BeautifulSoup


class PDF:
    def __init__(self, citation, url, short):
        self.citation = citation
        self.url = url
        self.short = short

    def __repr__(self):
        return self.url

    def __str__(self):
        return self.url

def getHTML(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    response = response.read().strip().decode('UTF-8')
    return response


def makePDFLinks(soup):
    links = []
    for link in soup.find_all('a'):
        href = str(link.get('href'))
        if (href.find('.pdf')) != -1:
            citation = link.parent.get_text()
            url = link.get('href')
            short = link.get_text().strip('"')
            links.append(PDF(citation, url, short))
    return links


def makeWikiLinks(soup):
    links = []
    for link in soup.find_all('a'):
        href = str(link.get('href'))
        if href.find('wiki') == 1 and href.find(':') == -1:
            links.append(href.split('/')[-1])
    return set(links)


def main():
    currentPage = 'jazz'
    fo = open(currentPage + '.html', 'w+')
    fo.write('<html>\n<body>\n<ul>')
    links = {}
    #currentPage = 'Astrology'
    currentPage = 'Jazz'
    url = "https://en.wikipedia.org/wiki/" + currentPage
    html = getHTML(url)
    soup = BeautifulSoup(html, 'html.parser')
    links[currentPage] = makePDFLinks(soup)
    setOfPages = makeWikiLinks(soup)
    traversedPages = set()

    for page in (setOfPages - traversedPages):
        print(page)
        url = "https://en.wikipedia.org/wiki/" + page
        try:
            html = getHTML(url)
            soup = BeautifulSoup(html, 'html.parser')
            links[page] = makePDFLinks(soup)
        except:
            print('FAILED FOR %s', page)
            pass
        traversedPages.add(page)

    keys = list(links.keys()).sort()
    for key in keys:
        print('writing ', key)
        fo.write('<li>' + key + '</li>')
        if len(links[key]) > 0:
            fo.write('<ul>\n')
            for link in links[key]:
                fo.write('<li><a href="' + str(link) + '">' + link.short + '</a></li>\n')
            fo.write('</ul>')
    fo.write('</ul>\n</body></html>')
    fo.close()


main()
