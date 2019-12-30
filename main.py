from pynaoqi_mate import Robot
from configuration import PepperConfiguration
from pepperAPI.speechRecognition import SpeechRecognition
from logic.hugo import Hugo
from pepperAPI.movement import Movement
from time import sleep

try:
    # Init stuff
    virtualRobotConfig = PepperConfiguration("Porter")
    my_robot = Robot(virtualRobotConfig)
    tts = my_robot.ALTextToSpeech
    tts.setLanguage("English")
    hugo = Hugo(my_robot)
    movement = Movement(my_robot)

     # init game
    movement.wakeup()
    movement.default_position()

    hugo.init_game()
    print("Init Game successfull")

    """ subscribe methode to word recognition """
    speechRecognition = SpeechRecognition(my_robot)
    speechRecognition.subscribe_to_recognition_word(hugo.sub_first_number_recognition)
    speechRecognition.subscribe_to_recognition_word(hugo.sub_playing_number)
    speechRecognition.subscribe_to_recognition_word(hugo.sub_question_if_correct_row_recognized)
    speechRecognition.subscribe_to_recognition_word(hugo.sub_stop_requested)
    speechRecognition.subscribe_to_recognition_word(hugo.sub_playing_again)
    print("Methods subscribed")

    while not hugo.is_game_canceled():
        sleep(0.1)

except Exception, e:
    print("Something is wrong: " + e.message)

finally:
    speechRecognition.unsubscribe_and_stop()
    my_robot.ALSpeechRecognition.pause(True)
    my_robot.ALSpeechRecognition.removeAllContext()
    my_robot.ALSpeechRecognition.pause(False)

    hugo.say_bye()

