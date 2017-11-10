import re
import urllib

from bs4 import BeautifulSoup


def __extract_all(html, is_doc):
    """Extracting the text from the HTML of the WSO2 documentation and removing the code segments"""
    # Adding '.' to the end of each list in HTML body
    modified_html = re.sub(r'(<\/(li|h\d|td|th)>)', r'.\1', html)
    soup = BeautifulSoup(modified_html, 'lxml')
    if is_doc:
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
                attr = value.get('href')
                urls.append(attr)
                if value.text != attr:
                    output += ' ' + value.text
        elif value.name is None and not visit_to_a:
            output += ' ' + value
        else:
            visit_to_a = False

    # Converting HTML entities into Unicode characters
    output = unicode(output)
    return output, urls


def get_data(url):
    """Getting data from the WSO2 doc content in web"""
    f = urllib.urlopen(url)
    myfile = f.read()
    soup = BeautifulSoup(myfile, 'lxml')
    if 'docs.wso2.com' in url:
        texts = soup.find('div', attrs={'class': 'wiki-content', 'id': 'main-content'})
        is_doc = True
    elif 'wso2.com/library' in url:
        texts = soup.find('div', attrs={'class': 'field-item even', 'property': 'content:encoded'})
        is_doc = False
    else:
        print '\033[1m' + 'Unidentified URL' + '\033[0m'
        return None
    data = __extract_all(str(texts), is_doc)[0]
    return data


def test():
    from commons.data.entity import Extractor

    url = "http://wso2.com/library/articles/2015/10/article-wso2-developer-studio-development-and-deployment-best" \
          "-practices/ "
    data = get_data(url)
    print data
    extractor = Extractor()
    print list(extractor.extract_entities(data))


if __name__ == "__main__":
    test()
