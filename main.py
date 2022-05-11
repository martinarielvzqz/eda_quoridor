import asyncio
import json
import sys
import websockets

from constants import (
    LIST_USERS, CHALLENGE, YOUR_TURN, GAMEOVER
)
from log import logger
from quoridor import Quoridor
from utils import Config

# contenedor de juegos
# gameid: Quoridor instance
games = {}


async def send(websocket, action, data):
    """Build, send to the server and return a message."""
    message = json.dumps(
        {
            'action': action,
            'data': data
        }
    )
    await websocket.send(message)
    return message


async def process_event(websocket):
    """Process events received from the server"""
    while True:
        try:
            request = await websocket.recv()
            request_data = json.loads(request)

            if request_data['event'] == LIST_USERS:
                logger.debug(f"<<< event: {request_data['event']} - data: {request_data['data']}")

            elif request_data['event'] == CHALLENGE:
                if request_data['data']['opponent'] == "martinv0001":
                    await send(websocket, 'accept_challenge', {
                        'challenge_id': request_data['data']['challenge_id']
                    })

            elif request_data['event'] == YOUR_TURN:
                # get or create the corresponding game and play
                if request_data["data"]["game_id"] not in games:
                    games[request_data["data"]["game_id"]] = Quoridor(request_data["data"])
                game = games[request_data["data"]["game_id"]]

                print(f"GAMES {len(games)}")

                # only draw board for main player
                if game.player == "martin2005@gmail.com":
                    board_graph = game.draw_board(request_data['data']['board'])
                    logger.debug(f"board\n{board_graph}")
                action, data = game.play(request_data["data"])
                message = await send(websocket, action, data)
                logger.debug(f">>> {message}")
            elif request_data['event'] == GAMEOVER:
                # recuperar y remover el game del diccionario
                game = games.pop(request_data["data"]["game_id"], None)
                # imprimr resultado
                if game:
                    game_result, message = game.game_over(request_data["data"])
                    logger.info(f"{game_result.value.upper()}: {message}")
                    # borrarlo
                    del game
            else:
                logger.warning(f"<<< unknown event: {request_data['event']} - data: {request_data['data']}")

        except Exception as e:
            logger.error(f"exception {e}")


async def start(host: str, auth_token: str):
    """start service"""
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
        logger.error("the token es missing")
