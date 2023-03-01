#!/usr/bin/env python
from concurrent.futures import ProcessPoolExecutor
from aioconsole import ainput
import asyncio
import websockets
from PIL import Image
from io import BytesIO
import json
import base64

image = Image.open("src/Untitled1.png")
image_bytes = image.tobytes()
image_io = BytesIO(image_bytes)
encoded_image = base64.b64encode(image_bytes)

image_string = '{{"type":"image", "content":"{stream}", "width":"{width}", "height":"{height}", "brightness":"{brightness}"}}'.format(stream=encoded_image.decode(),
                                                                                                                                      width=image.width,
                                                                                                                                      height=image.height,
                                                                                                                                      brightness=25)

color_string = '{"type": "color", "rgb":[0,255,0], "brightness":"25", "zone": "2"}'.encode()

trigger_string = '{"type":"status", "value":"1"}'.encode()

clear_string = '{"type":"clear"}'.encode()

# async def echo(websocket):
#     async for message in websocket:
#         await websocket.send(trigger_string)

async def echo(websocket):
    while True:
        text = await cmdListener()
        
        if text == "color":
            await websocket.send(color_string)
        elif text == "image": 
            await websocket.send(image_string)
        elif text == "trigger": 
            await websocket.send(trigger_string)
            async for message in websocket:
                #await websocket.send(trigger_string)
                print(message)
                break
        elif text == "clear": 
            await websocket.send(clear_string)

        


async def main():
    async with websockets.serve(echo, "192.168.1.65", 8080):
        await asyncio.Future()  # run forever´

async def cmdListener():
    #global text
    while True:
        text = await ainput(">>> ")
        if(text=="color" or text=="image" or text=="trigger" or text=="clear"):
            return text

asyncio.run(main())

# if __name__ == "__main__":
#     executor = ProcessPoolExecutor(2)
#     loop = asyncio.new_event_loop()
#     boo = loop.run_in_executor(executor, say_boo)
#     baa = loop.run_in_executor(executor, say_baa)

#     loop.run_forever()