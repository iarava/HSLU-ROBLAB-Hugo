class LED(object):
    def __init__(self, my_robot):
        self.__leds = my_robot.ALLeds

    def rotating_eyes(self, color):
        """
        rotating_eyes(color) -> None
            Rotates the eyes with color for 1/2 second.

            @param color hex-color
        """
        self.__leds.rotateEyes(color, 0.5, 0.5)

    def rasta(self):
        """
        rasta() -> None
            Starts the LED animation rasta.
        """

        self.__leds.rasta(7)