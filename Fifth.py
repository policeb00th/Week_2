class WeightedBinHeap:
    
    def __init__(self):
        self.heapList = [{'key': 'head','weight':'None'}]
        self.currentSize = 0
        
    def percUp(self,i):
        while i // 2 > 0:
            if self.heapList[i]['weight'] < self.heapList[i//2]['weight']:
                tmp = self.heapList[i//2]
                self.heapList[i//2] = self.heapList[i]
                self.heapList[i] = tmp
            i = i // 2
            
    def insert(self,key,weight):
        d = {'key':key,'weight':weight}
        self.heapList.append(d)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)
        
    def minChild(self,i):
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i*2]['weight'] < self.heapList[i*2+1]['weight']:
                return i * 2
            else:
                return i * 2 + 1
    
    def percDown(self,i):
        while (i * 2) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapList[i]['weight'] > self.heapList[mc]['weight']:
                tmp = self.heapList[i]
                self.heapList[i] = self.heapList[mc]
                self.heapList[mc] = tmp
            i = mc
            
    def delMin(self):
        retNode = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        self.percDown(1)
        return retNode
    
    def buildHeap(self,list):
        i = len(list) // 2
        self.currentSize = len(list)
        new = WeightedBinHeap().heapList
        self.heapList = new + list
        while (i > 0):
            self.percDown(i)
            i = i - 1
            
###############################################        
class PriorityQueue:
    
    def __init__(self):
        self.wbh = WeightedBinHeap()
        
    def enqueue(self,key,weight):
        self.wbh.insert(key,weight)
        
    def dequeue(self):
        return self.wbh.delMin()
    
    def isEmpty(self):
        return self.wbh.currentSize == 0
    
    def decreaseKey(self,key,weight):
        i = 1
        while i < (self.currentSize() + 1):
            if self.wbh.heapList[i]['key'] == key:
                self.wbh.heapList[i]['weight'] = weight
                self.wbh.percUp(i)
            else:
                i = i + 1
        
       
    def loadPriorityQueue(self,list):
        self.wbh.buildHeap(list)
        
    def currentSize(self):
        return self.wbh.currentSize
    

###############################################
class Vertex:
    def __init__(self,key):
        self.id = key
        self.connectedTo = {}
        self.distance = float("inf")
        self.pred = None

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id)
#        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self,nbr):
        return self.connectedTo[nbr]
    
    def setDistance(self,distance):
        self.distance = distance
    
    def getDistance(self):
        return self.distance
    
    def setPred(self,node):
        self.pred = node

    def getPred(self):
        return self.pred

    
###############################################    
class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,t,cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def getVertices(self):
        return self.vertList.keys()
    
    def __iter__(self):
        return (x for x in self.vertList.values())

###############################################
def maze2graph(mazeArray):
    height = len(mazeArray)
    width = len(mazeArray[0])
    nodes = height * width
    graph = Graph()
# iterate across each row starting at top left
    for row in range(height):
        for col in range(width):
            position = col + row * width
# add each vertex, id consecutive number starting at top left
            graph.addVertex(position)
# add edges at adjacent nodes that are spaces
            if mazeArray[row][col] == ' ':
                if mazeArray[row-1][col] == ' ':
                    graph.addEdge(position, position-width,1)
                    graph.addEdge(position-width, position,1)
                if mazeArray[row][col-1] == ' ':
                    graph.addEdge(position, position-1,1)
                    graph.addEdge(position-1, position,1)
    return graph


def graph2KeyWeightList(self):
    l = []
    for k in self.getVertices():
        d = {}
        d['key'] = k
        d['weight'] = self.getVertex(k).getDistance()
        l.append(d)
    return l


def dijkstra(graph,start):
    startVertex = graph.getVertex(start)
    startVertex.setDistance(0)
    pq = PriorityQueue()
    keyDistList = graph2KeyWeightList(graph)
    pq.loadPriorityQueue(keyDistList)
    i = start
    while i < (pq.currentSize() + 1):
        key = pq.dequeue()['key']
        currentVert = graph.getVertex(key)
        print ("current vertex is ", key)
        for nextVert in currentVert.getConnections():
            print (nextVert)
            print (currentVert.getDistance())
            print (nextVert.getDistance())
            print (currentVert.getWeight(nextVert))
            newDist = currentVert.getDistance() + currentVert.getWeight(nextVert)
            print (newDist)
            if newDist < nextVert.getDistance():
                print ("update distance")
                nextVert.setDistance( newDist )
                print (nextVert.getDistance())
                nextVert.setPred(currentVert)
                print (nextVert.getPred())
# this next step is not working! I can get the node with the reduced weight
# to swap with its parent but the rest of the heap is not reordered.
                pq.decreaseKey(nextVert,newDist)
        i = i + 1
# print final list of vertices and distance
# to get path through maze list vertices by increasing distance
    for v in graph:
        print("%s, %s" % (v, v.getDistance()))

                        
maze = [['+' for i in range(7)], [' ',' ','+',' ',' ',' ','+'], \
        ['+',' ','+',' ','+','+','+'], ['+',' ',' ',' ','+',' ','+'], \
        ['+',' ','+',' ',' ',' ',' '], ['+' for i in range(7)]]

# print my maze
for i in range(len(maze)):
    print (' '.join(maze[i]))

g = maze2graph(maze)
dijkstra(g,7)
