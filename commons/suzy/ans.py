import re

from commons.data.doc import get_data
from commons.data.entity import Extractor


def remove_default_intents(text):
    """Remove the unnecessary default intents"""
    criteria = re.compile(r'[XAIE]{4,}')
    new_text = re.sub(criteria, '', text)

    return new_text


def find_urls(text):
    """Find the urls in a given text and returns urls and text without the urls"""
    criteria = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    text_without_urls = re.sub(criteria, '', text)
    urls = re.findall(criteria, text)

    return text_without_urls, urls


def get_entities(extractor, bot_ans):
    """Getting the entities from the Bot  answer"""

    # Arranging the text and urls
    text_without_url = find_urls(bot_ans)[0]
    urls = find_urls(bot_ans)[1]
    # If default intents are encoded as XXXXX, AAAAA, IIIII and EEEEE ,they are removed
    text = remove_default_intents(text_without_url)

    print urls
    # Entity extraction from the text
    for en in extractor.extract_entities(text):
        yield en
    # Entity extraction from the urls
    for url in urls:
        try:
            data = get_data(url)
        except IOError:
            continue
        else:
            for en in extractor.extract_entities(data):
                yield en


def test():
    extractor = Extractor()

    bot_ans = """A fault sequence is a collection of mediators just like any other sequence, and it can be associated 
    with another sequence or a proxy service. When the sequence or the proxy service encounters an error during 
    mediation or while forwarding a message, the message that triggered the error is delegated to the specified fault 
    sequence. API development is usually done by someone who understands the technical aspects of the API, 
    interfaces, documentation, versions etc., while API management is typically carried out by someone who 
    understands the business aspects of the APIs. In most business environments, API development is a responsibility 
    that is distinct from API publication and management. WSO2 API Manager provides a simple Web interface names WSO2 
    API Publisher for API development and management, which is a structured GUI designed for API creators to develop, 
    document, scale, and version APIs, while also facilitating more API management-related tasks such as publishing 
    APIs, monetization, analyzing statistics, and promoting. You may require to map backend URLs to the pattern that 
    you want in the API Publisher. You may have dynamic backends which need to be resolved according to the request. 
    In such cases you need to implement URL mapping within API Manager. The URL pattern of the APIs in the Publisher 
    can be http://<hostname>:8280/<context>/<version>/<API resource>. You can define variables as part of the URI 
    template of your API's resources. For example, in the URI template /business/businessId/address/, businessId is a 
    variable. You can implement custom mediation flow and resolve these variables in mediation level. """

    print list(get_entities(extractor, bot_ans))


if __name__ == "__main__":
    test()
