import grpc_modules.master_pb2_grpc
import grpc_modules.master_pb2
import grpc
import numpy as np
 
import numpy as np
from scipy.spatial.distance import cdist 
 
#Function to implement steps given in previous section
def kmeansalgo(x,k, no_of_iterations):
    idx = np.random.choice(len(x), k, replace=False)
    #Randomly choosing Centroids 
    centroids = x[idx, :] #Step 1
     
    #finding the distance between centroids and all the data points
    distances = cdist(x, centroids ,'euclidean') #Step 2
     
    #Centroid with the minimum Distance
    points = np.array([np.argmin(i) for i in distances]) #Step 3
     
    #Repeating the above steps for a defined number of iterations
    #Step 4
    for _ in range(no_of_iterations): 
        centroids = []
        for idx in range(k):
            #Updating Centroids by taking mean of Cluster it belongs to
            temp_cent = x[points==idx].mean(axis=0) 
            centroids.append(temp_cent)
 
        centroids = np.vstack(centroids) #Updated Centroids 
         
        distances = cdist(x, centroids ,'euclidean')
        points = np.array([np.argmin(i) for i in distances])
         
    return points 

def main(itnum,old_response,status):
    input = ""
    with open("input.txt") as f:
        input += f.read()
    channel = grpc.insecure_channel('localhost:50051')
    stub = grpc_modules.master_pb2_grpc.MasterStub(channel)
    
    num_nodes = 5
    input = input.split(",")
    
    for i in range(num_nodes):
        request = grpc_modules.master_pb2.MapperRequest(inputData=input[2*i]+","+input[2*i+1])
        response = stub.Mapper(request)
        print(response)
    
    for i in range(num_nodes):
        request = grpc_modules.master_pb2.ReducerRequest(intermediateData=response)
        response = stub.Reducer(request)
        print(response)

    itnum +=1

    new_response = kmeansalgo(response)
    if new_response == old_response:
        status +=1

    if status == 2:
        print("Final output is: ",new_response)
        return
    
    old_response = new_response
    main(itnum,old_response,status)
    
itnum=0
old_response = None
status=0
main(itnum,old_response,status)