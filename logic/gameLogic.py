from enumerations.enums import GameDirection
from logic.gameSolution import GameSolution
import time


class GameLogic:
    def __init__(self):
        self.__numberOfOpponents = 1
        self.__whoseTurnCounter = 0
        self.__solution_counter = 1
        self.__game_direction = GameDirection.clockwise
        self.__game_solution = GameSolution(100)

        self.__opponents_position = []
        self.__potential_numbers_to_play_with = []
        self.__calculated_solution_numbers = {}

    def set_opponents_position(self, positions):
        """
        set_opponents_position(positions) -> None
            Sets the positions of all opponents. A position should place before the game starts
            and it should be a radiant value.

            @param positions A function argument.
        """
        self.__opponents_position = positions

    def get_position_of_current_player(self):
        """
        get_position_of_current_player(positions) -> radiant value
            Returns the position of the current player.
        """
        if self.__opponents_position.size != 0:
            if self.__whoseTurnCounter !=  0:
                return self.__opponents_position[self.__whoseTurnCounter - 1]
            else:
                return self.__opponents_position[0]

    def set_number_of_opponents(self, number):
        """
        set_number_of_opponents(number) -> bool
            Sets the number of opponents to play with.

            @param number Number of opponents
        """
        try:
            int(number)
            self.__reset_whose_turn_counter()
            self.__numberOfOpponents = number

            self.__logging("Method \"setNumberOfOpponents()\" Numbers of opponents set to " + str(number))
            return True
        except ValueError:
            return False

    def next_turn(self):
        """
        next_turn(positions) -> None
            Method should be called after each turn, so the whose-turn-counter and solution counter
            has the correct state.
        """
        if self.__game_direction == GameDirection.clockwise:
            self.__increase_whose_turn_counter()
        else:
            self.__decrease_whose_turn_counter()

        self.__solution_counter += 1
        self.__logging("Method \"nextTurn()\"")

    def set_game_direction(self, direction):
        """
        set_game_direction(direction) -> None
            Sets game direction. Default is GameDirection.clockwise.
        """
        self.__game_direction = direction
        self.__logging("Method \"setGameDirection()\" Game direction set to: " + str(direction))

    def set_numbers_to_play_temporary(self, numbers):
        """
        set_numbers_to_play_temporary(numbers) -> None
            Sets the numbers to play with temporary. The array should contains all number, which the user has set.
            Must be set before calling set_fixed_numbers().

            @:param numbers Expects an array.
        """
        self.__potential_numbers_to_play_with = numbers

    def set_fixed_numbers(self):
        """
        set_fixed_numbers() -> None
            After setting the numbers temporary, this method must be called, if the
        """
        if self.__potential_numbers_to_play_with.__len__() != 0:
            self.__calculated_solution_numbers = self.__game_solution.get_all_solutions(self.__potential_numbers_to_play_with)
            self.__potential_numbers_to_play_with = []
            self.__logging("Method \"setFixedNumbers()\" NumbersToPlayWith set to: " + str(self.__calculated_solution_numbers))

    def is_temporary_calculated(self):
        """
        is_temporary_calculated() -> bool
            Returns True if the numbers are temporary set otherwise False.
        """
        return self.__potential_numbers_to_play_with.__len__() != 0 and self.__calculated_solution_numbers.__len__() == 0

    def is_definitely_calculated(self):
        """
        is_definitely_calculated() -> bool
            Returns True if the solutions is calculated otherwise False.
        """
        return self.__potential_numbers_to_play_with.__len__() == 0 and self.__calculated_solution_numbers.__len__() != 0

    def reset_calculations(self):
        """
        reset_calculations() -> None
            Resets all calculations and sets them to default.
        """
        self.__numberOfOpponents = 1
        self.__whoseTurnCounter = 0
        self.__solution_counter = 1
        self.__game_direction = GameDirection.clockwise
        self.__potential_numbers_to_play_with = []
        self.__calculated_solution_numbers = {}

        self.__logging("Method \"resetCalculations()\" Calculations reseted")

    def is_it_my_turn(self):
        """
        is_it_my_turn() -> bool
            Returns True if it's peppers turn.
        """
        return self.__whoseTurnCounter == 0

    def get_solution(self):
        """
        get_solution() -> string
            Returns the solution for the current player.
        """
        return self.__calculated_solution_numbers[self.__solution_counter]

    def __increase_whose_turn_counter(self):
        if self.__whoseTurnCounter == self.__numberOfOpponents:
            self.__whoseTurnCounter = 0
        else:
            self.__whoseTurnCounter += 1

    def __decrease_whose_turn_counter(self):
        if self.__whoseTurnCounter == 0:
            self.__whoseTurnCounter = self.__numberOfOpponents
        else:
            self.__whoseTurnCounter -= 1

    def __reset_whose_turn_counter(self):
        self.__whoseTurnCounter = 0

    @staticmethod
    def __logging(message):
        print(str(time.time()) + " GameLogic.py: " + str(message))
