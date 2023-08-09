# Currently displays face mesh on black background
# Delete black_frame and replace with frame if you want to display webcam
# Type 'q' to exit

import cv2
import mediapipe as mp
import numpy as np


class TestTrack:
    def __init__(self):
        self.middle_x = 0
        self.middle_y = 0

        # Initialize video capture
        self.captureDevice = cv2.VideoCapture(0)

        # Commented out code is for using test video and exporting
        #self.captureDevice = cv2.VideoCapture("sample_footage.mov")

        # Get the frame width and height
        width = int(self.captureDevice.get(3))
        height = int(self.captureDevice.get(4))

        # Create a VideoWriter object
        #self.out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25, (width, height))

        # Create a MediaPipe FaceMesh instance
        self.mp_face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

        self.run()

    def run(self):
        while True:
            ret, frame = self.captureDevice.read()

            if not ret:
                break

            # Create a black frame to draw face mesh on
            black_frame = np.zeros_like(frame)

            # Convert the frame from BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame with FaceMesh to detect facial landmarks
            results = self.mp_face_mesh.process(rgb_frame)

            # Draw the detected facial landmarks (including eyes) on the frame
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    for id, landmark in enumerate(face_landmarks.landmark):
                        x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                        cv2.circle(black_frame, (x, y), 2, (0, 255, 0), -1)

                    # Draw red circles at the middle of the eyes
                    left_eye_x = int(face_landmarks.landmark[33].x * frame.shape[1])
                    left_eye_y = int(face_landmarks.landmark[33].y * frame.shape[0])
                    right_eye_x = int(face_landmarks.landmark[263].x * frame.shape[1])
                    right_eye_y = int(face_landmarks.landmark[263].y * frame.shape[0])
                    self.middle_x = (left_eye_x + right_eye_x) // 2
                    self.middle_y = (left_eye_y + right_eye_y) // 2
                    cv2.circle(black_frame, (self.middle_x, self.middle_y), 4, (0, 0, 255), -1)

            # Display the black frame with detected facial landmarks
            cv2.imshow('Eye Tracking', black_frame)
            #self.out.write(black_frame)

            # Press 'q' to exit the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release video capture and close OpenCV windows
        self.captureDevice.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    TestTrack()
