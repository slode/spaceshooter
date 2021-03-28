from triton.ecs import System

from .events import *
from .components import *

import pygame

# Systems
class InputSystem(System):
    def initialize(self):
        self.on(TickEvent, self.update)

    def update(self, _):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.emit(GameExitEvent())
                break

            if event.type == pygame.KEYDOWN:
                for e, [player] in self.registry.get_components(Player):
                    if event.key in player.key_map.keys():
                        self.registry.add_component(e, player.key_map[event.key])
                        continue
            if event.type == pygame.KEYUP:
                for e, [player] in self.registry.get_components(Player):
                    if event.key in player.key_map.keys():
                        self.registry.remove_component(e, player.key_map[event.key])
                        continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.emit(GameExitEvent())
                    break

            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_u:
                    self.emit(ToggleFullscreenEvent())
