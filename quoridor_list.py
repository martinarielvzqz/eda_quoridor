from quoridor import Quoridor


class QuoridorList:

    games = {}

    @classmethod
    def get_or_create(cls, data):
        """"""
        if data["game_id"] not in cls.games:
            cls.games[data["game_id"]] = cls(data["data"])

        return cls.games[data["game_id"]]


    @classmethod
    def finish_game(cls, data):
        """"""
        game = cls.games.pop(data["game_id"], None)
        return game.game_over(data)


