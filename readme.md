# Oblivious Routing Solver in Python

This is a pure solver for Oblivious Routing, input the topology, output the strategy, as easy as ABC!

Thanks to the authors of this paper!
Dankon al la aŭtoroj de ĉi tiu artikolo!
https://ieeexplore.ieee.org/document/4032716


## About ObliviousRouting_Solver.py

ObliviousRouting_Solver.py reads the topology file, calculates OR, and prints it to startegy file.

### Format of input: ###

The first line is two integers M, N, the number of nodes and edges
For the next N lines, each line contains three **integers**: n1, n2, c, describe a **bidirectional** edge that connects n1 and n2 with maxinum capacity of c.

### Format of output: ###

The routing f in the paper.
Or you can run the OR_decoder.py to get a more intuitive explanation.

## About OR_decoder.py
It reads the topology, the strategy and caculates the path

### Format of output ###

Each line describe a path of OR strategy.
path[:-1] is the nodes in the path, and path[-1] is the split ratio of traffic from path[0] to path[-2]
