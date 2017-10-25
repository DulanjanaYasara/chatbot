from zss import Node


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
            node.addkid(Node(x))
        else:
            node.addkid(tree_generate(x, dependency_list, visited_list))
        visited_list += [x]
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


def distance(q_dependency_list, a_dependency_list):
    """Used to find the edit distance of the dependency trees generated for the answer and the question
    :type a_dependency_list: list
    :type q_dependency_list: list
    """
    q_trees = [tree(q) for q in q_dependency_list if q]
    a_trees = [tree(a) for a in a_dependency_list if a]

    dist = 0
    for q_dep in q_trees:
        for a_dep in a_trees:
            dist += distance(a_dep, q_dep)
    return dist


def test():
    dependencies = [[[(0, u'root', 'R'), (3, u'add', u'V')], [(6, 'task', u'N'), (5, u'schedule', u'V')],
                     [(3, u'add', u'V'), (6, 'task', u'N')], [(3, u'add', u'V'), (8, 'esb', u'N')]]]
    a = [[[(0, u'root', 'R'), (3, u'run', u'V')], [(3, u'run', u'V'), (2, 'task', u'N')],
          [(3, u'run', u'V'), (5, 'piece', u'N')], [(5, 'piece', u'N'), (7, 'code', u'N')],
          [(5, 'piece', u'N'), (8, u'trigger', u'V')], [(8, u'trigger', u'V'), (11, 'timer', u'N')],
          [(5, 'piece', u'N'), (13, u'allow', u'V')], [(13, u'allow', u'V'), (14, u'you', u'P')],
          [(16, u'run', u'V'), (14, u'you', u'P')], [(13, u'allow', u'V'), (16, u'run', u'V')],
          [(16, u'run', u'V'), (18, 'job', u'N')], [(21, 'interval', u'N'), (20, u'specify', u'V')],
          [(16, u'run', u'V'), (21, 'interval', u'N')]]]
    print distance(dependencies, a)


if __name__ == "__main__":
    test()
