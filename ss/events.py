from triton.ecs import Event

# Event components
class CollisionEvent(Event):
    def __init__(self, ent1, ent2):
        self.entity1 = ent1
        self.entity2 = ent2

class GameStartEvent(Event):
    pass

class NextLevelEvent(Event):
    pass

class ToggleFullscreenEvent(Event):
    pass

class GameExitEvent(Event):
    pass

class TickEvent(Event):
    pass

class SecondTickEvent(Event):
    pass
