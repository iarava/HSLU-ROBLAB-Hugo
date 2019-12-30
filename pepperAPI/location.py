from naoqi import ALModule

from enumerations.enums import Position


class Location(ALModule):
    """
        This class is unfortunately not used in the program. We didn't have enough time to add this feature.
        With this class it should be possible, to detect sound and to tell if the "correct" person did say the
        solution...
    """
    def __init__(self, myrobot):
        super(Location, self)
        self.position = Position.unknown

        session = myrobot.session
        self.memory = session.service("ALMemory")

        self.tts = session.service("ALTextToSpeech")
        self.sound_localization = session.service("ALSoundLocalization")
        self.sound_localization.setParameter("Sensitivity", 0.8)
        self.sound_localization.subscribe("SoundLocalizationModule")

        self.subscriber = self.memory.subscriber("ALSoundLocalization/SoundLocated")
        self.subscriber.signal.connect(self.on_sound_located)

    def get_position(self):
        return self.position

    def subscribe_location(self):
        self.subscriber = self.memory.subscriber("ALSoundLocalization/SoundLocated")
        self.subscriber.signal.connect(self.on_sound_located)

    def on_sound_located(self, value):
        # Unsubscribe from to prevent multiple triggers
        self.subscriber = None

        if value[1][0] >= -0.26 and value[1][0] <= 0.26:
            self.tts.say("Front")
            self.position = Position.front
        elif value[1][0] >= -1.74 and value[1][0] < -0.26:
            self.tts.say("Right")
            self.position = Position.right
        elif value[1][0] > 0.26 and value[1][0] <= 1.74:
            self.tts.say("Left")
            self.position = Position.left
        elif value[1][0] >= -0.26 and value[1][0] <= 0.26:
            self.tts.say("Behind")
            self.position = Position.back
        else:
            self.tts.say("Unknown")
            self.position = Position.unknown

