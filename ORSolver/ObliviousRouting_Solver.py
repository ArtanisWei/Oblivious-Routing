import gurobipy as gp
from gurobipy import GRB
import numpy as np

graphFile = "topology.txt"
orFile = "orStrategy.txt"

arcList = []
edgeCnt = 0
arcCnt = 0
nodeCnt = 0

def arcToEdge(arc):
    if (arc < edgeCnt):
        return arc
    return arc - edgeCnt

def eeToPi(i, j):
    return i * edgeCnt + j

def eijToP(e, i, j):
    return e * nodeCnt * nodeCnt + i * nodeCnt + j

def ijaToF(i, j, a):
    rank = i * (nodeCnt - 1) + j
    if (j > i):
        rank -= 1
    return rank * arcCnt + a 

def loadGraph(fileIn):
    with open(fileIn, "r") as f:
        data = f.readline().split()
        global nodeCnt, edgeCnt, arcCnt, arcList
        nodeCnt = int(data[0])
        edgeCnt = int(data[1])
        arcList = [[0 for i in range(3)] for j in range(edgeCnt)]
        for i in range(edgeCnt):
            data = f.readline().split()
            arcList[i][0] = int(data[0])
            arcList[i][1] = int(data[1])
            arcList[i][2] = int(data[2])
        #Reversed edge (arc)
        for i in range(edgeCnt):
            arc = [ arcList[i][1], arcList[i][0], arcList[i][2] ]
            arcList.append(arc)
        arcCnt = edgeCnt * 2
    return

def solveOR(fileOut):
    model = gp.Model('OR')
    flowCnt = nodeCnt * (nodeCnt-1) * arcCnt
    flowVar = []
    pCnt = edgeCnt * nodeCnt * nodeCnt
    pVar = []
    piCnt = edgeCnt * edgeCnt
    piVar = []
    r = model.addVar(0)

    for i in range(flowCnt):
        flowVar.append(model.addVar(0.0, 1.0, name=str(i) ))
    for i in range(pCnt):
        pVar.append(model.addVar(0.0, GRB.INFINITY))
    for i in range(piCnt):
        piVar.append(model.addVar(0.0, GRB.INFINITY))

    r = model.addVar(0, GRB.INFINITY, 0, GRB.CONTINUOUS, "r")
    model.setObjective(r, GRB.MINIMIZE)

    #CONS 0, the target
    for i in range(edgeCnt):
        A_ub = gp.LinExpr()
        for j in range(edgeCnt):
            A_ub += arcList[j][2] * piVar[ eeToPi(i,j) ]
        model.addConstr(A_ub <= r)

    #CONS 1, flowVar must be a routing
    for i in range(nodeCnt):
        for j in range(nodeCnt):
            if (i == j):
                continue
            for l in range(nodeCnt):
                Aside = gp.LinExpr()
                for arc in range(arcCnt):
                    if (arcList[arc][0] == l):    #Sub Out flow
                        Aside -= flowVar[ ijaToF(i,j,arc) ]
                    if (arcList[arc][1] == l):    #Add In flow
                        Aside += flowVar[ ijaToF(i,j,arc) ] 
                if (l == i):
                    model.addConstr(Aside == -1.0)
                if (l == j):
                    model.addConstr(Aside == 1.0)
                if ((l != j) and (l != i)):
                    model.addConstr(Aside == 0.0)

    #CONS 2, the pVBound
    for edge in range(edgeCnt):
        for i in range(nodeCnt):
            for j in range(nodeCnt):
                if (i == j):
                    continue
                Aside = gp.LinExpr()
                Bside = gp.LinExpr()
                Aside += flowVar[ ijaToF(i,j,edge) ] / arcList[edge][2]
                Aside += flowVar[ ijaToF(i,j,edge+edgeCnt) ] / arcList[edge][2]
                Bside += pVar[ eijToP(edge, i, j) ]
                model.addConstr(Aside <= Bside)
                
    #CONS3, the ARC RULE
    for edge in range(edgeCnt):
        for j in range(nodeCnt):
            for arc in range(arcCnt):
                Aside = gp.LinExpr()
                Aside += piVar[ eeToPi(edge, arcToEdge(arc)) ]
                Aside += pVar[ eijToP(edge, j, arcList[arc][0]) ]
                Aside -= pVar[ eijToP(edge, j, arcList[arc][1]) ]
                model.addConstr(Aside >= 0.0)
    
    #EXTRA CONS (These might be useless)
    for i in range(piCnt):
        model.addConstr(piVar[i] >= 0.0)
    for edge in range(edgeCnt):
        for i in range(nodeCnt):
            for j in range(nodeCnt):
                if (i == j):
                    model.addConstr(pVar[ eijToP(edge,i,j) ] == 0.0)
                else:
                    model.addConstr(pVar[ eijToP(edge,i,j) ] >= 0.0)
    
    model.optimize()
    print(model.objVal)
    with open(fileOut, "w") as f:        
        for i in range(flowCnt):
            num = model.getVarByName(str(i)).X
            print(num, file=f)

if __name__ == "__main__":
    loadGraph(graphFile)
    solveOR(orFile)