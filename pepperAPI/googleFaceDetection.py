from google.cloud import vision
from google.cloud.vision import types

class GoogleFaceDetection:

    def get_faces_positions(self, input_filename):
        """
        get_faces_positions(positions) -> None
            Finds with help of google vision api all faces on an image. It returns an array of x-coordinates with each
            found face.

            @param input_filename Path and filename of image.
        """
        with open(input_filename, 'rb') as image:
            faces = self.__detect_face(image)
            print('Found {} face{}'.format(
                len(faces), '' if len(faces) == 1 else 's'))

            # Reset the file pointer, so we can read the file again
            image.seek(0)
            positions = self.__get_faces_positions(faces)
            positions.sort()
            print('X-coordinates of faces: ' + str(positions))

            return positions

    def __detect_face(self, face_file):
        # API client
        client = vision.ImageAnnotatorClient()

        content = face_file.read()
        image = types.Image(content=content)

        return client.face_detection(image=image).face_annotations

    def __get_faces_positions(self, faces):
        """
        Returns the middle x-coordinates of each face in an array.
        Args:
          faces: a list of faces found in the file. This should be in the format
              returned by the Vision API.
        """
        faces_x_coordinants = []

        for face in faces:
            face_x_mid_position = ((face.bounding_poly.vertices)[0].x + (face.bounding_poly.vertices)[1].x) / 2
            faces_x_coordinants.append(face_x_mid_position)

        return faces_x_coordinants