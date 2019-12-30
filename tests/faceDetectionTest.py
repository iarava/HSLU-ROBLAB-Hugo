import unittest
from pepperAPI.googleFaceDetection import GoogleFaceDetection

class GameLocigTest(unittest.TestCase):

    def test_simpleProcess(self):
        google = GoogleFaceDetection()

        positions = google.get_faces_positions('images/Kombiniert.jpg')
        print(positions)

if __name__ == '__main__':
    unittest.main()