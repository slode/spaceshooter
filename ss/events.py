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

class AnimationEvent(Event):
    UPLEFT=1
    UPCENTER=2
    UPRIGHT=3
    LEFT=4
    DEFAULT=5
    RIGHT=6
    BACKLEFT=7
    BACKCENTER=8
    BACKRIGHT=9
    SHOOTING=10
    EXPLODING=11
    
    def __init__(self, entity, state=DEFAULT):
        self.entity = entity
        self.state = state

class AnimationStopEvent(Event):
    def __init__(self, entity):
        self.entity = entity

class AnimationTickEvent(Event):
    pass
