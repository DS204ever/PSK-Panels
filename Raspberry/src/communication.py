import socket
import asyncio
import websocket
from multiprocessing import Process
import time, rel, json

websocket_ip = "192.168.1.65"
websocket_port = 8080

udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def udp_client():
    while True:
        udp_client_socket.sendto(
            "My message".encode(), ("255.255.255.255", 8080))
        time.sleep(1)


def udp_server():
    udp_server_socket.bind(("", 8081))
    message, addr = udp_server_socket.recvfrom(1024)
    print(message, addr)


def on_message(ws, message):
    jsonMessage = json.loads(message)
    match jsonMessage["type"]:
        case "color":

        case "image":

        case "trigger":

def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")


if __name__ == '__main__':
    # client_process = Process(target=udp_client)
    # server_process = Process(target=udp_server)
    # client_process.start()
    # server_process.start()
    # server_process.join()
    # client_process.terminate()
    url = "ws://{ip}:{port}/".format(ip=websocket_ip, port=websocket_port)
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
                              
    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()