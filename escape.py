"""

This file solves the 'Escape the ice problem.
The encoding of the pond needs to be given in a seperate file and the name of
that file should be given in FILENAME constant

"""
from graph import Graph
from vertex import Vertex

# Name of file
FILENAME = "test1.txt"

# No. of rows
ROW = 0

# No. of columns
COLUMN = 0

# Escape row.
ESCAPE = -1

# Graph representation of pond.
POND_GRAPH = Graph()

# Matrix with pond.
POND = []

# Queue for processing the vertices in graph.
PROCESS_Q = []

# Maximum value for the number of moves.
MAX_MOVES = 10000

def main(filename):
    """
    This method is the main method that calls other methods to solve the
    problem.
    :Pre: Encoded file is presesnt in correct location.
    :Post: Results are printed on the console.
    :param filename:
    :return:
    """
    read = readFile(filename)
    if read == 0:
        print("Inconsistency in data!")
        return
    buildGraphVertices()
    buildGraphEdges()
    initializeDistances()
    printResult()

def initializeDistances():
    """
    This method initializes the distances of the edges.
    :Pre: All the edges should be added.
    :Post: All the edges have proper distances
    :return:
    """
    while len(PROCESS_Q) > 0:
        current = PROCESS_Q[0]
        PROCESS_Q.remove(current)
        for vertex in POND_GRAPH.vertList.values():
            for connection in vertex.getConnections():
                if connection.id == current.id and vertex.distance > \
                                current.distance+1:
                    vertex.distance = current.distance+1
                    PROCESS_Q.append(vertex)

def buildGraphEdges():
    """
    This method initializes all the edges in the graph representation of the
    pond.
    :Pre: vertices have been all initialized.
    :Post: All the edges are added to the graph.
    :return:
    """
    global ROW, COLUMN, ESCAPE
    escapeVertex = POND_GRAPH.getVertex("ESC")
    foundRock = False
    for x in range(COLUMN-1, -1, -1):
        if not foundRock:
            element = POND[ESCAPE][x]
            if element == "*":
                foundRock = True
            else:
                currentVertex = POND_GRAPH.getVertex(str(x) + ":" + str(ESCAPE))
                currentVertex.distance = 1
                POND_GRAPH.addEdge(currentVertex.id, escapeVertex.id)
                PROCESS_Q.append(currentVertex)
    for x in range(0, ROW):
        for y in range(0, COLUMN):
            currentVertex = POND_GRAPH.getVertex(str(y)+":"+str(x))
            if currentVertex is not None and currentVertex.distance == MAX_MOVES:
                addEdges(currentVertex)


def addEdges(vertex):
    """
    This method adds proper edges to the graph representation of the pond.
    :Pre: Vertices have been initialized
    :Post: Edges are added properly based upon all movements from the vertex.
    :param vertex:
    :return:
    """
    vertex.visited = 1
    left = moveLeft(vertex)
    right = moveRight(vertex)
    up = moveUp(vertex)
    down = moveDown(vertex)
    if not left == False: POND_GRAPH.addEdge(vertex.id, left.id)
    if not right == False: POND_GRAPH.addEdge(vertex.id, right.id)
    if not up == False: POND_GRAPH.addEdge(vertex.id, up.id)
    if not down == False: POND_GRAPH.addEdge(vertex.id, down.id)

def moveLeft(vertex):
    """
    This method finds the next block of ice when we move in upward
    direction form a given vertex.
    :Pre: vertex is valid.
    :Post: correct block of ice is returned.
    :param vertex:
    :return:
    """
    global POND
    row = int(str(vertex.id).strip().split(":")[1])
    col = int(str(vertex.id).strip().split(":")[0])
    changed = False
    while col > 0 and POND[row][col-1] == ".":
        col -= 1
        changed = True
    if changed:
        leftVertex = POND_GRAPH.getVertex(str(col)+":"+str(row))
        return leftVertex
    else:
        return False


def moveRight(vertex):
    """
    This method finds the next block of ice when we move in rightward
    direction form a given vertex.
    :Pre: vertex is valid.
    :Post: correct block of ice is returned.
    :param vertex:
    :return:
    """
    global POND, COLUMN
    row = int(str(vertex.id).strip().split(":")[1])
    col = int(str(vertex.id).strip().split(":")[0])
    changed = False
    while col < COLUMN-1 and POND[row][col + 1] == ".":
        col += 1
        changed = True
    if changed:
        rightVertex = POND_GRAPH.getVertex(str(col) + ":" + str(row))
        return rightVertex
    else:
        return False

