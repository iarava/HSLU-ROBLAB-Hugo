from paramiko import SSHClient, AutoAddPolicy
import cv2
import numpy as np
from PIL import Image


class Ftp(object):
    def __init__(self):
        self.__ssh_client = None
        self.__sftp_client = None

    def load_image_from_robot(self, path):
        """
        load_image_from_robot(path) -> Image
            Returns an PIL image.

            @param path Path, inclusive image name and extension.
        """
        try:
            self.__ssh_client = SSHClient()
            self.__ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            self.__ssh_client.connect("192.168.1.102", username='nao', password='i2-p2e3p')
            self.__sftp_client = self.__ssh_client.open_sftp()

            remote_file = None
            image = None
            try:
                remote_file = self.__sftp_client.open(path, 'r')
                image = cv2.imdecode(np.fromstring(remote_file.read(), np.uint8), 1)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image, "RGB")
                print("image decoded")

            except IOError, e:
                print("Error in opening image via FTP: ", e.message)
            finally:
                if remote_file is not None:
                    remote_file.close()

            if self.__sftp_client is not None:
                self.__sftp_client.close()
                self.__ssh_client.close()
        except IOError, e:
            print("Error in opening image via FTP: ", e.message)

        return image