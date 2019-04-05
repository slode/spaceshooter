from triton.ecs import Registry, Component, System

import pygame

class Controllable(Component):
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
    def __init__(self, x=0, y=0, attenuation=0.9):
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

class Animatable(Component):
    def __init__(self, sprite=0):
        self.sprite_entity = sprite
        self.frame_rate = 30.0
        self.frame_index = 0
        self.last_frame = 0
        self.image = None
        self.rect = None

class Sprite(Component):
    def __init__(self, filename="spaceship.gif", rects=[]):
        rects=[(40, 40, 40, 45),
               (40, 86, 40, 45)]
        ss = spritesheet(filename)
        self.sprites = ss.images_at(rects, colorkey=-1)

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
        self.status = "RUNNING"
        self.t = 0
        self.dt = 1.0

# Event components
class ShootEvent(Component):
    pass
class CollisionEvent(Component):
    pass
class DieEvent(Component):
    pass
class GameStartEvent(Component):
    pass
class GameExitEvent(Component):
    pass
class NextLevelEvent(Component):
    pass

# Systems
class InputSystem(System):
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.registry.add_entity(GameExitEvent())
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.registry.add_entity(GameExitEvent())
                    break

            for e, [c, m] in self.registry.get_components(Controllable, Movable):
                # TODO: fix this logic.
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_UP:
                        m.forward = 1
                    elif event.key == pygame.K_DOWN:
                        m.backward = 1
                    elif event.key == pygame.K_LEFT:
                        m.left = 1
                    elif event.key == pygame.K_RIGHT:
                        m.right = 1
                    elif event.key == pygame.K_SPACE:
                        self.registry.add_component(e, ShootEvent())
                elif event.type == pygame.KEYUP: 
                    if event.key == pygame.K_UP:
                        m.forward = 0
                    elif event.key == pygame.K_DOWN:
                        m.backward = 0
                    elif event.key == pygame.K_LEFT:
                        m.left = 0
                    elif event.key == pygame.K_RIGHT:
                        m.right = 0

class ProjectileSystem(System):
    def update(self):
        for e, (p, w) in self.registry.get_components(
                Position, Weapon):
            if w.countdown > 0:
                w.countdown -= 1

        for e, (p, w, s) in self.registry.get_components(
                Position, Weapon, ShootEvent):
            if w.countdown <= 0:
                w.countdown = w.cooldown
                self.registry.add_entity(
                        Position(x=p.x, y=p.y),
                        Velocity(y=-1),
                        Movable(forward=1),
                        Renderable(),
                        Collidable())

        for e, (s,) in self.registry.get_components(
                ShootEvent):
            self.registry.remove_component(e, s)

class SimulationSystem(System):
    def update(self):
        dt = 0.01
        for e, (g,) in self.registry.get_components(
                GameState):
            dt = g.dt

        inv_dt = dt/1000.0

        for e, (v, m) in self.registry.get_components(
                Velocity, Movable):
            v.y += (m.backward-m.forward)*10*dt
            v.x += (m.right-m.left)*10*dt

        for e, (p, v) in self.registry.get_components(
                Position, Velocity):
            att = v.attenuation
            v.x *= att
            v.y *= att
            p.x += v.x*inv_dt
            p.y += v.y*inv_dt
            
from sprites import spritesheet
class AnimationSystem(System):
    def __init__(self):
        pass

    def update(self):
        for e, (g,) in self.registry.get_components(
                GameState):
            t = g.t

        for e, (p, a, m) in self.registry.get_components(
                Position, Animatable, Movable):
            
            if a.image is None or (t - a.last_frame) > a.frame_rate:
                [s] = self.registry.get_entity(a.sprite_entity, Sprite)
                a.image = s.sprites[a.frame_index]
                a.rect = a.image.get_rect()
                a.last_frame = t
                a.frame_index = (a.frame_index + 1) % len(s.sprites)
                a.rect.center = (p.x, p.y)

import pygame.gfxdraw
class RenderSystem(System):
    def __init__(self):
        self.screen_size = (800, 800)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.fullscreen = False
        self.FPS = 160

    def update(self):
        self.screen.fill((100,100,100))

        for e, (p, r, a) in self.registry.get_components(
                Position, Renderable, Animatable):
            self.screen.blit(
                a.image,
                a.rect)

        pygame.display.update()
        dt = self.clock.tick(self.FPS)
        for e, (g,) in self.registry.get_components(
                GameState):
            g.dt = dt
            g.t += dt

class CollisionSystem(System):
    pass

class ScreenwrapSystem(System):
    def update(self):
        for e, (p, v) in self.registry.get_components(
                Position, Velocity):
            if p.x < 0:
                p.x = 800
            elif p.x > 800:
                p.x = 0
            if p.y < 0:
                p.y = 800
            elif p.y > 800:
                p.y = 0


class DamageSystem(System):
    def update(self):
        pass

class GameStateSystem(System):
    def update(self):
        for e, (g) in self.registry.get_components(
                GameExitEvent):
            pygame.quit()

def main():
    pygame.init()
    registry = Registry()
    registry.add_system(InputSystem())
    registry.add_system(SimulationSystem())
    #registry.add_system(CollisionSystem())
    registry.add_system(ScreenwrapSystem())
    registry.add_system(DamageSystem())
    registry.add_system(ProjectileSystem())
    registry.add_system(AnimationSystem())
    registry.add_system(RenderSystem())
    registry.add_system(GameStateSystem())

    registry.add_entity(GameState())
    sprite_id=registry.add_entity(Sprite())

    registry.add_entity(
            Position(),
            Velocity(),
            Health(),
            Weapon(),
            Movable(),
            Controllable(),
            Animatable(sprite = sprite_id),
            Renderable())

    registry.add_entity(
            Position(),
            Velocity(),
            Health(),
            Weapon(),
            Movable(),
            Animatable(sprite = sprite_id),
            Renderable())

    while not any(registry.get_components(GameExitEvent)):
        registry.update()

main()
