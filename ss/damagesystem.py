from triton.ecs import System

from .events import *
from .components import *

from .animationsystem import AnimationStopEvent

class DamageSystem(System):
    def initialize(self):
        self.on(TickEvent, self.update)
        self.on(CollisionEvent, self.on_collision)
        self.on(SecondTickEvent, self.update_cooldown)
        self.on(AnimationStopEvent, self.remove_dead_items)

    def remove_dead_items(self, ev):
        [p1, v1, h1] = self.registry.get_entity(ev.entity, Position, Velocity, Health)
        if h1 is None or h1.health <= 0:
            self.registry.remove_entity(ev.entity)

    def update_cooldown(self, _):
        pass

    def on_collision(self, event):
        [p1, v1, h1] = self.registry.get_entity(event.entity1, Position, Velocity, Health)
        [p2, v2, h2] = self.registry.get_entity(event.entity2, Position, Velocity, Health)

        if h1 is None or h2 is None:
            return 

        damage = min(h1.health, h2.health)
        h1.health -= damage
        h2.health -= damage

        if h1.health <= 0:
            self.registry.remove_component(event.entity1, Collidable)
            self.registry.add_entity(
                    Position(x=p1.x, y=p1.y),
                    Velocity(x=v1.x, y=v1.y),
                    Movable(),
                    Renderable(),
                    Animatable("explosion", loopable=False))

        if h2.health <= 0:
            self.registry.remove_component(event.entity2, Collidable)
            self.registry.add_entity(
                    Position(x=p2.x, y=p2.y),
                    Velocity(x=v2.x, y=v2.y),
                    Movable(),
                    Renderable(),
                    Animatable("explosion", loopable=False))

    def update(self, _):
        pass
