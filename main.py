from pygame.locals import *
import pygame
from functools import partial

from player import Player
from maze import Maze


class App:

    def __init__(self):

        self._running = True
        self._display_surf = None
        self._player_surface = None
        self._block_surf = None
        self.player = Player()
        self.maze = Maze(10, 10)

    def on_init(self):
        pygame.init()
        self.WINDOW_WIDTH = 1280  # pygame.display.Info().current_w
        self.WINDOW_HEIGHT = 720  # pygame.display.Info().current_h

        self._display_surf = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT),
                                                     pygame.HWSURFACE | pygame.RESIZABLE)
        self._running = True
        self._player_surface = self._scale_image(self.player._rotated_image)
        self._block_surf = self._scale_image(pygame.image.load("art\wall.png"))
        self._fog_surf = self._scale_image(pygame.image.load("art/fog.png"))
        self._floor_surf = self._scale_image(pygame.image.load("art/floor.png"))

        pygame.display.set_caption('Join Ed To Get Her!')
        pygame.display.set_icon(self._player_surface)

    def handle_events(self):
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        fog_radius = 100
        self.maze.draw(self._display_surf, self.player, fog_radius, self._block_surf, self._fog_surf, self._floor_surf)
        self._display_surf.blit(self._scale_image(self.player._rotated_image), (self.player._x, self.player._y))
        pygame.display.flip()

    def on_cleanup(self):
        pygame.display.quit()
        pygame.quit()

    def handle_key_presses(self):
        keys = pygame.key.get_pressed()
        actions = {K_RIGHT: partial(self.try_movement, key=K_RIGHT),
                   K_LEFT: partial(self.try_movement, key=K_LEFT),
                   K_UP: partial(self.try_movement, key=K_UP),
                   K_DOWN: partial(self.try_movement, key=K_DOWN),
                   K_ESCAPE: self._stop}

        for key in actions.keys():
            if keys[key]:
                actions[key]()

    def on_execute(self):
        self.on_init()

        while self._running:
            self.handle_key_presses()

            self.handle_events()

            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def _stop(self, *args, **kwargs):
        self._running = False

    def _scale_image(self, image):
        new_width = int(self.WINDOW_WIDTH / 20)
        new_height = int(self.WINDOW_HEIGHT / 20)
        return pygame.transform.smoothscale(image, (new_width, new_height))

    def try_movement(self, key):
        future_pos = self.player.check_future_position(key)
        if self.maze.check_empty(future_pos):
            self.player.move(key)


if __name__ == "__main__":
    app = App()
    app.on_execute()
