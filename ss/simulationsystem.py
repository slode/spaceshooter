from triton.ecs import System

from .events import *
from .components import *

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

        if m.backward - m.forward > 0:
            if m.right - m.left > 0:
                self.emit(AnimationEvent(accel.entity, AnimationEvent.BACKRIGHT))
            elif m.right - m.left < 0:
                self.emit(AnimationEvent(accel.entity, AnimationEvent.BACKLEFT))
            else:
                self.emit(AnimationEvent(accel.entity, AnimationEvent.BACKCENTER))
        elif m.backward - m.forward < 0:
            if m.right - m.left > 0:
                self.emit(AnimationEvent(accel.entity, AnimationEvent.UPRIGHT))
            elif m.right - m.left < 0:
                self.emit(AnimationEvent(accel.entity, AnimationEvent.UPLEFT))
            else:
                self.emit(AnimationEvent(accel.entity, AnimationEvent.UPCENTER))
        else:
            if m.right - m.left > 0:
                self.emit(AnimationEvent(accel.entity, AnimationEvent.RIGHT))
            elif m.right - m.left < 0:
                self.emit(AnimationEvent(accel.entity, AnimationEvent.LEFT))
            else:
                self.emit(AnimationEvent(accel.entity, AnimationEvent.DEFAULT))


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

