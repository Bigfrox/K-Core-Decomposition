'''
Data Mining
Assignment 5, Graph Clustering by k-Core Decomposition
Myeong suhwan
'''

from datetime import datetime
import sys

def getDataFromFile(filename):
    input_file = open(filename,'r')
    graph = dict()
    
    line = None
    line = input_file.readline().split()
    
    while line != "":
        
        if not line[0] in graph:
            graph[line[0]] = [line[1]]

        elif line[0] in graph:
            connected = graph[line[0]]
            connected.append(line[1])
            graph[line[0]] = list(set(connected))

        if not line[1] in graph:
            graph[line[1]] = [line[0]]

        elif line[1] in graph:
            connected = graph[line[1]]
            connected.append(line[0])
            graph[line[1]] = list(set(connected))
        

        line = input_file.readline().split()
        if not line:
            break
        
    
    return graph

def output_to_file(filename,cluster):
    file = open(filename, 'w')
    
    for v in cluster:
        if not v:
            continue
        file.write('{0} : {1}'.format(len(v),v))
        file.write("\n")
    file.close()

def GetNeighbors(graph,vertex,node_set):

    for r in graph[vertex]:
        node_set.add(r)

    
    return node_set




def main():
    #inputfile = 'assignment5_input.txt' #! sys
    #inputfile = 'test_input.txt'


    if len(sys.argv) != 2:
        print("No input file.")
        print("<Usage> as5.py assignment5_input.txt")
        return -1;
    
    inputfile = sys.argv[1]
    output_filename = 'output.txt'

    graph = getDataFromFile(inputfile)
    start_time = datetime.now()
    
    k=2

    isChanged = True
    while isChanged:
        isChanged = False
        del_list = []    
        
        for v in graph:
            
            if len(graph[v]) <= k:
                del_list.append(v)
                isChanged = True
        for d in del_list:
            
            del graph[d] #* delete vertex

        for d in del_list:
            for v in graph:
                if d in graph[v]:
                    #print(d," is deleted in ", graph[v])
                    graph[v].remove(d) #* delete edge
                    #print("result = ", graph[v])
                    


    graph = dict(sorted(graph.items(),key=lambda x : len(x[1]), reverse=True))
    
    #* Show degree of every node
    # for v in graph:
    #     print(v ," ::", len(graph[v]),graph[v])

    cluster = list()
    
    #* first of all, cluster with vertex and neighbors
    for v in graph:
        node_set = set()
        node_set.add(v) #*(1)
        node_set = GetNeighbors(graph,vertex=v,node_set=node_set) #*(2)
        
        cluster.append(node_set)


    
    #* Eliminate redundant case
    index = 0
    j_index = 0

    while index < len(cluster):
        v = cluster[index]
        
        j_index = 0
        while j_index < len(cluster):
            
            
            if index == j_index:
                j_index += 1
                continue
            if j_index >= len(cluster):
                break    

            u = cluster[j_index]
            
            if v == u:
                
                #print(u," is deleted")
                cluster.remove(u)
                j_index -= 1
            
            j_index += 1
        index += 1
                



    #* Merge two clusters if common neighbor is.
    isChanged = True
    while(isChanged):
        isChanged = False
        i=0
        j=0
        for i in range(len(cluster)):
            if not cluster[i]:
                continue
            for j in range(len(cluster)):
                if not cluster[j]:
                    continue

                if i>=j:
                    continue
                
                if cluster[i].intersection(cluster[j]):
                    # print(" = = = = = = == = == = == = = ")
                    # print(len(cluster[i]),"cluster i: ",cluster[i])
                    # print(len(cluster[j]),"cluster j: ",cluster[j])
                    # print("intersection : ",cluster[i].intersection(cluster[j]))
                    cluster[i] = cluster[i].union(cluster[j])
                    cluster[j] = set()
                    isChanged = True
                    # print(len(cluster[i]),"union=>>",cluster[i])
    
    #* show cluster number and nodes in the cluster
    i=0
    for v in cluster:
        if not v:
            continue
        print("cluster",i,v)
        print("\n\n")
        i +=1   

    print("[+] Time Elapsed : ", datetime.now() - start_time, "microseconds")

    #* save to output file with size : nodes in a cluster
    output_to_file(output_filename,cluster)
    

if __name__ == '__main__':
    main()