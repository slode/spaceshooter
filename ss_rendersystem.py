import pygame
import pygame.gfxdraw

class RenderSystem(System):
    def initialize(self):
        self.screen = None
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.on(TickEvent, self.update)
        self.on(ToggleFullscreenEvent, self.toggle_fullscreen)
        self.toggle_fullscreen(None)

    def toggle_fullscreen(self, _):
        self.screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        if self.screen is not None and self.screen.get_flags() & pygame.FULLSCREEN:
            self.screen = pygame.display.set_mode(self.screen_size, pygame.DOUBLEBUF, 32)
        else:
            self.screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN | pygame.DOUBLEBUF, 32)

        for e, (g,) in self.registry.get_components(
                GameState):
            g.screen_size = self.screen_size

    def update(self, _):
        self.screen.fill((100,100,100))

        for e, (p, a) in self.registry.get_components(
                Position, Animatable):
            if a.image is None:
                continue
            self.screen.blit(
                a.image,
                a.rect)

        pygame.display.update()
        dt = self.clock.tick(self.FPS)
        for e, (g,) in self.registry.get_components(
                GameState):
            g.dt = dt
            g.t += dt
            g.screen_size = self.screen_size
