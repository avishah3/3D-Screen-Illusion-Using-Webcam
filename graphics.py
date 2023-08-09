import pygame
import numpy as np


class Graphics3D:
    def __init__(self, graphic, x, y, z, width, height):
        # Loading the graphic and making it 0.5x its size
        self.graphic = pygame.image.load(graphic)
        self.graphic = pygame.transform.scale(self.graphic, (self.graphic.get_width() // 2, self.graphic.get_height() // 2))

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

        # Resized graphic based on z-distance and camera z-distance
        resize_x = self.graphic.get_width() * self.cf * projected_z
        resize_y = self.graphic.get_height() * self.cf * projected_z

        scaled_gfx = pygame.transform.scale(self.graphic, (resize_x, resize_y))

        # Darken graphic based on z-distance
        dark = pygame.Surface((scaled_gfx.get_width(), scaled_gfx.get_height()), flags=pygame.SRCALPHA)
        n = 255 * (1-self.cf)
        dark.fill((n, n, n, 0))
        scaled_gfx.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

        # Rectangles are drawn by top left corner in pygame
        left_x = int(projected_x*self.width - scaled_gfx.get_width() / 2)
        top_y = int(projected_y*self.height - scaled_gfx.get_height() / 2)

        screen.blit(scaled_gfx, (left_x, top_y))