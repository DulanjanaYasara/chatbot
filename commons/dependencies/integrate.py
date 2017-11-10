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
    q_dependencies = list(generate(core_nlp.parse(question)))
    for index, value in enumerate(answer_list):
        a_dependencies = list(generate(core_nlp.parse(unidecode(value))))
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
    q_text2 = '''What is Enterprise Integrator? '''
    a_text2 = ['''WSO2 Enterprise Integrator (WSO2 EI) is a comprehensive integration solution that enables
    communication among various, disparate applications. Instead of having your applications communicate directly
    with each other in all their various formats, each application simply communicates with WSO2 EI, which acts
    mainly as an ESB to handle transforming and routing the messages to their appropriate destinations. The WSO2 EI
    product can be used to manage short-running, stateless integration flows (using the ESB profile) as well as
    long-running, stateful business processes (using the Business Process profile). The product also includes a
    separate Analytics profile for comprehensive monitoring, a Message Broker profile (WSO2 MB) that can be used for
    reliable messaging, as well as the WSO2 MSF4 j profile, which you can use to run microservices for your
    integration flows. The ESB profile in WSO2 EI provides its fundamental services through an event-driven and
    standards-based messaging engine (the bus), which allows integration architects to exploit the value of messaging
    without writing code. This ESB profile is a step ahead of the previous releases of WSO2 Enterprise Service Bus,
    as it provides data integration capabilities within the same runtime.''',
               '''In this guide, we have shown how each pattern in the patterns catalog can be simulated using various
             constructs in the ESB profile of WSO2 Enterprise Integrator (EI) . Click on a topic in the list below for
             details.''',
               '''If you have not done so already, download the latest version of WSO2 Enterprise Integrator. Extract
               the archive file to a dedicated directory for WSO2 Enterprise Integrator, which will hereafter be
               referred to as <EI_HOME>.''']
    q_text = '''How to change the default database? '''
    a_text = ['''Note that the Message Broker profile in WSO2 EI contains a default broker-specific database in
    addition to the Carbon database. You can change the default database configurations in each of the EI profiles by
    setting up new physical databases, and updating the relevant configurations in each profile. We recommend the use
    of an industry-standard RDBMS such as Oracle, PostgreSQL, MySQL, MS SQL, etc. when you set up your production
    environment. For information on setting up a new database for your profile, see Setting up the Physical Database
    in the WSO2 Administration Guide. Add the database drivers to the <EI_HOME>/lib/directory when setting up the
    database.''',
              '''To change the default database configurations for WSO2 DAS, see Working with Databases.''']

    print best_ans(dependency_parse, q_text, a_text)


if __name__ == '__main__':
    test()
