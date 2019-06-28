from triton.ecs import System

from .components import *
from .events import *

import pygame
import pygame.gfxdraw

pygame.init()

class RenderSystem(System):
    def initialize(self):
        self.screen = None
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.on(TickEvent, self.update)
        self.on(GameExitEvent, self.game_exit)
        self.on(ToggleFullscreenEvent, self.toggle_fullscreen)
        self.toggle_fullscreen(None)

    def toggle_fullscreen(self, _):
        self.screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.screen_size = (800, 800)
#        if self.screen is not None and self.screen.get_flags() & pygame.FULLSCREEN:
        self.screen = pygame.display.set_mode(self.screen_size, pygame.DOUBLEBUF, 32)
 #       else:
  #          self.screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN | pygame.DOUBLEBUF, 32)

    def update(self, _):
        self.screen.fill((100,100,100))

        for e, (p, r) in self.registry.get_components(
                Position, Renderable):

            if r.image is None:
                continue

            self.screen.blit(
                r.image,
                r.rect)

        pygame.display.update()
        dt = self.clock.tick(self.FPS)
        for e, (g,) in self.registry.get_components(
                GameState):
            g.dt = dt
            g.t += dt
            g.screen_size = self.screen_size
    
    def game_exit(self, _):
        pygame.quit()
