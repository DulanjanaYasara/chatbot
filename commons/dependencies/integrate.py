from dependencies import generate
from main import CoreNLP
from map import find_score


def best_ans(core_nlp, question, answer_list):
    """
    Choose the best answer index, out of given answer list according to the question
    :param question: string
    :type answer_list: list
    :type core_nlp: CoreNLP
    """
    scores = {}
    q_dependencies = list(generate(core_nlp.parse(question)))
    for index, value in enumerate(answer_list):
        a_dependencies = list(generate(core_nlp.parse(value)))
        scores[index + 1] = find_score(q_dependencies, a_dependencies)

    print scores
    min_scores = min(scores.values())
    return [k for k, v in scores.iteritems() if v == min_scores]


def test():
    dependency_parse = CoreNLP()
    q_text = '''How to define membershipHandler properties in Dynamic Load-balance Endpoint?'''
    a_text = ['''You can make sure that sensitive information about the server is not revealed in error messages, 
    by customizing the error pages in your product. For instructions, see Customizing Error Pages in the WSO2 
    Administration Guide.''', '''You can send and receive RESTful messages through the the ESB profile sing the HTTP 
    and HTTPS transports (other transports such as the Local transport are not supported). The following topics 
    describe the various scenarios for using REST. Using REST with a Proxy Service. Using REST with APIs. You can 
    also use the HTTP endpoint to define REST endpoints using URI templates similar to the REST API.''', '''A Failover 
    Group is a list of leaf endpoints grouped 
    together for the purpose of passing an incoming message from one endpoint to another if a failover occurs. The 
    first endpoint in failover group is considered the primary endpoint. An incoming message is first directed to the 
    primary endpoint, and all other endpoints in the group serve as back-ups. If the primary endpoint fails, 
    the next active endpoint is selected as the primary endpoint, and the failed endpoint is marked as inactive. 
    Thus, failover group ensures that a message is delivered as long as there is at least one active endpoint among 
    the listed endpoints. The Enterprise Integrator switches back to the primary endpoint as soon as it becomes 
    available. This behaviour is known as dynamic failover.''', '''You can specify membershipHandler properties using 
    the property elements. The policy attribute of the dynamic Load-balance element specifies the load-balancing policy 
    (algorithm) to be used for selecting the next member that will receive the message.''', '''I play.''']
    # q_text = '''How to add a scheduled task into ESB?'''
    # a_text = ['''A scheduled task to ESB can be added by doing this.''']
    print best_ans(dependency_parse, q_text, a_text)


if __name__ == '__main__':
    test()
