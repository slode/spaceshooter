from triton.ecs import Registry, Component, System

#from ss.sprites import SpriteLoader

from ss.events import *
from ss.components import *

from ss.aisystem import AiSystem
from ss.inputsystem import InputSystem
from ss.rendersystem import RenderSystem
from ss.damagesystem import DamageSystem
from ss.animationsystem import AnimationSystem
from ss.collisionsystem import CollisionSystem
from ss.gamestatesystem import GameStateSystem
from ss.projectilesystem import ProjectileSystem
from ss.screenwrapsystem import ScreenwrapSystem
from ss.simulationsystem import SimulationSystem

import pygame

def main():
    registry = Registry()
    registry.add_system(InputSystem())
    registry.add_system(AiSystem())
    registry.add_system(SimulationSystem())
    registry.add_system(ScreenwrapSystem())
    registry.add_system(CollisionSystem())
    registry.add_system(ProjectileSystem())
    animation_system = registry.add_system(AnimationSystem())
    registry.add_system(RenderSystem())
    registry.add_system(DamageSystem())
    registry.add_system(GameStateSystem())

    from ss.animationsystem import sprite_by_slices, generate_grid, AnimationEvent

    animation_system.add_sprite("spaceship",
            sprite_by_slices(
                filename="res/spaceship.gif",
                slices = {
                    AnimationEvent.UPLEFT:    [(0, 40, 30, 45),  (0, 86, 30, 45)],
                    AnimationEvent.UPCENTER:  [(40, 40, 40, 45), (40, 86, 40, 45)],
                    AnimationEvent.UPRIGHT:   [(85, 40, 30, 45), (85, 86, 30, 45)],
                    AnimationEvent.LEFT:      [(0, 40, 30, 45),  (0, 86, 30, 45)],
                    AnimationEvent.DEFAULT:   [(40, 40, 40, 45), (40, 86, 40, 45)],
                    AnimationEvent.RIGHT:     [(85, 40, 30, 45), (85, 86, 30, 45)],
                    AnimationEvent.BACKLEFT:  [(0, 0, 30, 40)],
                    AnimationEvent.BACKCENTER:[(40, 0, 40, 40)],
                    AnimationEvent.BACKRIGHT: [(85, 0, 30, 40)]
            }))

    animation_system.add_sprite("explosion",
            sprite_by_slices(
                filename="res/explosion.png",
                slices = {
                    AnimationEvent.DEFAULT: generate_grid(slice_size=(96, 96), grid_size=(5, 4))
            }))

    animation_system.add_sprite("rocket",
            sprite_by_slices(
                filename="res/rocket.bmp",
                slices = {AnimationEvent.DEFAULT: [(0, 0, 15, 50), (0, 15, 15, 50)]
            }))

    import pygame

    registry.add_entity(
            Player(keymap={
                pygame.K_UP: UpAccel(),
                pygame.K_DOWN: DownAccel(),
                pygame.K_RIGHT: RightAccel(),
                pygame.K_LEFT: LeftAccel(),
                pygame.K_SPACE: Shooting()
            }),
            Position(x=50, y=50),
            Velocity(),
            Health(health=50),
            Weapon(),
            Collidable(),
            Animatable("spaceship"),
            Renderable())

    registry.add_entity(
            Player(keymap={
                pygame.K_w: UpAccel(),
                pygame.K_s: DownAccel(),
                pygame.K_d: RightAccel(),
                pygame.K_a: LeftAccel(),
                pygame.K_e: Shooting()
            }),
            Position(x=100, y=100),
            Velocity(),
            Health(health=50),
            Weapon(),
            Collidable(),
            Animatable("spaceship"),
            Renderable())

    registry.add_entity(
            EntityAi(),
            Position(),
            UpAccel(),
            Velocity(),
            Health(health=50),
            Weapon(),
            Collidable(team=2),
            Animatable("spaceship"),
            Renderable()
            )

    gamestate = GameState()
    registry.add_entity(gamestate)
    while gamestate.running:
        registry.process()

main()
