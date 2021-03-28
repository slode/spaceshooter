from triton.ecs import System
from triton.vector2d import *

from .events import *
from .components import *

class AiTick(Event):
    pass

class AiSystem(System):
    def initialize(self):
        self.on(TickEvent, self.on_ai_tick)

    def vertical_chase(self, e, ai_pos, target_pos):
        self.registry.remove_component(e, UpAccel())
        self.registry.remove_component(e, DownAccel())

        if ai_pos.y < target_pos.y:
            self.registry.add_component(e, UpAccel())

    def horizontal_chase(self, e, ai_pos, target_pos):
        self.registry.remove_component(e, LeftAccel())
        self.registry.remove_component(e, RightAccel())

        if ai_pos.x  < target_pos.x:
            self.registry.add_component(e, RightAccel())
        elif ai_pos.x > target_pos.x:
            self.registry.add_component(e, LeftAccel())

    def on_ai_tick(self, aitick):
        for e, (p, ai) in self.registry.get_components(
                Position, EntityAi):

            v = Vector2d(p.x, p.y)
            targets = []
            for te, (p, _) in self.registry.get_components(Position, Player):
                targets.append(Vector2d(p.x, p.y))

            if targets:
                closest = None
                target = None

                for vt in targets:
                    if closest is None or (vt-v).length() < closest:
                        closest = (vt-v).length()
                        target = vt

                if target:
                    self.vertical_chase(e, p, target)
                    self.horizontal_chase(e, p, target)


