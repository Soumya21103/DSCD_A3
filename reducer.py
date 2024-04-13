


class ReduceeServicer(object):
    '''Reciever for all rpc'''
    pass

class Reducer:
    def __init__(self) -> None:
        pass
    
    def start_server(self):
        pass

    def stop_server(self):
        pass

    def get_reduce_partitions(self):
        pass

    def suffle_sort(self):
        pass

    def reduce_partition(self):
        pass

    def reduce(self):
        pass

    def send_results(self):
        pass

if __name__ == "__main__":
    server = Reducer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        server.stop_server()