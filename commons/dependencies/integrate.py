from dependencies import generate
from main import CoreNLP
from map import distance


def best_ans(core_nlp, question, answer_list):
    """
    Choose the best answer index, out of given answer list according to the question
    :param question: string
    :type answer_list: list
    :type core_nlp: CoreNLP
    """
    distances = {}
    q_dependencies = list(generate(core_nlp.parse(question)))
    print q_dependencies
    for index, value in enumerate(answer_list):
        a_dependencies = list(generate(core_nlp.parse(value)))
        print a_dependencies
        distances[index + 1] = distance(q_dependencies, a_dependencies)

    print distances
    min_dist = min(distances.values())
    return [k for k, v in distances.iteritems() if v == min_dist]


def test():
    dependency_parse = CoreNLP()
    q_text = '''How to use REST endpoints to trigger messages in ESB?'''
    a_text = ['''You can make sure that sensitive information about the server is not revealed in error messages, 
    by customizing the error pages in your product. For instructions, see Customizing Error Pages in the WSO2 
    Administration Guide.''', '''You can send and receive RESTful messages through the the ESB profile using the HTTP 
    and HTTPS transports (other transports such as the Local transport are not supported). The following topics 
    describe the various scenarios for using REST. 
    ''', '''In the Users list, click Delete next to the user you want to delete, and then click Yes to confirm the 
    operation. Related Topics. See Configuring User Stores for instructions on how to configure primary and secondary 
    user stores.''', '''Yes. For information, contact us.''', '''A task runs a piece of code triggered by a timer, allowing 
    you to run scheduled jobs at specified intervals. A task can be scheduled in the following ways: Using count and 
    interval attributes to run the task a specified number of times at a given interval. Giving the scheduled time as a 
    cron style entry. Making the task run only once after WSO2 EI starts by using the once attribute. Having deployed a 
    task implementation to the ESB profile (see Writing Tasks), you can use the WSO2 EI Management Console to add a task 
    to the "Tasks" list and schedule various instances of the task. You can use either UI configuration  or XML 
    configuration to add and schedule tasks. ''']
    print best_ans(dependency_parse, q_text, a_text)


if __name__ == '__main__':
    test()
