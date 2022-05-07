import asyncio
import json
import sys
import websockets

from utils import Config


async def send(websocket, action, data):
    """Build a send a message to the server."""
    message = json.dumps(
        {
            'action': action,
            'data': data
        }
    )
    print(f">>> {message}")
    await websocket.send(message)


async def process_event(websocket):
    """Process events received from the server"""
    while True:
        try:
            request = await websocket.recv()
            request_data = json.loads(request)
            print(f"<<< event: {request_data['event']} - data: {request_data['data']}")

            if request_data['event'] == "challenge" and request_data['data']['opponent'] == "martinv0001":
                await send(websocket, 'accept_challenge', {
                    'challenge_id': request_data['data']['challenge_id']
                })
            elif request_data['event'] == 'your_turn':
                pass
        except Exception as e:
            print(f"exception {e}")


async def start(host: str, auth_token: str):
    """start service"""
    uri = f"{host}?token={auth_token}"

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print(f"connected to {host}")
                await process_event(websocket)
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


def main(auth_token: str):
    asyncio.get_event_loop().run_until_complete(start(Config["host"], auth_token))


if __name__ == '__main__':
    """Read the token received from parameter or configured and start the service"""
    auth_token = None

    if len(sys.argv) >= 2:
        auth_token = sys.argv[1]
    else:
        auth_token = Config.get("token", None)

    if auth_token:
        main(auth_token)
    else:
        print("the token es missing")
