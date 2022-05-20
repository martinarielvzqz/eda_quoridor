import asyncio
import json
import os
import sys
import websockets

from quoridor.constants import (
    ACTION_ACCEPT_CHALLENGE,
    EVENT_CHALLENGE,
    EVENT_LIST_USERS,
    EVENT_GAME_OVER,
    EVENT_YOUR_TURN,
    GAMES_DIR
)
from quoridor.log import logger
from quoridor.quoridor import QuoridorList, Quoridor
from quoridor.utils import Config


async def process_event(websocket):
    """Process events received from the server"""
    while True:
        try:
            request = await websocket.recv()
            request_data = json.loads(request)

            if request_data["event"] == EVENT_LIST_USERS:
                logger.info(
                    f"<<< event: {request_data['event']} - data: {request_data['data']}"
                )

            elif request_data["event"] == EVENT_CHALLENGE:
                logger.info(f"<<< {request_data}")
                # only for dev
                # if request_data["data"]["opponent"] not in [
                #     "martinv0001",
                #     "martin2005@gmail.com",
                # ]:
                #     continue
                message = json.dumps({
                    "action": ACTION_ACCEPT_CHALLENGE,
                    "data": {"challenge_id": request_data["data"]["challenge_id"]}
                })
                await websocket.send(message)

            elif request_data["event"] == EVENT_YOUR_TURN:
                game = QuoridorList.get_or_create(request_data["data"])
                move = game.play(request_data["data"])
                await websocket.send(json.dumps(move))

            elif request_data["event"] == EVENT_GAME_OVER:
                logger.debug(f"<<< {request_data}")
                QuoridorList.finish_game(request_data["data"])
            else:
                logger.warning(
                    f"<<< unknown event: {request_data['event']} - data: {request_data['data']}"
                )

        except Exception as e:
            logger.error(f"exception {e}")


async def start(host: str, auth_token: str):
    """Start service"""
    uri = f"{host}?token={auth_token}"

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                logger.info(f"connected to {host}")
                await process_event(websocket)
        except KeyboardInterrupt:
            logger.info("exiting...")
            break
        except websockets.exceptions.InvalidURI as e:
            logger.error(f"invalid uri... {e}")
            break
        except Exception as e:
            logger.error(f"error connecting... {e}")
            # retry in 5 seconds
            await asyncio.sleep(5)


def main(auth_token: str):
    asyncio.get_event_loop().run_until_complete(start(Config["host"], auth_token))


if __name__ == "__main__":
    """Read the token received by parameter or configured one and start the service"""
    auth_token = None

    if len(sys.argv) >= 2:
        auth_token = sys.argv[1]
    else:
        auth_token = Config.get("token", None)

    if auth_token:
        os.makedirs(GAMES_DIR, exist_ok=True)
        main(auth_token)
    else:
        logger.error("the token es missing")
