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
    registry.add_system(DamageSystem())
    registry.add_system(ProjectileSystem())
    registry.add_system(AnimationSystem())
    registry.add_system(RenderSystem())
    registry.add_system(GameStateSystem())


    ship_sprite=registry.add_entity(
            SpriteSheet(filename="res/spaceship.gif",
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
                }
    ))

    registry.add_entity(
            PlayerOne(),
            Position(x=50, y=50),
            Velocity(),
            Health(),
            Weapon(),
            Movable(),
            Collidable(),
            Animatable(ship_sprite),
            Renderable())

    registry.add_entity(
            PlayerTwo(),
            Position(),
            Velocity(),
            Health(),
            Weapon(),
            Movable(),
            Collidable(),
            Animatable(ship_sprite),
            Renderable())

    gamestate = GameState()
    registry.add_entity(gamestate)
    while gamestate.running:
        registry.process()

main()
