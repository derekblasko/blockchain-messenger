import sys
from node import node

if __name__ == "__main__":
    
    ip = sys.argv[1]
    port = int(sys.argv[2])
    api_port = int(sys.argv[3])
    key_file = None
    if len(sys.argv) > 4:
        key_file = sys.argv[4]
    peer = sys.argv[5]
    peer_port = sys.argv[6]
    
    Node = node(ip, port, key_file)
    Node.start_p2p(peer, peer_port)
    
    Node.start_api(api_port)
    
  


    