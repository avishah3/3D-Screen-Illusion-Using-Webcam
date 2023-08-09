import math

import cv2
import mediapipe as mp


class TrackEyes:
    def __init__(self):
        # Initialize video capture
        self.captureDevice = cv2.VideoCapture(0)

        # Get the webcam dimensions
        self.webcam_width = int(self.captureDevice.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.webcam_height = int(self.captureDevice.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Middle eye coordinates
        self.middle_x = self.webcam_width / 2
        self.middle_y = self.webcam_height / 2

        # Eye distance (to determine how close/far user is)
        self.eye_dist = 0.15 * self.webcam_width

        # Create a MediaPipe FaceMesh instance
        self.mp_face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

    def get_eye_info(self):
        return self.middle_x, self.middle_y, self.eye_dist

    def update(self):
        ret, frame = self.captureDevice.read()

        if not ret:
            self.release_capture()

        # Convert the frame from BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with FaceMesh to detect facial landmarks
        results = self.mp_face_mesh.process(rgb_frame)

        # Get eye information
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                left_eye_x = int(face_landmarks.landmark[33].x * frame.shape[1])
                left_eye_y = int(face_landmarks.landmark[33].y * frame.shape[0])
                right_eye_x = int(face_landmarks.landmark[263].x * frame.shape[1])
                right_eye_y = int(face_landmarks.landmark[263].y * frame.shape[0])

                self.middle_x = (left_eye_x + right_eye_x) // 2
                self.middle_y = (left_eye_y + right_eye_y) // 2

                self.eye_dist = math.sqrt((right_eye_x - left_eye_x)**2 + (right_eye_y - left_eye_y)**2)

    def release_capture(self):
        self.captureDevice.release()
        cv2.destroyAllWindows()
