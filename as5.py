'''
Data Mining
Assignment 5, Graph Clustering by k-Core Decomposition
Myeong suhwan

'''

from datetime import datetime
import time

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
    inputfile = 'assignment5_input.txt' #! sys
    #inputfile = 'test_input.txt'
    output_filename = 'output.txt'
    graph = getDataFromFile(inputfile)
    start_time = datetime.now()
    
    k=2
    isChanged = True

    while isChanged:
        isChanged = False
        del_list = []    
        
        for v in graph:
            #print(v ," ::", graph[v])
            if len(graph[v]) <= k:
                del_list.append(v)
                isChanged = True
        for d in del_list:
            #print(d)
            del graph[d] #* delete vertex

        for d in del_list:
            for v in graph:
                if d in graph[v]:
                    print(d," is deleted in ", graph[v])
                    graph[v].remove(d) #* delete edge
                    print("result = ", graph[v])
                    


    graph = dict(sorted(graph.items(),key=lambda x : len(x[1]), reverse=True))
    
    for v in graph:
        print(v ," ::", len(graph[v]),graph[v]) #* Degree
 
    cluster = list()
    
    print("Graph is made")
    for v in graph:
        node_set = set()
        node_set.add(v) #*(1)
        node_set = GetNeighbors(graph,vertex=v,node_set=node_set) #*(2)
        #print(node_set)
        cluster.append(node_set)


    
    #* Eliminate redundant case
    index = 0
    j_index = 0

    while index < len(cluster):
        v = cluster[index]
        #print("=====================")
        #print("v : ", v)
        j_index = 0
        while j_index < len(cluster):
            #print("j_index",j_index)
            
            if index == j_index:
                j_index += 1
                continue
            if j_index >= len(cluster):
                break    

            u = cluster[j_index]
            #print("u : ", u)
            if v == u:
                #print("v:", v)
                #print(u," is deleted")
                cluster.remove(u)
                j_index -= 1
            
            j_index += 1
        index += 1
                


     
    i=0
    for v in cluster:
        if not v:
            continue
        print("cluster",i,v)
        print("\n\n")
        i +=1   
    

    #* Clustering
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
                    print(" = = = = = = == = == = == = = ")
                    # print(len(cluster[i]),"cluster i: ",cluster[i])
                    # print(len(cluster[j]),"cluster j: ",cluster[j])
                    print("intersection : ",cluster[i].intersection(cluster[j]))
                    cluster[i] = cluster[i].union(cluster[j])
                    cluster[j] = set()
                    isChanged = True
                    # print(len(cluster[i]),"union=>>",cluster[i])
    
    i=0
    for v in cluster:
        if not v:
            continue
        print("cluster",i,v)
        print("\n\n")
        i +=1   



    # new_cluster = list()
    # redundant_set = set()
    # is_Changed = True

    
    # num = 0

    # while is_Changed:
    #     num += 1
    #     print("num : ",num)
    #     is_Changed = False

    #     index = 0
    #     while index < len(cluster):
    #         v = cluster[index]
    #         result = set()
    #         j_index = 0
    #         if index in redundant_set:
    #             index += 1
    #             continue
    #         while j_index < len(cluster):
    #             #print("j" ,j_index)
    #             if index == j_index:
    #                 j_index += 1
    #                 continue
    #             if j_index >= len(cluster):
    #                 break
    #             if j_index in redundant_set:
    #                 j_index += 1
    #                 continue

    #             u = cluster[j_index]
    #             #print("u : ", u)
    #             if v.intersection(u):
    #                 #print("intersection : ",v.intersection(u))
                    
    #                 is_Changed = True
    #                 result = result.union(v.union(u))
                        
                    
    #                 redundant_set.add(j_index)
                    
            
    #             j_index += 1
    #         #print(result)
    #         new_cluster.append(result)
    #         index += 1








    # i=0
    # for v in new_cluster:
    #     if not v:
    #         continue
    #     print("cluster",i,v)
    #     print("\n\n")
    #     i +=1




    print("[+] Time Elapsed : ", datetime.now() - start_time, "microseconds")




    output_to_file(output_filename,cluster)
    

if __name__ == '__main__':
    main()