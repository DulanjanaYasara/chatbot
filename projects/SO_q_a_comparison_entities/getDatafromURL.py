import urllib

from bs4 import BeautifulSoup


def extractall(html):
    """Extracting the text from the HTML and removing the code segments"""
    soup = BeautifulSoup(html, 'lxml')
    [c.extract_entities() for c in soup.findAll('div', attrs={'class': 'code panel pdl conf-macro output-block'})]

    data = list(soup.recursiveChildGenerator())
    visit_to_a = False
    # URLs are saved separately for future use
    urls = []
    output = ''

    # Working with the hyperlink
    for value in data:
        if value.name == 'a':
            visit_to_a = True
            if hasattr(value, 'href'):
                urls.append(value['href'])
                if value.text != value['href']:
                    output += value.text
        elif value.name is None and not visit_to_a:
            output += ' ' + value
        else:
            visit_to_a = False

    # Converting HTML entities into Unicode characters
    output = unicode(output)

    return output, urls


def get_data_from_url(url):
    """Getting data from the WSO2 doc content in the web"""
    f = urllib.urlopen(url)
    myfile = f.read()
    soup = BeautifulSoup(myfile, 'lxml')
    texts = soup.find('div', attrs={'class': 'wiki-content', 'id': 'main-content'})

    data = extractall(str(texts))[0]
    return data

# link = 'https://docs.wso2.com/display/ADMIN44x/Deploying+Composite+Applications+in+the+Server'
# print get_data_from_url(link)
