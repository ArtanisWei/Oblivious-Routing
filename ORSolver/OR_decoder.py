nodeCnt = 0
edgeCnt = 0
edgeList = []
orMat = []

pathList = []
MINN = 0.0000001

graphFile = "topology.txt"
orFile = "orStrategy.txt"
pathFile = "orPath.txt"

def loadGraph(fileIn):
    with open(fileIn, "r") as f:
        data = f.readline().split()
        global nodeCnt, edgeCnt, edgeList
        nodeCnt = int(data[0])
        edgeCnt = int(data[1])
        edgeList = [[0 for i in range(3)] for j in range(edgeCnt)]
        for i in range(edgeCnt):
            data = f.readline().split()
            edgeList[i][0] = int(data[0])
            edgeList[i][1] = int(data[1])
            edgeList[i][2] = int(data[2])
        for i in range(edgeCnt):
            edge = [ edgeList[i][1], edgeList[i][0], edgeList[i][2] ]
            edgeList.append(edge)
        edgeCnt = edgeCnt * 2
    return

def loadOR(fileIn):
    with open(fileIn, "r") as f:
        for line in f.readlines():
            num = float(line)
            orMat.append(num)
    return

def DFS(tar, path, flow):
    global MINN
    now = path[-1]
    if (flow < MINN):
        return
    if (now == tar):
        pathList.append([])
        for node in path:
            pathList[-1].append(node)
        pathList[-1].append(flow)
        return
    
    for i in range(edgeCnt):
        if (flow < MINN):
            break
        if (edgeList[i][0] != now):
            continue
        newflow = min(flowRemain[i], flow)
        if (newflow < MINN):
            continue
        flow -= newflow
        flowRemain[i] -= newflow
        path.append(edgeList[i][1])
        DFS(tar, path, newflow)
        del(path[-1])
    
def decodeOR(fileOut):
    global flowRemain, pathList
    num = 0
    flowRemain = [0 for i in range(edgeCnt)]
    f = open(fileOut, "w")
    
    for i in range(nodeCnt):
        for j in range(nodeCnt):
            if (i == j):
                continue
            pathList = []
            for l in range(0, edgeCnt):
                flowRemain[l] = orMat[num*edgeCnt + l]
            num = num + 1
            
            DFS(j, [i], 1.0)
            for path in pathList:
                for point in path:
                    print(point, end = " ", file = f)
                print("", file = f)
                
if __name__ == "__main__":
    loadGraph(graphFile)
    loadOR(orFile)
    decodeOR(pathFile)