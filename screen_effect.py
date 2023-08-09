import pygame
import sys

from track_eyes import TrackEyes
from rectangles import Rectangle3D
from graphics import Graphics3D


class ScreenEffect:
    def __init__(self):
        # Create the TrackEyes instance
        self.track_eyes = TrackEyes()

        pygame.init()

        # Screen dimensions
        self.screen_width, self.screen_height = 1920, 1080
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('3D Screen Effect')

        # Calculate the scaling factors from webcam to game window
        self.x_scale = self.screen_width / self.track_eyes.webcam_width
        self.y_scale = self.screen_height / self.track_eyes.webcam_height

        # Eye info
        self.middle_x = self.screen_width / 2
        self.middle_y = self.screen_height / 2

        # Normalized eye info
        self.normalized_x = 0.5
        self.normalized_y = 0.5
        self.normalized_z = 0.5

        # Increase to intensify effect (0.5-1)
        # The further away the user is from the screen, the lower the number should be
        self.fov_multiplier = 0.75

        # Creating rectangles
        self.rectangles = []
        self.create_rectangles()

        # Creating graphics
        self.graphics = []
        self.create_graphics()

    def create_rectangles(self):
        # Lower rectangle count and increase width in rectangles.py for better performance
        num_rectangles = 2000
        for i in reversed(range(num_rectangles)):
            z = i * 0.0005  # Adjust the spacing of the rectangles in the z-direction
            self.rectangles.append(Rectangle3D(0.5, 0.5, z, self.screen_width, self.screen_height))

    def create_graphics(self):
        num_graphics = 10
        for i in reversed(range(num_graphics)):
            z = i * 0.05
            self.graphics.append(Graphics3D("gators_logo.png", 0.5, 0.5, z, self.screen_width, self.screen_height))

    def run(self):
        clock = pygame.time.Clock()
        while True:
            # Run at 60 fps and stop if 'X' button, 'q', or 'esc'
            clock.tick(60)
            self.track_eyes.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.track_eyes.release_capture()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        self.track_eyes.release_capture()
                        pygame.quit()
                        sys.exit()

            # Get the middle eye point
            middle_point = self.track_eyes.get_eye_info()

            if middle_point is not None:
                middle_x, middle_y, eye_dist = middle_point

                # Scale the middle eye tracking point to match pygame dimensions
                self.middle_x = int(middle_x * self.x_scale)
                self.middle_y = int(middle_y * self.y_scale)

                # Normalize values (z is based on distance between user's eyes)
                self.normalized_x = self.middle_x / self.screen_width
                self.normalized_y = self.middle_y / self.screen_height
                self.normalized_z = eye_dist / self.track_eyes.webcam_width

                # Clear the screen
                self.screen.fill((0, 0, 0))

                # Draw the middle eye tracking point as a white dot for testing
                #pygame.draw.circle(self.screen, (255, 255, 255), (self.middle_x, self.middle_y), 100 * self.normalized_z)

            # Draw the 3D rectangles
            for rectangle in self.rectangles:
                rectangle.draw(self.screen, (self.normalized_x, self.normalized_y, self.normalized_z), self.fov_multiplier)

            # Draw the 3D graphics
            for graphic in self.graphics:
                graphic.draw(self.screen, (self.normalized_x, self.normalized_y, self.normalized_z), self.fov_multiplier)

            # Update the display
            pygame.display.flip()


if __name__ == "__main__":
    screen_effect = ScreenEffect()
    screen_effect.run()
