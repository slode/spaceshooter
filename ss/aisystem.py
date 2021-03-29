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
        self.registry.remove_component(e, DownAccel)
        self.registry.remove_component(e, UpAccel)

        if ai_pos.y - 10 < target_pos.y:
            self.registry.add_component(e, DownAccel())
        elif ai_pos.y + 10 > target_pos.y:    
            self.registry.add_component(e, UpAccel())

    def horizontal_chase(self, e, ai_pos, target_pos):
        self.registry.remove_component(e, LeftAccel)
        self.registry.remove_component(e, RightAccel)

        if ai_pos.x -10  < target_pos.x:
            self.registry.add_component(e, RightAccel())
            print("A")
            print(self.registry.get_entity(e, LeftAccel, RightAccel))
        elif ai_pos.x - 10 > target_pos.x:
            self.registry.add_component(e, LeftAccel())
            print(self.registry.get_entity(e, LeftAccel, RightAccel))
            print("B")

    def shoot(self, e, ai_pos, target_pos):
        if target_pos.x - 10 < ai_pos.x < target_pos.x + 10:
            self.registry.add_component(e, Shooting())
        else:
            self.registry.remove_component(e, Shooting)

    def on_ai_tick(self, aitick):
        for e, (p, ai) in self.registry.get_components(
                Position, EntityAi):

            v = Vector2d(p.x, p.y)
            targets = []
            for te, (p2, _) in self.registry.get_components(Position, Player):
                targets.append(Vector2d(p2.x, p2.y))

            if targets:
                closest = 1000
                target = None

                target = targets[0]
                for vt in targets:
                    if closest is None:
                        closest = (vt-v).length()
                        target = vt
                    elif (vt-v).length() < closest:
                        closest = (vt-v).length()
                        target = vt

                if target:
                    self.vertical_chase(e, p, target)
                    self.horizontal_chase(e, p, target)
                    self.shoot(e, p, target)


