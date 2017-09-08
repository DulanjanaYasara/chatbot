from data.text import EntityExtractor
from data.url import find_urls, get_data_from_url
from suzy import remove_default_intents


def get_entities(bot_ans):
    """Getting the entities from the Bot  answer"""

    # Arranging the text and urls
    text_without_url = find_urls(bot_ans)[0]
    urls = find_urls(bot_ans)[1]
    text = remove_default_intents(text_without_url)

    ans_entities = set()
    # Entity extraction from the text
    extractor = EntityExtractor()
    for en in extractor.extract(text):
        ans_entities.add(en.lower())
    # Entity extraction from the urls
    for url in urls:
        for en in extractor.extract(get_data_from_url(url)):
            ans_entities.add(en.lower())
    return ans_entities
