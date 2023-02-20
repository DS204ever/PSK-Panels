import socket
from multiprocessing import Process
import time

udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def udp_client():
    while True:
        udp_client_socket.sendto("My message".encode(), ("255.255.255.255", 8080))
        time.sleep(1)
    
def udp_server():
    udp_server_socket.bind(("",8081))
    message, addr = udp_server_socket.recvfrom(1024)
    print(message, addr)


if __name__ == '__main__':
    client_process = Process(target=udp_client)
    server_process = Process(target=udp_server)
    client_process.start()
    server_process.start()
    server_process.join()
    client_process.terminate()