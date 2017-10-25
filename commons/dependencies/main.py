# -*- coding: utf-8 -*-
from pycorenlp import StanfordCoreNLP


class CoreNLP:
    """Used to initialize the Stanford Core NLP in servlet mode and then connect to it using a socket"""

    def __init__(self, timeout=15000, port=9000, buffer_size=4096):
        """Used to initialize the StanfordAPI object with the host, port and buffer"""
        # self.host = socket.gethostname()
        self.port = str(port)
        # self.timeout = str(timeout)
        # self.buffer = str(buffer_size)
        # self.process = Popen(
        #     args=['java', '-mx4g', '-cp', 'commons/corenlp/*', 'edu.stanford.nlp.pipeline.StanfordCoreNLPServer',
        #           '-port', self.port, '-timeout', self.timeout])
        # time.sleep(5)
        self.nlp = StanfordCoreNLP('http://localhost:' + self.port)

    def parse(self, text):
        output = self.nlp.annotate(text, properties={
            'annotators': 'tokenize,ssplit,pos,depparse,parse,coref',
            'coref.algorithm': 'neural',
            'outputFormat': 'json'
        })
        return output

        # def __del__(self):
        #     """ Terminating the process """
        #     self.process.terminate()


def test():
    """Test method for the Stanford API class"""
    dependency_parse = CoreNLP()
    text = '''Yes. For information, contact us.'''
    print(dependency_parse.parse(text))


if __name__ == "__main__":
    test()
