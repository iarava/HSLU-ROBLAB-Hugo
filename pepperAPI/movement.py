import qi

from time import sleep
from pepperAPI.LED import LED
import time


class Movement(object):
    def __init__(self,my_robot):
        self.__move = my_robot.ALMotion
        self.__max_rad = 1.57
        self.__leds = LED(my_robot)
        self.__audio = my_robot.ALAudioPlayer

    def wakeup(self):
        """
        wakeup() -> None
            Calls the wakeUp() method on the roboter, to start it and set head to default position.
        """
        print("starting robot")
        self.__move.wakeUp()
        self.default_head_position()
        print("end starting robot")

    def move_head(self, rad_x, rad_y, time_to_wait_after_movement):
        """
        move_head(rad_x, rad_y, time) -> None
            Moves head to x- and y-radiant value and sleeps the given time.

            @param rad_x Radiant value of x-position
            @param rad_y Radiant value of y-position
            @param time_to_wait_after_movement
        """
        self.__logging("Method: moveHead() -> starting movment with param " + str(rad_x) + " and " + str(rad_y))
        if rad_x is None:
            rad_x = 0

        rad_x = round(rad_x, 2)
        rad_y = round(rad_y, 2)

        if rad_x > self.__max_rad:
            rad_x = self.__max_rad
        self.__move.setAngles("HeadYaw", rad_x, 0.2)
        self.__move.setAngles("HeadPitch", rad_y, 0.2)
        sleep(time_to_wait_after_movement)

    def winner_dance(self):
        """
        winner_dance() -> None
            Start a cool winner dance with music.
        """
        qi.async(self.__leds.rasta)
        qi.async(self.__audio.playFile, "/data/home/nao/gruppe5/win1.mpeg")
        print("Dancing")
        self.__dance_start_position()
        sleep(2)
        self.__dance_arm()
        sleep(1)
        self.default_position()
        sleep(3)
        self.__audio.stopAll()

    def default_position(self):
        """
        default_position() -> None
            Sets the body and head of the roboter to it's default positions.
        """
        self.default_body_position()
        self.default_head_position()

    def default_body_position(self):
        """
        default_body_position() -> None
            Sets the body robot to it's default positions.
        """
        pace = 0.1

        self.__move.setAngles("LShoulderPitch", 1.75, pace)
        self.__move.setAngles("LShoulderRoll", 0.098, pace)
        self.__move.setAngles("LElbowRoll", -0.096, pace)
        self.__move.setAngles("LElbowYaw", -1.69, pace)
        self.__move.setAngles("LHand", 0.012, pace)
        self.__move.setAngles("LWristYaw", 0.03, pace)
        self.__move.setAngles("RShoulderPitch", 1.75, pace)
        self.__move.setAngles("RShoulderRoll", -0.098, pace)
        self.__move.setAngles("RElbowRoll", 0.096, pace)
        self.__move.setAngles("RElbowYaw", 1.69, pace)
        self.__move.setAngles("RHand", 0.012, pace)
        self.__move.setAngles("RWristYaw", -0.03, pace)
        self.__move.setAngles("KneePitch", -0.01, pace)
        self.__move.setAngles("HipPitch", -0.035, pace)
        self.__move.setAngles("HipRoll", 0.0, pace)
        self.__logging("Method default_body_position(): Set body to default.")

    def default_head_position(self):
        """
        default_head_position() -> None
            Sets the head robot to it's default positions.
        """
        self.__move.setAngles("HeadPitch", 0.0, 0.1)
        self.__move.setAngles("HeadYaw", 0.0, 0.1)
        self.__logging("Method default_head_position(): Set head to default.")

    def __dance_start_position(self):
        positionHeadPitch = 0.5
        positionHeadYaw = 0
        positionKneePitch = 1.6
        positionHipPitch = 0.5
        pace = 0.1
        self.__move.setAngles("HeadPitch", positionHeadPitch, pace)
        self.__move.setAngles("HeadYaw", positionHeadYaw, pace)
        self.__move.setAngles("KneePitch", positionKneePitch, pace)
        self.__move.setAngles("HipPitch", -positionHipPitch, pace)

    def __dance_arm(self):
        positionShoulderPitch = 0.8
        positionElbowRoll = 1.3
        pace = 0.5
        for i in range(1, 4):
            self.__move.setAngles("RShoulderPitch", positionShoulderPitch, pace)
            self.__move.setAngles("RElbowRoll", positionElbowRoll, pace)
            sleep(0.5)
            self.__move.setAngles("RShoulderPitch", 1.9, pace)
            self.__move.setAngles("RElbowRoll", positionElbowRoll, pace)
            sleep(0.5)

    @staticmethod
    def __logging(message):
        print(str(time.time()) + " Movement.py: " + str(message))