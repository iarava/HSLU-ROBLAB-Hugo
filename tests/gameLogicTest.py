import unittest
from logic.gameLogic import GameLogic

class GameLocigTest(unittest.TestCase):

    def test_simpleProcess(self):
        logic = GameLogic()

        self.assertFalse(logic.is_temporary_calculated())
        self.assertFalse(logic.is_definitely_calculated())

        logic.set_numbers_to_play_temporary([2])
        self.assertTrue(logic.is_temporary_calculated())
        self.assertFalse(logic.is_definitely_calculated())

        logic.set_fixed_numbers()
        self.assertFalse(logic.is_temporary_calculated())
        self.assertTrue(logic.is_definitely_calculated())

        logic.reset_calculations()
        self.assertFalse(logic.is_temporary_calculated())
        self.assertFalse(logic.is_definitely_calculated())

    def test_playingOneToOne(self):
        logic = GameLogic()
        logic.set_numbers_to_play_temporary([3])
        logic.set_fixed_numbers()

        self.assertEqual(logic.get_solution(), "1")
        logic.next_turn()
        self.assertEqual(logic.get_solution(), "2")
        logic.next_turn()
        self.assertEqual(logic.get_solution(), "Hugo")
        logic.next_turn()
        self.assertEqual(logic.get_solution(), "4")

if __name__ == '__main__':
    unittest.main()