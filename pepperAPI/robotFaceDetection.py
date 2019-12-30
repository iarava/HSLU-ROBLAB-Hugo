from PIL import Image
from enumerations.enums import PictureSide
from pepperAPI.ftp import Ftp
import numpy as np
import time
from pepperAPI.googleFaceDetection import GoogleFaceDetection

imageWidth = 640
imageHeight = 480
robot_path_to_save = "/home/nao/gruppe5/"
path_local = "C:\\temp\\"
imgLeft = "left.jpg"
imgMiddle = "middle.jpg"
imgRight = "right.jpg"
imgName = "combined.jpg"
angle = 168.9


class RobotFaceDetection:
    def __init__(self, my_robot, movement):
        self.__img_combined = None
        self.__img_left = ""
        self.__img_middle = ""
        self.__img_right = ""
        self.__robot = my_robot
        self.__movement = movement
        self.__ftp = Ftp()
        self.__camera = self.__robot.ALPhotoCapture
        self.__google = GoogleFaceDetection()

    def detect_faces(self):
        """
        detect_faces(path) -> Array
            Takes pictures with three angels and detects position of faces on it. Method returns an array of
            radiant values, with the recognized faces on it.
        """
        self.__take_picture(PictureSide.Left)
        self.__take_picture(PictureSide.Middle)
        self.__take_picture(PictureSide.Right)
        self.__movement.default_position()
        self.__combine_images()
        faces = self.__google.get_faces_positions(path_local + imgName)
        array_of_faces = np.asarray(faces)
        self.__logging("Methode dectect_faces, rad-positions of faces: " + str(self.__x_to_rad(array_of_faces)))

        return self.__x_to_rad(array_of_faces)

    def __x_to_rad(self, x):
        return np.round(-1 * np.deg2rad((angle / (3 * imageWidth) * x) - angle / 2), 2)

    def __combine_images(self):
        try:
            self.__logging("Methode combine_images: starting")
            Left = self.__ftp.load_image_from_robot(robot_path_to_save + imgLeft)
            Middle = self.__ftp.load_image_from_robot(robot_path_to_save + imgMiddle)
            Right = self.__ftp.load_image_from_robot(robot_path_to_save + imgRight)
            self.__logging("Methode combine_images: opened all images")
            self.__img_combined = Image.new("RGB", (3 * imageWidth, imageHeight))
            self.__img_combined.paste(Left, (0, 0))
            self.__img_combined.paste(Middle, (imageWidth, 0))
            self.__img_combined.paste(Right, (2 * imageWidth, 0))
            self.__img_combined.save(path_local + imgName)
            self.__logging("Methode combine_images: saved combined image")
            self.__is_img_finished = True
            self.__logging("Methode take_Picture: saved left picture")
        except Exception, e:
            print("Fehler: " + str(e.message))

    def __take_picture(self, side):
        self.__logging("In Methode take_Picture")
        if side == PictureSide.Left:
            self.__movement.move_head(np.deg2rad(angle / 3), np.deg2rad(-9.7), 2)
            self.__img_left = self.__camera.takePicture(robot_path_to_save, imgLeft)
            self.__logging("Methode take_Picture: saved left picture")
        elif side == PictureSide.Middle:
            self.__movement.move_head(0, np.deg2rad(-9.7), 2)
            self.__img_middle = self.__camera.takePicture(robot_path_to_save, imgMiddle)
            self.__logging("Methode take_Picture: saved middle picture")
        elif side == PictureSide.Right:
            self.__movement.move_head(np.deg2rad(-angle / 3), np.deg2rad(-9.7), 2)
            self.__img_right = self.__camera.takePicture(robot_path_to_save, imgRight)
            self.__logging("Methode take_Picture: saved right picture")

    @staticmethod
    def __logging(message):
        print(str(time.time()) + " robotFaceDetection.py: " + str(message))