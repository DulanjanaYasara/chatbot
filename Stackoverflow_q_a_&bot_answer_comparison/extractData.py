from bs4 import BeautifulSoup


# import re

def extractall(html):
    soup = BeautifulSoup(html, 'lxml', )
    data = list(soup.recursiveChildGenerator())
    visit_to_a = False
    output = ''

    for value in data:
        if value.name == 'a':
            visit_to_a = True
            output += value.text
            if hasattr(value, 'href') and value.text != value['href']:
                output += ' [' + value['href'] + '] '
        elif value.name is None and not visit_to_a:
            # visit_to_a = False
            output += value
        else:
            visit_to_a = False

    return output

    # def visible(element):
    #     if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
    #         return False
    #     # elif re.match('<!--.*-->', str(element)):
    #     #     return False
    #     else:
    #         return True
    #
    # result = filter(visible, data)
    # output = ''.join(result)
    # return output


    # htmll = ''' <p>I ain\'t able to login Nope - at least the cache won\'t return it</p> <p> The default token lifetime
    #  can be set in the <strong>identity.xml</strong> config file, see <a
    # href="https://docs.wso2.com/display/AM160/Working+with+Access+Tokens#WorkingwithAccessTokens-changeDef"
    # rel="nofollow noreferrer">the documentation</a> </p> ''' html='<p><a href="https://i.stack.imgur.com/BVXK5.png"
    # rel="nofollow noreferrer"><img src="https://i.stack.imgur.com/BVXK5.png" alt="enter image description
    # here"></a></p><p>In order to achieve this, you can simply create an API like below</p>' print extractall(htmll)
