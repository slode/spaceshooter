import pygame
from triton.ecs import System
from events import *
from components import PlayerOne, PlayerTwo, Movable

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
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.emit(GameExitEvent())
                    break

            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_u:
                    self.emit(ToggleFullscreenEvent())
            for e, [c, m] in self.registry.get_components(PlayerOne, Movable):
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_UP:
                        self.emit(AccelEvent(e, AccelEvent.FW, 1))
                    elif event.key == pygame.K_DOWN:
                        self.emit(AccelEvent(e, AccelEvent.BW, 1))
                    elif event.key == pygame.K_LEFT:
                        self.emit(AccelEvent(e, AccelEvent.LT, 1))
                    elif event.key == pygame.K_RIGHT:
                        self.emit(AccelEvent(e, AccelEvent.RG, 1))
                    elif event.key == pygame.K_SPACE:
                        self.emit(ShootEvent(e))
                elif event.type == pygame.KEYUP: 
                    if event.key == pygame.K_UP:
                        self.emit(AccelEvent(e, AccelEvent.FW, 0))
                    elif event.key == pygame.K_DOWN:
                        self.emit(AccelEvent(e, AccelEvent.BW, 0))
                    elif event.key == pygame.K_LEFT:
                        self.emit(AccelEvent(e, AccelEvent.LT, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.emit(AccelEvent(e, AccelEvent.RG, 0))

            for e, [c, m] in self.registry.get_components(PlayerTwo, Movable):
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_w:
                        self.emit(AccelEvent(e, AccelEvent.FW, 1))
                    elif event.key == pygame.K_s:
                        self.emit(AccelEvent(e, AccelEvent.BW, 1))
                    elif event.key == pygame.K_a:
                        self.emit(AccelEvent(e, AccelEvent.LT, 1))
                    elif event.key == pygame.K_d:
                        self.emit(AccelEvent(e, AccelEvent.RG, 1))
                    elif event.key == pygame.K_e:
                        self.emit(ShootEvent(e))
                elif event.type == pygame.KEYUP: 
                    if event.key == pygame.K_w:
                        self.emit(AccelEvent(e, AccelEvent.FW, 0))
                    elif event.key == pygame.K_s:
                        self.emit(AccelEvent(e, AccelEvent.BW, 0))
                    elif event.key == pygame.K_a:
                        self.emit(AccelEvent(e, AccelEvent.LT, 0))
                    elif event.key == pygame.K_d:
                        self.emit(AccelEvent(e, AccelEvent.RG, 0))
