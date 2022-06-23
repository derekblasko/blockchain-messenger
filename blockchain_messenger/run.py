from node import node


def create_node(ip, port, api_port, key_file):
    Node = node(ip, port, key_file)
    Node.start_p2p()
    Node.start_api(api_port)
    
