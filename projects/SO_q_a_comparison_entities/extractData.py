import re

from bs4 import BeautifulSoup


def extractall(html):
    """Extracting the text from the HTML and checking whether there are codes or blockquotes"""
    soup = BeautifulSoup(html, 'lxml')

    # Obtaining the code segments from the body
    codes = [c.get_text() for c in soup('code')]
    errors = [e.get_text() for e in soup('blockquote')]

    has_codes = False
    for code in codes:
        if list(code).count('\n') > 1:
            has_codes = True

    has_errors = False
    for error in errors:
        if list(error).count('\n') > 1:
            has_errors = True

    # Check whether the HTML has codes or blockquotes
    has_codes_errors = has_codes or has_errors

    data = list(soup.recursiveChildGenerator())
    visit_to_a = False
    output = ''

    # Working with the hyperlink and images with links
    for value in data:
        if value.name == 'a':
            visit_to_a = True
            output += value.text
            if hasattr(value, 'href') and value.text != value['href']:
                output += ' [' + value['href'] + '] '

        elif value.name is None and not visit_to_a:
            output += value
        else:
            visit_to_a = False

    # Converting HTML entities into Unicode characters
    output = unicode(output)

    return output, has_codes_errors


def find_urls(text):
    """Find the urls in a given text and returns urls and text without the urls"""
    criteria = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    text_without_urls = re.sub(criteria, '', text)
    urls = re.findall(criteria, text)

    return text_without_urls, urls


    # htmll = '''<p>I could get some response like this.</p> <pre><code>"    {"name":"vesselStatus","type":"string",
    # "value":"S","scope":"global"},</code></pre>''' print extractall(htmll)

    # text = '''A registry is a content store and metadata repository. WSO2 Enterprise Integrator provides a registry
    #  with a built-in repository that stores the configurations and the configuration metadata. These configurations
    #  and artifacts define your messaging architecture. You can also use an external registry/repository for
    # resources such as WSDLs, schemas, scripts, XSLT and XQuery transformations, etc.\nFor more details please refer
    #   https://docs.wso2.com/display/ADMIN44x/Working+with+the+Registry\nWSO2 ESB tooling is used to create and
    # manage WSO2 ESB artifacts. WSO2 ESB tooling can be used to build the artifacts into a Composite Archive (CAR)
    # file, which can be used to deploy the artifacts into the ESB. \nFor more details please refer
    # https://docs.wso2.com/enterprise-integrator/WSO2+Enterprise+Integrator+Tooling\nAAAAAAAAAAAAAAAAA
    # \nXXXXXXXXXXXXXXXXX\nFor message transformations, use the XSLT mediator, PayloadFactory mediator,
    # For-Each mediator, and Enrich mediator. Message transformation includes scenarios such as XML to JSON
    # conversions, JSON to XML conversions, XML format transitions etc.\nFor more details please refer
    # http://docs.wso2.com/enterprise-integrator/Message+Transformations\nDeploying a Composite Application Archive (
    # also known as a CApp or .car file) can be done in four ways: Via the Tooling interface, via the management
    # console, via hot deployment and by using the Maven plugin. \nFor more details please refer
    # https://docs.wso2.com/display/ADMIN44x/Deploying+Composite+Applications+in+the+Server ''' print find_urls(text)
