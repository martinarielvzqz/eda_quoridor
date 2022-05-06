import asyncio
import json
import websockets

from utils import Config


async def play(websocket):
    """..."""

    while True:
        try:
            request = await websocket.recv()
            request_data = json.loads(request)
            print(f"<<< event: {request_data['event']} - data: {request_data['data']}")
        except Exception as e:
            print(f"exception {e}")


async def start(host: str, auth_token: str):
    """start service"""
    uri = f"{host}?token={auth_token}"

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print(f"connected to {host}")
                await play(websocket)
        except KeyboardInterrupt:
            print("exiting...")
            break
        except websockets.exceptions.InvalidURI as e:
            print(f"invalid uri... {e}")
            break
        except Exception as e:
            print(f"error connecting... {e}")
            # retry in 5 segs
            await asyncio.sleep(5)


def main():
    asyncio.get_event_loop().run_until_complete(start(Config['host'], Config['token']))


if __name__ == '__main__':
    main()
