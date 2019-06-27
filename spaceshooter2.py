from triton.ecs import Registry, Component, System

from ss_events import *
from ss_components import *

from ss_aisystem import AiSystem
from ss_inputsystem import InputSystem
from ss_rendersystem import RenderSystem
from ss_damagesystem import DamageSystem
from ss_animationsystem import AnimationSystem
from ss_collisionsystem import CollisionSystem
from ss_gamestatesystem import GameStateSystem
from ss_projectilesystem import ProjectileSystem
from ss_screenwrapsystem import ScreenwrapSystem
from ss_simulationsystem import SimulationSystem

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
            SpriteSheet(filename="spaceship.gif",
            BWCT=[(40, 0, 40, 40)],
            FWCT=[(40, 40, 40, 45),
                (40, 86, 40, 45)],
            BWLT=[(0, 0, 30, 40)],
            FWLT=[(0, 40, 30, 45),
                  (0, 86, 30, 45)],
            BWRG=[(85, 0, 30, 40)],
            FWRG=[(85, 40, 30, 45),
                  (85, 86, 30, 45)]))

    registry.add_entity(
            Position(x=50, y=50),
            Velocity(),
            Health(),
            Weapon(),
            Movable(),
            PlayerOne(),
            Animatable(ship_sprite),
            Renderable())

    registry.add_entity(
            Position(),
            Velocity(),
            Health(),
            Weapon(),
            PlayerTwo(),
            Movable(),
            Animatable(ship_sprite),
            Renderable())

    gamestate = GameState()
    registry.add_entity(gamestate)
    while gamestate.running:
        registry.process()

main()
