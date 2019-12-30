class GameSolution:
    def __init__(self, max_value):
        self.__max_value = max_value
        self.__hugo_string = "hugo"

    def get_all_solutions(self, numbers):
        """
        get_all_solutions(numbers) -> Dictionary
            Calculates the solution for the numbers for the game HUGO. The result is returned as a dictionary. The
            key is the counter of the game and the value is the solution.

            @param numbers A list of numbers, for which the solution should be calculated.
        """
        numbers_to_play_with = []
        solution = {}

        for number in numbers:
            numbers_to_play_with.extend(self.__get_solution_for_number(number))

        numbers_to_play_with.sort()
        numbers_to_play_with = list(set(numbers_to_play_with))

        for val in range(1, self.__max_value + 1):
            if numbers_to_play_with.__contains__(val):
                solution[val] = self.__hugo_string
            else:
                solution[val] = str(val)

        return solution

    def __get_solution_for_number(self, number):
        hugo_numbers = []

        try:
            int(number)

            # string of value
            string_row = str(number)
            for val in range(1, self.__max_value + 1):
                hugo_numbers.append(val * number)

                # row with number in it
                if string_row not in str(val):
                    continue
                else:
                    hugo_numbers.append(val)

        except ValueError:
            print("No number recognized")

        return hugo_numbers