def moveUp(vertex):
    """
    This method finds the next block of ice when we move in upward
    direction form a given vertex.
    :Pre: vertex is valid.
    :Post: correct block of ice is returned.
    :param vertex:
    :return:
    """
    global POND
    row = int(str(vertex.id).strip().split(":")[1])
    col = int(str(vertex.id).strip().split(":")[0])
    changed = False
    while row > 0 and POND[row - 1][col] == ".":
        row -= 1
        changed = True
    if changed:
        upVertex = POND_GRAPH.getVertex(str(col)+":"+str(row))
        return upVertex
    else:
        return False

def moveDown(vertex):
    """
    This method finds the next block of ice when we move in downward
    direction form a given vertex.
    :Pre: vertex is valid.
    :Post: correct block of ice is returned.
    :param vertex:
    :return:
    """
    global POND, ROW
    row = int(str(vertex.id).strip().split(":")[1])
    col = int(str(vertex.id).strip().split(":")[0])
    changed = False
    while row < ROW-1 and POND[row+1][col] == ".":
        row += 1
        changed = True
    if changed:
        downVertex = POND_GRAPH.getVertex(str(col)+":"+str(row))
        return downVertex
    else:
        return False

def buildGraphVertices():
    """
    This method makes the vertices based upon the pond input for the graph
    representation of the pond.
    :Pre: Graph has been initialized.
    :Post: All the required vertices are initialized and inserted in the graph.
    :return:
    """
    global ROW, COLUMN, ESCAPE
    filedata = POND
    for x in range(0,len(filedata)):
        for y in range(0, COLUMN):
            if filedata[x][y] != "*":

                newVertex = Vertex(str(y)+":"+str(x),MAX_MOVES)

                if x == ESCAPE and filedata[x][COLUMN-1] != "*":
                    newVertex.distance = 1
                    newVertex.visited = 1
                POND_GRAPH.addVertex(newVertex)
                escapeVertex = Vertex("ESC", 0)
                escapeVertex.distance = 0
                escapeVertex.visited = 1
                POND_GRAPH.addVertex(escapeVertex)

def readFile(filename):
    """
    This method reads the file 'filename' and then stores the contents of
    that file into an array and returns that list.
    :Pre: The file is present in the directory. The format of file is correct.
    :Post: The list is returned with all the lines of the file. ROW, COLUMN
    and ESCAPE are initialized.
    :param filename: Name of the file to be read and stored.
    :return list with contents of the file:
    """
    global ROW, COLUMN, ESCAPE, MAX_MOVES
    try:
        data = [line.strip('\n') for line in open(filename)]
    except FileNotFoundError:
        print("that's not a file!")
        return
    oneLine = data[0].strip().split(" ")
    ROW = int(oneLine[0])
    COLUMN = int(oneLine[1])
    ESCAPE = int(oneLine[2])
    if ESCAPE > ROW-1:
        print("Escape point incorrect")
        return 0
    if len(data) != ROW+1:
        print("Inconsistency in no. of rows!!")
        return 0
    for x in range(1, len(data)):
        oneColumn = data[x].strip().split(" ")
        if len(oneColumn) != COLUMN:
            print("More columns!!")
            return 0
        POND.append(oneColumn)
    MAX_MOVES = ROW * COLUMN
    return 1

def printResult():
    """
    This method prints the result in required format using the graph.
    :Pre: The distances are initialized with correct values inside the graph
    :Post: The result is printed in proper format as required.
    :return: N/A
    """
    results = {}
    for x in POND_GRAPH.vertList.values():
        if x.distance not in results.keys():
            results[x.distance] = ["("+str(x.id).replace(":",",")+")"]
        else:
            results[x.distance].append("("+str(x.id).replace(":",",")+")")
    for x in results.keys():
        if x is not 0:
            if x == MAX_MOVES:
                print("NOT REACHABLE : "+str(results.get(x)))
            else:
                print(str(x)+" : "+str(results.get(x)))

if __name__ == "__main__":
    main(FILENAME)