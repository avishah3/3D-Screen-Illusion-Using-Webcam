import pygame
import numpy as np


class Rectangle3D:
    def __init__(self, x, y, z, width, height):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height

        # Perspective projection isn't linear, this logarithmic function estimates xyz to xy
        self.cf = np.exp(-5 * z)

    def draw(self, screen, camera_pos, fov_multiplier):
        fov_ratio = fov_multiplier * (camera_pos[2]+0.7)

        # Projecting xyz to xy with respect to eye location
        projected_x = 1 - (self.x + (self.x - camera_pos[0]) * (1-self.cf) * fov_ratio)
        projected_y = 1 - (self.y + (self.y - camera_pos[1]) * (1-self.cf) * fov_ratio)
        projected_z = camera_pos[2] * 1.5 + 1.0

        # Resized rectangle based on z-distance and camera z-distance
        out_width = self.width * self.cf * projected_z
        out_height = self.height * self.cf * projected_z

        # Rectangles are drawn by top left corner in pygame
        rect_x = int(projected_x*self.width - out_width / 2)
        rect_y = int(projected_y*self.height - out_height / 2)

        # Drawing rectangle (further away is darker)
        rect = pygame.Rect(rect_x, rect_y, out_width, out_height)
        width = 40*self.cf
        color = (0*self.cf, 50*self.cf, 248*self.cf)
        pygame.draw.rect(screen, color, rect, width=int(width))
