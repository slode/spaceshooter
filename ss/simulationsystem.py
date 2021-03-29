from triton.ecs import System

from .events import *
from .components import *

class SimulationTickEvent(Event):
    pass

class SimulationSystem(System):
    def initialize(self):
        self.on(TickEvent, self.update)
        self.on(SimulationTickEvent, self.sim_update)

        self._last_update = 0.0

    def update(self, _):
        for e, (g,) in self.registry.get_components(
                GameState):
            if g.t - self._last_update > 1000/60:
                self._last_update = g.t
                self.emit(SimulationTickEvent())

    def sim_update(self, _):
        dt = 0.01
        for e, (g,) in self.registry.get_components(GameState):
            dt = g.dt

        for e, [v,] in self.registry.get_components(Velocity):
            [up, down, left, right] = self.registry.get_entity(
                    e, UpAccel, DownAccel, LeftAccel, RightAccel)
            ay = -1.0 if up    else 0.0
            ay += 1.0 if down  else 0.0
            ax =  1.0 if right else 0.0
            ax -= 1.0 if left  else 0.0

            v.y += ay * dt / 100.0
            v.x += ax * dt / 100.0
            v.y = max(min(v.y, v.max_speed), -v.max_speed)
            v.x = max(min(v.x, v.max_speed), -v.max_speed)

        for e, (p, v) in self.registry.get_components(
                Position, Velocity):
            att = v.attenuation
            v.x *= att
            v.y *= att
            p.x += v.x * dt
            p.y += v.y * dt

