from time import time

from unidecode import unidecode

from dependencies import generate
from main import CoreNLP
from map import find_score


def best_ans(core_nlp, question, answer_list):
    """Choose the best answer index, out of given answer list according to the question

    :type question: string
    :type answer_list: list
    :type core_nlp: CoreNLP
    """
    scores = {}
    start_time = time()
    q_dependencies = list(generate(core_nlp.parse(question)))
    elapsed_time = time() - start_time
    print 'Time taken to create q dependencies :', elapsed_time
    for index, value in enumerate(answer_list):
        start_time = time()
        a_dependencies = list(generate(core_nlp.parse(unidecode(value))))
        elapsed_time = time() - start_time
        print 'Time taken to create a dependencies :', elapsed_time
        scores[index + 1] = find_score(q_dependencies, a_dependencies)

    print 'Scores :', str(scores)

    min_scores = min(scores.values())
    return [k for k, v in scores.iteritems() if v == min_scores]


def test():
    dependency_parse = CoreNLP()
    q_text1 = '''What is a Failover group? '''
    a_text1 = ['''A Failover Group is a list of leaf endpoints grouped together for the purpose of passing an incoming 
        message from one endpoint to another if a failover occurs. The first endpoint in failover group is considered
        the primary endpoint. An incoming message is first directed to the primary endpoint, and all other endpoints
        in the group serve as back-ups. If the primary endpoint fails, the next active endpoint is selected as the
        primary endpoint, and the failed endpoint is marked as inactive. Thus, failover group ensures that a message
        is delivered as long as there is at least one active endpoint among the listed endpoints.''',
               '''An endpoint is a specific destination for a message such as an address, WSDL, a failover group,
               a load-balance group etc. WSO2 API Manager has support for a range of different endpoint types, allowing the
               API Gateway to connect with advanced types of backends. It supports HTTP endpoints, URL endpoints (also
               termed as address endpoint), WSDL endpoints, Failover endpoints, Load-balanced endpoints. For more
               information about endpoints, see Working with Endpoints.''',
               '''For example, the device_management tag is used to group all the device management APIs including those
               that belong to the device type APIs. To know about the available tags and the APIs grouped under each tag,
               go to the API Cloud Store, click on the available tags in the left side panel. The response: The cURL request
               will be as follows if your username is example@wso2.com, the organization is wso2, and the password is
               123456.''',
               '''The following page is opened by clicking Failover Group in the Add Endpoint tab of the Manage Endpoints
               page. Enter a name for the failover group endpoint, and if you want to add any properties, click Add Property
               and specify the properties. To add a child endpoint to the failover endpoint, click Add Child ,
               and then select the required endpoint type from the list. Do the following: Enter the basic details for the
               child endpoint, such as the name and address. '''
               ]
    q = '''Can I use BPMN instead of BPEL via the Business Process profile? '''
    a = ['''The Business Process Profile supports both BPMN and BPEL.''']
    print best_ans(dependency_parse, q, a)


if __name__ == '__main__':
    test()
