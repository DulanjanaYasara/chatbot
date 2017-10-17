from ete2 import Tree

words = ["reel", "road", "root", "curd", "curl", "whatever", "whenever", "wherever"]

# Creates a empty tree
tree = Tree()
tree.name = ""
# Lets keep tree structure indexed
name2node = {}
# Make sure there are no duplicates
words = set(words)
# Populate tree
for wd in words:
    # If no similar words exist, add it to the base of tree
    target = tree
    print wd

    # Find relatives in the tree
    for pos in xrange(len(wd), -1, -1):
        print pos
        root = wd[:pos]
        print root
        if root in name2node:
            target = name2node[root]
            break

    # Add new nodes as necessary
    fullname = root
    for letter in wd[pos:]:
        print letter
        fullname += letter
        new_node = target.add_child(name=letter, dist=1.0)
        name2node[fullname] = new_node
        print name2node
        target = new_node

# Print structure
print tree.get_ascii()
# You can also use all the visualization machinery from ETE
# (http://packages.python.org/ete2/tutorial/tutorial_drawing.html)
# tree.show()

# You can find, isolate and operate with a specific node using the index
wh_node = name2node["whe"]
print wh_node.get_ascii()


# You can rebuild words under a given node
def recontruct_fullname(node):
    name = []
    while node.up:
        name.append(node.name)
        node = node.up
    name = ''.join(reversed(name))
    return name


for leaf in wh_node.iter_leaves():
    print recontruct_fullname(leaf)
