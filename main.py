from monster import Monster
from pygame.locals import *
import pygame
from functools import partial

from player import Player
from maze import Maze
from princess import Princess


class App:

    def __init__(self):
        self.WINDOW_WIDTH = 1280  # pygame.display.Info().current_w
        self.WINDOW_HEIGHT = 720  # pygame.display.Info().current_h
        self._running = True
        self._display_surf = None
        self._player_surface = None
        self._block_surf = None
        self._monster_surf = None
        self.maze = Maze(18, 32)
        [player_pos, princess_pos] = self.maze.random_floor_position(2)
        self.player = Player(player_pos[1], player_pos[0])
        self.princess = Princess(princess_pos[1], princess_pos[0], self._scale_image(pygame.image.load("art/princess.png")))
        self.monsters = []
        self.fireflies = []

    def on_init(self):
        pygame.init()

        self._display_surf = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT),
                                                     pygame.HWSURFACE | pygame.RESIZABLE)
        self._player_surface = self._scale_image(self.player.get_surface())
        self._block_surf = self._scale_image(pygame.image.load("art/wall.png"))
        self._fog_surf = self._scale_image(pygame.image.load("art/fog.png"))
        self._floor_surf = self._scale_image(pygame.image.load("art/floor.png"))
        self._monster_surf = self._scale_image(pygame.image.load("art/minotaur.png"))

        y, x = self.maze.random_floor_position()[0]
        self.monsters.append(Monster(x, y, self._monster_surf))

        pygame.display.set_caption('Join Ed To Get Her!')
        pygame.display.set_icon(self._player_surface)
        y, x = self.maze.random_floor_position()[0]
        self.monsters.append(Monster(x, y, self._monster_surf))
        self._running = True

    def handle_events(self):
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        fog1_radius = 100
        fog2_radius = 140
        alpha=128
        self.maze.draw(self._display_surf, self.player, self.princess, self.fireflies, fog1_radius, fog2_radius, self._block_surf, alpha, self._fog_surf, self._floor_surf, self.monsters)
        self._display_surf.blit(self._scale_image(self.player.get_surface()), self.player.position)
        self.render_fireflies()
        pygame.display.flip()

    def render_fireflies(self):
        for firefly in self.fireflies:
            self._display_surf.blit(self._scale_image(firefly.get_surface()), firefly.position)

    def on_cleanup(self):
        pygame.display.quit()
        pygame.quit()

    def handle_key_presses(self):
        keys = pygame.key.get_pressed()
        actions = {K_RIGHT: partial(self.try_movement, key=K_RIGHT, character=self.player),
                   K_LEFT: partial(self.try_movement, key=K_LEFT, character=self.player),
                   K_UP: partial(self.try_movement, key=K_UP, character=self.player),
                   K_DOWN: partial(self.try_movement, key=K_DOWN, character=self.player),
                   K_SPACE: partial(self.player.action, key=K_SPACE, app=self),
                   K_ESCAPE: self._stop}

        for key in actions.keys():
            if keys[key]:
                actions[key]()
    
    def move_characters(self):
        pnv = self.princess.get_next_move()
        if pnv:
            self.try_movement(pnv, self.princess)
        for monster in self.monsters:
            next_move = monster.get_next_move()
            if next_move:
                self.try_movement(next_move, monster)
        for i, firefly in enumerate(self.fireflies):
            if firefly.light <= 0:
                self.fireflies.pop(i)
                continue
            next_move = firefly.get_next_move()
            if next_move:
                self.try_movement(next_move, firefly)

    def on_execute(self):
        self.on_init()

        while self._running:
            self.handle_key_presses()
            self.move_characters()
            self.handle_end_cases()

            self.handle_events()

            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def _stop(self, *args, **kwargs):
        self._running = False

    def _scale_image(self, image):
        new_width = 36#int(self.WINDOW_WIDTH / 20)
        new_height = 36#int(self.WINDOW_HEIGHT / 20)
        return pygame.transform.smoothscale(image, (new_width, new_height))

    def try_movement(self, key, character):
        future_pos = character.check_future_position(key)
        if self.maze.check_empty(future_pos):
            character.move(key)

    def handle_end_cases(self):
        pass


if __name__ == "__main__":
    app = App()
    app.on_execute()
