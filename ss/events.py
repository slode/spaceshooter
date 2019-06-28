from triton.ecs import Event

# Event components
class CollisionEvent(Event):
    pass
class DieEvent(Event):
    pass
class GameStartEvent(Event):
    pass
class NextLevelEvent(Event):
    pass

class ToggleFullscreenEvent(Event):
    pass

class AccelEvent(Event):
    FW=1
    BW=2
    LT=3
    RG=4
    def __init__(self, entity, direction, on=0):
        self.entity = entity
        self.direction = direction
        self.on = on

class ShootEvent(Event):
    def __init__(self, entity):
        self.entity = entity

class GameExitEvent(Event):
    pass

class TickEvent(Event):
    pass

class AnimationTickEvent(Event):
    pass

class EntityStateEvent(Event):
    def __init__(self, entity):
        self.entity = entity
