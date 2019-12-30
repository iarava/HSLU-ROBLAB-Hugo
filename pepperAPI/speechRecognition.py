from time import sleep
import zope.event
from pepperAPI.LED import LED
from pepperAPI.movement import Movement
import qi


class SpeechRecognition(object):
    def __init__(self, myRobot):
        super(SpeechRecognition, self).__init__()
        self.__speech = myRobot.ALSpeechRecognition
        self.__tts = myRobot.ALTextToSpeech

        # Example: Adds 1 to 100 + Hugo to the vocabulary
        self.__speech.pause(True)
        vocabulary = ["hugo", "yes", "no", "stop"]
        for i in range(1, 100):
            vocabulary.append(str(i))
        self.__speech.setVocabulary(vocabulary, False)
        self.__speech.pause(False)
        # Or, if you want to enable word spotting:
        # asr.setVocabulary(vocabulary, True)

        # Start the speech recognition engine with user Test_ASR
        self.__speech.subscribe2("Test_ASR")
        self.__subscriber = None
        self.__memory = myRobot.ALMemory
        self.__leds = LED(myRobot)
        self.__movement = Movement(myRobot)
        self.__animation = myRobot.session.service("ALAnimationPlayer")
        self.__subscribe()

    def recognition(self, value):
        self.__subscriber = None
        print("In SpeechRecognition: " + str(value[0]))
        print("In SpeechRecognition: " + str(value))
        if (value[1] > 0.42):
            self.__leds.rotating_eyes(0xFF0DFF)
            zope.event.notify(str(value[0]))
            sleep(1)
        else:
            qi.async(self.__make_gesture_and_default_body,"animations/Stand/Gestures/WhatSThis_1")
            self.__tts.say("What did you say?")
            sleep(1)
        self.__subscribe()

    def __subscribe(self):
        self.__leds.rotating_eyes(0xFBFF00)
        self.__subscriber = self.__memory.subscriber("WordRecognized")
        self.__subscriber.signal.connect(self.recognition)

    def unsubscribe_and_stop(self):
        # Stop the speech recognition engine with user Test_ASR
        self.__subscriber = None
        self.__speech.unsubscribe("Test_ASR")

    def subscribe_to_recognition_word(self, method):
        zope.event.subscribers.append(method)

    def unsubscribe_from_recognition_word(self, method):
        zope.event.subscribers.remove(method)

    def __make_gesture_and_default_body(self, gesture_path):
        self.__animation.run(gesture_path)
        self.__movement.default_body_position()
