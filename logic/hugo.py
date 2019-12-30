import qi

from enumerations.enums import GameDirection, PictureSide
from pepperAPI.movement import Movement
from logic.gameLogic import GameLogic
from pepperAPI.robotFaceDetection import RobotFaceDetection
import time
import numpy as np


class Hugo(object):
    def __init__(self, my_robot):
        # init robot
        self.__movement = Movement(my_robot)
        self.__tts = my_robot.ALTextToSpeech
        self.__animation = my_robot.session.service("ALAnimationPlayer")
        # init class variable
        self.__numbers_temporary_recognized = False
        self.__playing = False
        self.__playing_again_requested = False
        self.__gameCanceled = False
        self.__detected_opponents = 1
        # helper classes
        self.__game_logic = GameLogic()
        self.__picture_logic = RobotFaceDetection(my_robot, self.__movement)

    def sub_first_number_recognition(self, number):
        """
        sub_first_number_recognition(positions) -> None
            This method sets the temporary recognized number. Pepper asks then back if the recognized
            number is correct.

            @param number The recognized number
        """
        try:
            if not self.__numbers_temporary_recognized:
                self.__game_logic.set_numbers_to_play_temporary([int(number)])

                if self.__detected_opponents != 0:
                    self.__game_logic.set_number_of_opponents(self.__detected_opponents)

                self.__game_logic.set_game_direction(GameDirection.clockwise)
                self.__tts.say("Let's play with number " + str(number) + ", is this correct?")
                self.__numbers_temporary_recognized = True
            else:
                self.__logging(
                    "Method \"sub_rowCalculated()\" self.__rowRecognized: " + str(self.__numbers_temporary_recognized))
        except Exception, e:
            self.__logging("Method \"sub_rowCalculated()\" in exception: Not a number:" + str(e))

    def sub_question_if_correct_row_recognized(self, value):
        """
        sub_question_if_correct_row_recognized(value) -> None
            After temporary recognized number, this method sets fixed value, if opponent says yes otherwise he
            asks back.

            @param value The recognized value.
        """
        # Check if correct number
        if self.__is_temporary_recognized() and str(value).lower() == "yes":
            self.__game_logic.set_fixed_numbers()

            self.__tts.say("Cool let's start!")
            self.__tts.say("It's my turn")

            self.__playing = True
            self.__say_solution()
            self.__prepare_next_turn()

        elif self.__is_temporary_recognized() and str(value).lower() == "no":
            self.__tts.say("Could you repeat the number please?")
            self.__reset_game()
        else:
            self.__logging("Method \"sub_questionIfCorrectRow()\" self.__rowRecognized: " + str(
                self.__numbers_temporary_recognized) +
                           "and self.__gameLogic.isTemporaryCalculated(): " + str(
                self.__game_logic.is_temporary_calculated()) +
                           "and value: " + str(value))

    def sub_playing_number(self, number):
        """
        sub_playing_number(number) -> None
            Method while in playing mode. Pepper checks and calculates correct solution.

            @param number Recognized number
        """
        if self.__is_playing() and str(number).lower() != 'stop':
            if not self.__game_logic.is_it_my_turn():  # opponents turn
                if self.__is_correct_solution(number):
                    self.__prepare_next_turn()

                    if self.__game_logic.is_it_my_turn():
                        self.__say_solution()
                        self.__prepare_next_turn()
                else:
                    self.__say_correct_solution_and_restart()
        else:
            self.__logging("Method \"sub_numberPlay()\" self.__gameCanceled: " + str(self.__gameCanceled) +
                           " and self.__playing: " + str(self.__playing) +
                           " and not number: __gameLogic.isDefenetlyCalulated() " + str(
                self.__game_logic.is_definitely_calculated()))

    def sub_stop_requested(self, value):
        """
        sub_stop_requested(value) -> None
            Method to cancel the game by saying "stop"

            @param value Recognized value
        """
        if str(value).lower() == "stop":
            self.__gameCanceled = True
            self.__logging("Method \"sub_stopRequested()\" Stop is requested and successful set")
        else:
            self.__logging("Method \"sub_stopRequested()\" Stop not requested")

    def sub_playing_again(self, value):
        """
        sub_playing_again(value) -> None
             Method to play again.

            @param value Recognized value
        """
        if self.__playing_again_requested:
            if str(value).lower() == "yes":
                self.__playing_again_requested = False
                self.__say_start_game()
            elif str(value).lower() == "no":
                self.__gameCanceled = True

    def say_bye(self):
        qi.async(self.__make_gesture_and_reset, "animations/Stand/Gestures/Hey_3")
        self.__tts.say("Oh it's a pity, but lets play another time!")
        self.__tts.say("See ya")
        self.__movement.default_position()

    def init_game(self):
        qi.async(self.__make_gesture_and_default_body, "animations/Stand/Gestures/Hey_7")
        self.__tts.say("Let's play hugo!")
        time.sleep(3)
        self.__say_start_game()

    def __make_gesture_and_reset(self, gesture_path):
        self.__animation.run(gesture_path)
        self.__movement.default_position()

    def __make_gesture_and_default_body(self, gesture_path):
        self.__animation.run(gesture_path)
        self.__movement.default_body_position()

    def is_game_canceled(self):
        return self.__gameCanceled

    def __prepare_next_turn(self):
        self.__game_logic.next_turn()
        self.__movement.move_head(self.__game_logic.get_position_of_current_player(), np.deg2rad(-9.7), 0.5)

    def __find_opponents(self):
        qi.async(self.__tts.say, "I'm identifying my super opponents")
        faces = self.__picture_logic.detect_faces()
        self.__game_logic.set_opponents_position(faces)
        self.__detected_opponents = faces.size
        self.__movement.move_head(self.__game_logic.get_position_of_current_player(), np.deg2rad(-9.7), 0.5)
        self.__tts.say("I found " + str(faces.size) + " people.")


    def __say_start_game(self):
        self.__find_opponents()
        self.__movement.move_head(self.__game_logic.get_position_of_current_player(), np.deg2rad(-9.7), 0.5)
        qi.async(self.__make_gesture_and_default_body, "animations/Stand/Gestures/You_1")
        self.__tts.say("Which row do you want to play?")

    def __reset_game(self):
        self.__numbers_temporary_recognized = False
        self.__playing = False
        self.__game_logic.reset_calculations()

        self.__logging("Method \"resetGame()\" Game reseted")

    def __say_solution(self):
        gesture_path = "animations/Stand/Gestures/HeSays_" + str(np.random.choice([1, 2, 3]))
        qi.async(self.__make_gesture_and_default_body, gesture_path)
        self.__tts.say(self.__game_logic.get_solution())

    def __is_playing(self):
        return not self.__gameCanceled and self.__playing and self.__game_logic.is_definitely_calculated()

    def __say_correct_solution_and_restart(self):
        qi.async(self.__make_gesture_and_reset, "animations/Stand/Gestures/No_3")
        self.__tts.say("You're wrong! The correct solution is " + str(self.__game_logic.get_solution()))
        self.__tts.say("I won! Let's dance")
        self.__movement.winner_dance()

        self.__movement.move_head(self.__game_logic.get_position_of_current_player(), np.deg2rad(-9.7), 0.5)
        self.__tts.say("Do you want to play again?")
        self.__reset_game()
        self.__playing_again_requested = True

    def __is_correct_solution(self, number):
        return str(self.__game_logic.get_solution()).lower() == str(number)

    def __is_temporary_recognized(self):
        return self.__numbers_temporary_recognized == True and self.__game_logic.is_temporary_calculated()

    @staticmethod
    def __logging(message):
        print(str(time.time()) + " Hugo.py: " + str(message))
