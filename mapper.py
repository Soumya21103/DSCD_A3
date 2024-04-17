import os
import math
import grpc
from grpc_modules import mapper_pb2
from grpc_modules import mapper_pb2_grpc
from concurrent import futures


def map(centroids, points, R):
    intermediate_output = []
    for p in points:
        distance = []
        for c in range(len(centroids)):
            x1 = p[0]
            y1 = p[1]
            x2 = centroids[c][0]
            y2 = centroids[c][1]
            distance.append((c, math.pow(x1-x2, 2) + math.pow(y1-y2, 2)))
        closest_centroid = min(distance, key=lambda x: x[1])
        intermediate_output.append((closest_centroid[0], (p, 1)))

    partition(intermediate_output, R)

def partition(inter, R):
    global id
    node_dir = f"M{id}"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    node_dir = os.path.join(script_dir, f"M{id}")
    os.makedirs(node_dir, exist_ok=True)

    K = set()
    for j in inter:
        K.add(j[0])
        partition = j[0] % R
        partition_file = os.path.join(node_dir, f"partition_{partition+1}.txt")

        if partition not in partitioned_data.keys():
            with open(partition_file, "w") as file:
                file.write(f"{j}\n")
            partitioned_data[partition] = [j]
        else:
            with open(partition_file, "a") as file:
                file.write(f"{j}\n")
            partitioned_data[partition].append(j)

    # If R>K, create empty files for the extra partitions
    if R>len(K):
        k = len(K)+1
        while k <= R:
            partition_file = os.path.join(node_dir, f"partition_{k}.txt")
            with open(partition_file, "w") as file:
                file.write(f"")
            partitioned_data[k-1] = []
            k+=1


    
class MapperServer(mapper_pb2_grpc.MapperServicer):
    def __init__(self):
        self.indices = []
        self.input_file = ""
        self.centroids_file = ""
        self.centroids = []
        self.points = []
        self.R = 0

    def StartMapper(self, request, context):
        self.R = request.R
        self.indices = list(request.indices)
        self.input_file = request.input_file
        self.centroids_file = request.centroids_file
        all_points = points_from_file(self.input_file)

        self.centroids = points_from_file(self.centroids_file)
        self.points = [all_points[i] for i in mapper_server.indices]

        return mapper_pb2.StartMapperResponse(success=True)

    def GetPartition(self, request, context):
        partition_index = request.partition_index
        if partition_index in partitioned_data:
            partition_items = partitioned_data[partition_index]
            response = mapper_pb2.MapperResponse()
            for item in partition_items:
                partition_item = response.items.add()
                partition_item.index = item[0]
                partition_item.point.x = item[1][0][0]
                partition_item.point.y = item[1][0][1]
                partition_item.count = item[1][1]
            return response
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Partition not found")
            return mapper_pb2.MapperResponse()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mapper_pb2_grpc.add_MapperServicer_to_server(MapperServer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()

def points_from_file(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    points = [tuple(map(float, line.strip().split(','))) for line in lines]
    return points

port = "50051"
# change assignment of ID after adding to worker.py
id = 1
partitioned_data = {} 

mapper_server = MapperServer()
while not mapper_server.indices or not mapper_server.input_file or not mapper_server.centroids_file:
    pass

map(mapper_server.centroids, mapper_server.points, mapper_server.R)
serve()