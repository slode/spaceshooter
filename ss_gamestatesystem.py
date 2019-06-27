from triton.ecs import System

from ss_events import *
from ss_components import *

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

