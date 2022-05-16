from unittest import TestCase

from quoridor.quoridor import Quoridor


class TestQuoridor(TestCase):

    def setUp(self):
        self.data = {
            'score_1': -12.0,
            'score_2': -49.0,
            'walls': 9.0,
            'board': '        N     N                                                          |                *      -*-       |                                                                N                                 S|    S     S     *                |                                               ',  # noqa
            'side': 'S', 'player_1':
            'martinv0001',
            'player_2': 'martin2005@gmail.com',
            'remaining_moves': 171.0,
            'turn_token': '3317aaf3-a8a9-4e47-80a8-f2138ad4d408',
            'game_id': '32dc2990-ce84-11ec-aef0-7ecdf393f9cc'
        }

    def test_sample(self):
        game = Quoridor(self.data)
        assert isinstance(game, Quoridor)
