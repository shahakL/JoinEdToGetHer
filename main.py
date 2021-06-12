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
        self._display_surf = None
        self._player_surface = None
        self._block_surf = None
        self._monster_surf = None
        self.level = 1

    def on_init(self):
        self._running = True
        self.won = False
        self.maze = Maze(18, 32)
        [player_pos, princess_pos] = self.maze.random_floor_position(2)
        self.player = Player(player_pos[1], player_pos[0], self.level)
        self.princess = Princess(princess_pos[1], princess_pos[0],
                                 self._scale_image(pygame.image.load("art/princess.png")))
        self.monsters = []
        self.fireflies = []

        pygame.init()

        self._display_surf = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT),
                                                     pygame.HWSURFACE | pygame.RESIZABLE)
        self._player_surface = self._scale_image(self.player.get_surface())
        self._block_surf = self._scale_image(pygame.image.load("art/wall.png"))
        self._fog_surf = self._scale_image(pygame.image.load("art/fog.png"))
        self._floor_surf = self._scale_image(pygame.image.load("art/floor.png"))
        self._monster_surf = self._scale_image(pygame.image.load("art/minotaur.png"))

        positions = self.maze.random_floor_position(self.level)
        for (y, x) in positions:
            self.monsters.append(Monster(x, y, image=self._monster_surf))

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
        fog1_radius = 100
        fog2_radius = 140
        alpha = 128
        self.maze.draw(self._display_surf, self.player, self.princess, self.fireflies, fog1_radius, fog2_radius,
                       self._block_surf, alpha, self._fog_surf, self._floor_surf, self.monsters)
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
            next_move = monster.get_next_move(self.player.position)
            if next_move:
                self.try_movement(next_move, monster)
        for i, firefly in enumerate(self.fireflies):
            if firefly.light <= 0:
                self.fireflies.pop(i)
                continue
            next_move = firefly.get_next_move()
            if next_move:
                did_move = self.try_movement(next_move, firefly)
                if not did_move:
                    firefly.reset_inertia()

    def on_execute(self):
        self.on_init()

        self.show_start_screen()

        while self._running:
            self.handle_key_presses()
            self.move_characters()

            self.handle_events()

            self.on_loop()
            self.on_render()
            self.handle_end_cases()
        self.show_score()
        self.on_cleanup()

    def _stop(self, *args, **kwargs):
        self._running = False

    def _scale_image(self, image):
        new_width = 36  # int(self.WINDOW_WIDTH / 20)
        new_height = 36  # int(self.WINDOW_HEIGHT / 20)
        return pygame.transform.smoothscale(image, (new_width, new_height))

    def try_movement(self, key, character):
        future_pos = character.check_future_position(key)
        if self.maze.check_empty(future_pos):
            character.move(key)
            return True
        else:
            return False

    def handle_end_cases(self):
        if any([self.are_touching(monster, self.player) for monster in self.monsters]):
            self._running = False
            self.won = False
        elif self.are_touching(self.princess, self.player):
            self._running = False
            self.won = True

    def are_touching(self, c1, c2):
        l = 20
        share_x = c1.position[0] <= c2.position[0] <= (c1.position[0] + l) or \
                  c2.position[0] <= c1.position[0] <= (c2.position[0] + l)
        share_y = c1.position[1] <= c2.position[1] <= (c1.position[1] + l) or \
                  c2.position[1] <= c1.position[1] <= (c2.position[1] + l)
        return share_x and share_y

    def show_score(self):
        if self.won:
            bg_color = (250, 200, 200)
            font_color = (255, 0, 0)
            self.level += 1
            msg = "You Joined Them Together! Press Enter and start level " + str(self.level) + "!"
        else:
            bg_color = (0, 0, 0)
            font_color = (255, 0, 0)
            msg = "You killed Ed! Press Enter to start over..."
        self._display_surf.fill(bg_color)
        myfont = pygame.font.SysFont("Papyrus", 30)
        label = myfont.render(msg, 1, font_color)
        self._display_surf.blit(label, (self.WINDOW_WIDTH * 0.01, self.WINDOW_HEIGHT * 0.9))
        pygame.display.flip()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        done = True
        self.on_execute()

    def show_start_screen(self):
        black = (0,0,0)
        self._display_surf.fill(black)
        title = pygame.font.SysFont("Blackadder ITC", 100)
        font_color = (255, 0, 0)
        label = title.render("Join Ed To Get Her", 1, font_color)
        self._display_surf.blit(label, (self.WINDOW_WIDTH * 0.1, self.WINDOW_HEIGHT * 0.3))
        subtitle = pygame.font.SysFont("Papyrus", 50)
        label = subtitle.render("press Enter to start level 1", 1, font_color)
        self._display_surf.blit(label, (self.WINDOW_WIDTH * 0.1, self.WINDOW_HEIGHT * 0.6))
        pygame.display.flip()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        done = True


if __name__ == "__main__":
    app = App()
    app.on_execute()
