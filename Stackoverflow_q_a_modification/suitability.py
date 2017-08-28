import re


def availability_codes(body):
    # Checks whether the body contains HTML tags or not
    regexph = re.compile(r'<(.*)>(.|\n)*?<\/(.*)>')
    # Checks whether the body contains Java code snippets
    regexpj = re.compile(r'{[^{}]{45,}}')
    # Checks whether body contains
    regexpa = re.compile(r'at(. +\.)')

    if regexph.search(body) or regexpj.search(body):
        return False
    else:
        return True
