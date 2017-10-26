from zss import Node
from zss import distance


def tree_generate(node_name, dependency_list, visited_list):
    """Generating a tree from the node name given
    :type visited_list: list
    :param node_name: str
    :type dependency_list: list
    """
    node = Node(node_name)
    visited_list += [node_name]
    kids = [x[1][1] for x in dependency_list if x[0][1] == node_name]
    for x in kids:
        if x in visited_list:
            node.value = 1
            node.addkid(Node(x))
        else:
            node.addkid(tree_generate(x, dependency_list, visited_list))
        visited_list += [x]

    else:
        if not Node.get_children(node):
            node.value = 1
        else:
            node.value += sum([x.value for x in Node.get_children(node)])
            # print node.label, node.value
    return node


def tree(dependency_list):
    """
    Generating a tree from the dependency list
    :type dependency_list: list
    """
    for value in dependency_list:
        if 'root' == value[0][1]:
            return tree_generate('root', dependency_list, [])
        else:
            print 'No root found !!!'


def find_score(q_dependency_list, a_dependency_list):
    """Used to find the edit distance of the dependency trees generated for the answer and the question
    :type a_dependency_list: list
    :type q_dependency_list: list
    """

    score = 0
    # score=[]
    for q_dep in q_dependency_list:
        print q_dep
        print'___________________________________________________________________________________________________'
        q_tree = tree(q_dep)
        q_entities = set(find_entities(q_dep))
        for a_dep in a_dependency_list:
            a_tree = tree(a_dep)
            a_entities = set(find_entities(a_dep))
            # Finding the edit distance
            # edit_distance = simple_distance(a_tree, q_tree)
            edit_distance = distance(a_tree, q_tree, get_children, insert_cost, remove_cost, update_cost)
            print a_dep
            print 'Edit distance :',
            print edit_distance
            # Finding common entities
            common = len(q_entities.intersection(a_entities))
            print common
            score += (common / float(edit_distance))
            # score.append(edit_distance)
    return min(score)


def find_entities(dependency_list):
    for dependency in dependency_list:
        yield dependency[1][1]


def get_children(node):
    return Node.get_children(node)


def insert_cost(node):
    # print 'insert',node.label, node.value, node.children
    return 4 * node.value


def remove_cost(node):
    # print 'remove',node.label,node.value,node.children
    return 1 * node.value


def update_cost(a, b):
    # If a and b are equal cost is 0
    if a == b:
        return 0
    else:
        # print 'update ',a,b
        return 2 * max(a.value, b.value)


def test():
    dependencies = [[[(0, u'root', 'R'), (3, u'add', u'V')], [(6, 'task', u'N'), (5, u'schedule', u'V')],
                     [(3, u'add', u'V'), (6, 'task', u'N')], [(3, u'add', u'V'), (8, 'esb', u'N')]]]
    # a = [[[(0, u'root', 'R'), (3, u'run', u'V')], [(3, u'run', u'V'), (2, 'task', u'N')],
    #       [(3, u'run', u'V'), (5, 'piece', u'N')], [(5, 'piece', u'N'), (7, 'code', u'N')],
    #       [(5, 'piece', u'N'), (8, u'trigger', u'V')], [(8, u'trigger', u'V'), (11, 'timer', u'N')],
    #       [(5, 'piece', u'N'), (13, u'allow', u'V')], [(13, u'allow', u'V'), (14, u'you', u'P')],
    #       [(16, u'run', u'V'), (14, u'you', u'P')], [(13, u'allow', u'V'), (16, u'run', u'V')],
    #       [(16, u'run', u'V'), (18, 'job', u'N')], [(21, 'interval', u'N'), (20, u'specify', u'V')],
    #       [(16, u'run', u'V'), (21, 'interval', u'N')]]]
    a = [[[(0, u'root', 'R'), (8, u'add', u'V')], [(3, 'task', u'N'), (2, u'schedule', u'V')],
          [(8, u'add', u'V'), (3, 'task', u'N')], [(3, 'task', u'N'), (5, 'esb', u'N')],
          [(8, u'add', u'V'), (7, u'be', u'V')], [(8, u'add', u'V'), (10, 'esb', u'N')],
          [(8, u'add', u'V'), (12, u'do', u'V')]]]

    # tree_generate('root', dependencies, [])
    print find_score(dependencies, a)


if __name__ == "__main__":
    test()
