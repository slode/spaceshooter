from triton.ecs import System
from triton.vector2d import Vector2d

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
        try:
            [p1, v1, h1] = self.registry.get_entity(event.entity1, Position, Velocity, Health)
            [p2, v2, h2] = self.registry.get_entity(event.entity2, Position, Velocity, Health)
        except KeyError:
            return

        if h1 is None or h2 is None:
            return 

        damage = min(h1.health, h2.health)
        h1.health -= damage
        h2.health -= damage

        if h1.health <= 0:
            self.registry.remove_entity(event.entity1)

        if h2.health <= 0:
            self.registry.remove_entity(event.entity2)

        if h2.health <= 0 or h1.health <= 0:
            p_avg = Vector2d(p1.x+p2.x, p1.y+p2.y)/2
            v_avg = Vector2d(v1.x+v2.x, v1.y+v2.y)/2
            self.registry.add_entity(
                    Position(x=p_avg.x, y=p_avg.y),
                    Velocity(x=v_avg.x, y=v_avg.y),
                    Health(health=0),
                    Renderable(),
                    Animatable("explosion", loopable=False, frame_rate=10))

    def update(self, _):
        pass
