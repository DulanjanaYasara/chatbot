from bs4 import BeautifulSoup


# import re

def extractall(html):
    """Extracting the text from the HTML and checking whether there are codes or blockquotes"""
    soup = BeautifulSoup(html, 'lxml')

    # Obtaining the code segments from the body
    codes = [c.get_text() for c in soup('code')]
    errors = [e.get_text() for e in soup('blockquote')]

    has_codes = False
    for code in codes:
        if list(code).count('\n') > 2:
            has_codes = True

    has_errors = False
    for error in errors:
        if list(error).count('\n') > 2:
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


def print_all(no_q_accepted_answers, no_given_bot):
    """Printing the efficiency of the bot w.r.t. Stackoverflow accepted answer questions"""
    print '___________________Process succeed___________________'
    print 'Number of questions with accepted answers :', no_q_accepted_answers
    print 'Number of questions given to the bot      :', no_given_bot
    print 'As a percentage                           :', round(no_given_bot / float(no_q_accepted_answers) * 100,
                                                               0), '%'

# TEST CASE
# htmll = '''
# <p>I could get some response like this.</p>
# <pre><code>"    {"name":"vesselStatus","type":"string","value":"S","scope":"global"},</code></pre>'''
# print extractall(htmll)
