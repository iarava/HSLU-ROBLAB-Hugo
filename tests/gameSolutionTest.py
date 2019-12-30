import unittest
from logic.gameSolution import GameSolution

class GameSolutionTest(unittest.TestCase):

    def test_soltionForNumber3(self):
        # given
        logic = GameSolution(13)
        hugo = "Hugo"
        expectedSolution = {
            1: "1",
            2: "2",
            3: hugo,
            4: "4",
            5: "5",
            6: hugo,
            7: "7",
            8: "8",
            9: hugo,
            10: "10",
            11: "11",
            12: hugo,
            13: hugo
        }

        # when
        actualSolution = logic.get_all_solutions([3])

        # then
        self.assertEqual(actualSolution, expectedSolution)

    def test_soltionForNumber3And4(self):
        # given
        logic = GameSolution(14)
        hugo = "Hugo"
        expectedSolution = {
            1: "1",
            2: "2",
            3: hugo,
            4: hugo,
            5: "5",
            6: hugo,
            7: "7",
            8: hugo,
            9: hugo,
            10: "10",
            11: "11",
            12: hugo,
            13: hugo,
            14: hugo
        }

        # when
        actualSolution = logic.get_all_solutions([3, 4])

        # then
        self.assertEqual(actualSolution, expectedSolution)

if __name__ == '__main__':
    unittest.main()