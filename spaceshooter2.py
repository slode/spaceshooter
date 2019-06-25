from triton.ecs import Registry, Component, System
from ss_events import *
from ss_inputsystem import *

import pygame

class PlayerOne(Component):
    pass

class PlayerTwo(Component):
    pass

class Movable(Component):
    def __init__(self, forward=0, backward=0, left=0, right=0):
        self.forward = forward
        self.backward = backward
        self.left = left
        self.right = right

class Position(Component):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Velocity(Component):
    def __init__(self, x=0, y=0, attenuation=0.90):
        self.attenuation = attenuation
        self.x = x
        self.y = y

class Orientation(Component):
    def __init__(self, direction=1):
        self.direction = direction

class Weapon(Component):
    def __init__(self, damage=10, cooldown=3):
        self.damage = damage
        self.cooldown = cooldown
        self.countdown = 0

class AnimationStrip:
    def __init__(self):
        pass

class Animatable(Component):
    def __init__(self, sprite_sheet):
        self.sprite_sheet = sprite_sheet
        self.frame_rate = 30.0
        self.frame_index = 0
        self.previous_frame = 0
        self.image = None
        self.rect = None
        self.sprites = None

from sprites import spritesheet
class SpriteSheet(Component):
    def __init__(self, filename=None, **slices):
        ss = spritesheet(filename)
        self.sprites = {}
        for k,v in slices.items():
            self.sprites[k] = ss.images_at(v, colorkey=-1)

class Renderable(Component):
    pass

class Health(Component):
    def __init__(self, health=10):
        self.health = 10

class Collidable(Component):
    def __init__(self):
        self.rect = None

class GameState(Component):
    def __init__(self):
        self.running = True
        self.t = 0
        self.dt = 1.0
        self.screen_size = (0,0)



class ProjectileSystem(System):
    def initialize(self):
        self.on(TickEvent, self.handle_cooldowns)
        self.on(ShootEvent, self.on_shootevent)

    def handle_cooldowns(self, event):
        for e, (g,) in self.registry.get_components(
                GameState):
            dt = g.dt/1000

        for e, (p, w) in self.registry.get_components(
                Position, Weapon):
            if w.countdown > 0:
                w.countdown -= dt

    def on_shootevent(self, event):
        (p, w) = self.registry.get_entity(
                event.entity,
                Position, Weapon)
        if w.countdown <= 0:
            w.countdown = w.cooldown
            self.registry.add_entity(
                    Position(x=p.x, y=p.y),
                    Velocity(y=-1),
                    Movable(forward=1),
                    Renderable(),
                    Collidable())

class SimulationSystem(System):
    def initialize(self):
        self.on(AccelEvent, self.on_accel)
        self.on(TickEvent, self.update)

    def on_accel(self, accel):
        (v, m) = self.registry.get_entity(
                accel.entity,
                Velocity, Movable)
        if accel.direction == AccelEvent.FW:
            m.forward = accel.on
        elif accel.direction == AccelEvent.BW:
            m.backward = accel.on
        elif accel.direction == AccelEvent.LT:
            m.left = accel.on
        elif accel.direction == AccelEvent.RG:
            m.right = accel.on

    def update(self, _):
        dt = 0.01
        for e, (g,) in self.registry.get_components(
                GameState):
            dt = g.dt

        for e, (v, m) in self.registry.get_components(
                Velocity, Movable):
            v.y += (m.backward-m.forward)*dt/100.0
            v.x += (m.right-m.left)*dt/100.0

        for e, (p, v) in self.registry.get_components(
                Position, Velocity):
            att = v.attenuation
            v.x *= att
            v.y *= att
            p.x += v.x * dt
            p.y += v.y * dt
            
class AnimationSystem(System):
    def initialize(self):
        self.on(AnimationTickEvent, self.update)
        self.on(AccelEvent, self.on_accel)

    def on_accel(self, accel):
        [a, m] = self.registry.get_entity(
                accel.entity, Animatable, Movable)
        [s] = self.registry.get_entity(
                a.sprite_sheet, SpriteSheet)

        sprite_key = []
        if m.backward == 1:
            sprite_key.append("BW")
        else:
            sprite_key.append("FW")
        
        if m.left == m.right:
            sprite_key.append("CT")
        elif m.left == 1:
            sprite_key.append("LT")
        else:
            sprite_key.append("RG")

        key = "".join(sprite_key)
        if key in s.sprites:
            a.sprites = s.sprites[key]

    def update(self, _):
        for e, (g,) in self.registry.get_components(
                GameState):
            t = g.t

        for e, (p, a) in self.registry.get_components(
                Position, Animatable):
            
            if a.sprites is None:
                [s] = self.registry.get_entity(
                        a.sprite_sheet, SpriteSheet)
                a.sprites = s.sprites["FWCT"]
            
            if  (t - a.previous_frame) > a.frame_rate:
                a.previous_frame = t
                a.frame_index = (a.frame_index + 1) % len(a.sprites)
                a.image = a.sprites[a.frame_index]
                a.rect = a.image.get_rect()
                a.rect.center = (p.x, p.y)


class CollisionSystem(System):
    pass

class ScreenwrapSystem(System):
    def initialize(self):
        self.on(TickEvent, self.update)

    def update(self, _):
        for e, (p, v) in self.registry.get_components(
                Position, Velocity):
            for e, (g,) in self.registry.get_components(
                    GameState):
                if p.x < 0:
                    p.x = g.screen_size[0]
                elif p.x > g.screen_size[0]:
                    p.x = 0
                if p.y < 0:
                    p.y = g.screen_size[1]
                elif p.y > g.screen_size[1]:
                    p.y = 0

class DamageSystem(System):
    def initialize(self):
        self.on(TickEvent, self.update)

    def update(self, _):
        pass

class GameStateSystem(System):
    def initialize(self):
        self.on(TickEvent, self.update)
        self.on(GameExitEvent, self.exit)
        self.emit(TickEvent())

    def exit(self, _):
        for e, (g,) in self.registry.get_components(
                GameState):
            g.running = False

    def update(self, _):
        self.emit(TickEvent())
        self.emit(AnimationTickEvent())

def main():
    pygame.init()
    registry = Registry()
    registry.add_system(GameStateSystem())
    registry.add_system(InputSystem())
    registry.add_system(SimulationSystem())
    #registry.add_system(CollisionSystem())
    registry.add_system(ScreenwrapSystem())
    registry.add_system(DamageSystem())
    registry.add_system(ProjectileSystem())
    registry.add_system(AnimationSystem())
    registry.add_system(RenderSystem())


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
            Movable(),
            PlayerOne(),
            Animatable(ship_sprite),
            Renderable())

    for i in range(100):
        registry.add_entity(
                Position(x=10+i*10, y=10+i*10),
                Velocity(),
                Health(),
                Weapon(),
                Movable(),
                PlayerTwo(),
                Animatable(ship_sprite),
                Renderable())

    registry.add_entity(
            Position(),
            Velocity(),
            Health(),
            Weapon(),
            Movable(),
            Animatable(ship_sprite),
            Renderable())

    gamestate = GameState()
    registry.add_entity(gamestate)
    while gamestate.running:
        registry.process()

    pygame.quit()
main()
