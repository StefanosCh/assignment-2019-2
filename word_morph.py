import sys
import Levenshtein

#BK Tree with extra attributes for A* search
class BKT(object):
    "Generic tree node."
    def __init__(self, children=None, word='',distance = None):
        self.distance = distance
        self.searchDistance = None
        self.searchPrev = None
        self.word= word
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.word

    def add_child(self, node):
        assert isinstance(node, BKT)
        self.children.append(node)

    def get_child(self,distance):
        for i in self.children:
            if i.distance == distance:
                return i
        return None

def BKInsert(bk,word):
    if bk == None :
        bk = BKT(word=word)
        return bk
    node=bk

    while node != None :
        node_word=node.word
        distance = Levenshtein.distance(node_word, word)
        parent = node
        node = node.get_child(distance)
        if node == None:
            parent.add_child(BKT(word=word,distance=distance))
            return bk

#Modified to return only r distance
def BKTreeSearch(bk, word, r):
    results=[]
    to_check=[]
    to_check.append(bk)
    while to_check.__len__() > 0:
        node = to_check.pop(0)
        node_word = node.word
        distance = Levenshtein.distance(node_word, word)
        if distance == r :
            results.append(node)
        l = distance - r
        h = distance + r
        children = node.children
        for child in children:
            d=child.distance
            if l <= d <= h :
                to_check.append(child)
    return results

def findMin(set):
    min = set.pop()
    for i in set :
        if i.searchDistance < min.searchDistance :
            min = i

    return min

def readDict(filename):
    with open(filename) as f:
        dict = []
        t = 1
        # read file
        while (t):
            t = f.readline().rstrip("\n")
            dict.append(t)
    #remove last line
    dict = dict[:len(dict)-1]
    # find max node
    return dict

def astar(bkt, start, target):
    visited = set()
    unvisited = set()
    start_node = BKTreeSearch(bkt,start,0)[0]

    start_node.searchDistance = 0

    node = start_node
    unvisited.add(start_node)
    while node.word != target:
        next_nodes=(BKTreeSearch(bkt,node.word,1))

        for i in visited:
            if i in next_nodes:
                next_nodes.remove(i)

        unvisited.update(next_nodes)

        for i in unvisited :
            tDistance = node.searchDistance + Levenshtein.distance(i.word, target)
            if i.searchDistance == None or tDistance < i.searchDistance:
                i.searchDistance = tDistance
                i.searchPrev = node
        unvisited.remove(node)
        visited.add(node)
        node = findMin(unvisited.copy())

    finallist=[]
    while node != None :
        finallist.append(node)
        node = node.searchPrev

    finallist.reverse()

    return finallist

dictionary_file = sys.argv[1]
start_word = sys.argv[2]
target_word = sys.argv[3]

dict = readDict(dictionary_file)
bk = None
for i in dict:
    bk = BKInsert(bk,i)

print(astar(bk,start_word,target_word))