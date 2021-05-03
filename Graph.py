class Graph:
    def __init__(self, n) :
        self.numVert = n

        self.adjList = []

        for x in range(n): 
            dictionary = {}
            self.adjList.append(dictionary)


    def getSize(self):
        return self.numVert


    def hasEdge(self, u, v):
        dictionary = self.adjList[u]
        if v in dictionary:
            return True
        else:
            return False


    def getWeight(self, u, v):
        boolean = self.hasEdge(u , v)
        if boolean: 
            dictionary = self.adjList[u]
            return dictionary[v]
        else: 
            return -1


    def addEdge(self, u, v, weight):
        if not self.hasEdge(u,v) and int(weight) > 0:
            dictionary = self.adjList[u]
            dictionary[v] = weight
            self.adjList[u] = dictionary


    def outNeighbors(self, u):
        dictionary = self.adjList[u]
        return list(dictionary.keys())




