import socket
import asyncio
import websocket
from multiprocessing import Process
import time
import rel
import json
from matrix import Matrix
import base64

from PIL import Image #delete later

websocket_ip = "192.168.1.65"
websocket_port = 8080

udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

myMatrix = Matrix()

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
    if jsonMessage["type"] == "image":
        myImage = Image.frombytes('RGB', (int(jsonMessage["width"]),int(jsonMessage["height"])), base64.b64decode(jsonMessage["content"]))
        myMatrix.applyImage(myImage, int(jsonMessage["brightness"]))

    elif jsonMessage["type"] == "color":
        print("color")

def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")
    time.sleep(1)
    ws.send("teste")


if __name__ == '__main__':
    # client_process = Process(target=udp_client)
    # server_process = Process(target=udp_server)
    # client_process.start()
    # server_process.start()
    # server_process.join()
    # client_process.terminate()
    url = "ws://{ip}:{port}/".format(ip=websocket_ip, port=websocket_port)
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    ws.run_forever(dispatcher=rel, reconnect=5)
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()

    
    # myMatrix.lightZone((255,0,0), 25, 0)
    # while True:
    #     time.sleep(1)
    #     myMatrix.lightZone((255,0,0), 25,1)
