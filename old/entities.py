import random
import pygame
from pygame.locals import *
from sprites import spritesheet

class Game:
    
    def __init__(self, dim):
        self.sprites = {}
        self.dim = dim
        self.ship = None
        self.friends = []
        self.enemies = []
        self.neutral_bottom = []
        self.neutral_top = []
        self.level = 0
    
    def update(self):
        for friend in self.friends:
            for enemy in self.enemies:
                if friend.rect.colliderect(enemy.rect):
                    enemy.health = enemy.health - 1
                    friend.health = friend.health - 1
                    self.neutral_top.append(Explosion(self, enemy.rect.center))

        for entity in self.friends:
            if entity.health <= 0:
                self.friends.remove(entity)
            entity.update()

        for entity in self.enemies:
            if entity.health <= 0:
                self.enemies.remove(entity)
            entity.update()

        for entity in self.neutral_bottom:
            if entity.health <= 0:
                self.neutral_bottom.remove(entity)
            entity.update()

        for entity in self.neutral_top:
            if entity.health <= 0:
                self.neutral_top.remove(entity)
            entity.update()
        
        self.load_level()

    def draw(self, surface):
        for entity in self.neutral_bottom:
            entity.draw(surface)

        for entity in self.friends:
            entity.draw(surface)

        for entity in self.enemies:
            entity.draw(surface)

        for entity in self.neutral_top:
            entity.draw(surface)

    def reset(self):
        self.level = 0
        self.enemies = []
        self.friends = []
        self.neutral_bottom = []
        self.neutral_top = []
        self.ship = Ship(self, (self.dim[0] // 2, self.dim[1] - 100))
        self.friends.append(self.ship)
        for x in range(200):
            star = Star(self)
            self.neutral_bottom.append(star)

    def start(self):
        self.level = 1

    def finished(self):
        if self.ship.health <= 0:
            return True
        if self.level >= 4 and len(self.enemies) == 0:
            return True
        return False
    
    def success(self):
        if self.finished and self.ship.health > 0:
            return True
        return False


    def load_level(self):
        if len(self.enemies) > 0 or self.level == 0:
            return

        if self.level == 1:
            for x in range(10):
                enemy = Enemy1(self, (random.randint(0, self.dim[0]), 50))
                enemy.speed_x = random.randint(-10.0, 10.0)
                enemy.speed_y = random.randint(3.0, 10.0)
                self.enemies.append(enemy)
        elif self.level == 2:
            for x in range(10):
                enemy = Enemy2(self, (random.randint(0, self.dim[0]), 50))
                enemy.speed_x = random.randint(-10.0, 10.0)
                enemy.speed_y = random.randint(3.0, 10.0)
                self.enemies.append(enemy)
        elif self.level == 3:
            for x in range(1):
                enemy = Enemy3(self, (self.dim[0] // 2, 50))
                enemy.speed_x = random.randint(-10.0, 10.0)
                enemy.speed_y = random.randint(3.0, 10.0)
                self.enemies.append(enemy)
        self.level = self.level + 1

class Entity(object):
    spritelib = {}

    def __new__(cls, game, pos=(0,0)):
        if cls not in Entity.spritelib:
            Entity.spritelib[cls] = cls.load_images()
        cls.images = Entity.spritelib[cls]
        return super(Entity, cls).__new__(cls)

    def __init__(self, game, pos=None):
        self.game = game
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.rect = self.images[0].get_rect()
        if pos is None:
            pos = (0,0)
        self.rect.center = pos
        self.time = 0
        self.health = 1
        self.shoot_delay = 0
        self.shoot_cooldown = 0
        self.init()

    @classmethod
    def load_images(cls):
        raise NotImplemented("")

    def init(self):
        pass

    def shoot(self):
        raise NotImplementedError("")

    def load_images(self):
        raise NotImplementedError("")

    def select_image(self):
        raise NotImplementedError("")
    
    def action(self):
        pass
        
    def draw(self, surface):
        surface.blit(
            self.select_image(),
            self.rect)

    def update(self):
        self.time = self.time + 1
        current_image = self.select_image()
        self.rect.x = self.rect.x + int(self.speed_x)
        self.rect.y = self.rect.y + int(self.speed_y)
        self.shoot_delay = max(0, self.shoot_delay - 1)
        self.shoot_cooldown = max(0, self.shoot_cooldown - 1)
        self.action()

class Ship(Entity):
    
    def init(self):
        self.health = 10
        self.shoot_cooldown = 0.0

    @classmethod
    def load_images(cls):
        ss = spritesheet('spaceship.gif')
        rects = [
            (40, 0, 40, 40),
            (40, 40, 40, 45),
            (40, 86, 40, 45),
            (0, 0, 30, 40),
            (0, 40, 30, 45),
            (0, 86, 30, 45),
            (85, 0, 30, 40),
            (85, 40, 30, 45),
            (85, 86, 30, 45),
        ]
        return ss.images_at(rects, colorkey=-1)

    def action(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.game.dim[0]:
            self.rect.right = self.game.dim[0]

        if self.rect.y < 0:
            self.rect.top = 0
        elif self.rect.bottom > self.game.dim[1]:
            self.rect.bottom = self.game.dim[1]

        self.speed_x = self.speed_x * 0.90
        self.speed_y = self.speed_y * 0.90

    def shoot(self):
        if self.shoot_cooldown <= 0:
            self.game.friends.append(Rocket(self.game, self.rect.midtop))
            self.shoot_cooldown = 3
            
    def select_image(self):
        if self.speed_x <= -1.0:
            if self.speed_y <= 0.0:
                index = int(self.time*0.5) % 2 + 4
                return self.images[index]
            return self.images[3]
        elif self.speed_x >= 1.0:
            if self.speed_y <= 0.0:
                index = int(self.time*0.5) % 2 + 7
                return self.images[index]
            return self.images[6]
        else:
            if self.speed_y <= 0.0:
                index = int(self.time*0.5) % 2 + 1
                return self.images[index]
            return self.images[0]

class Rocket(Entity):
    def init(self):
        self.speed_y = -10.0

    @classmethod    
    def load_images(cls):
        ss = spritesheet('rocket.bmp')
        rects = [
            (0, 0, 15, 50),        
        ]
        images = ss.load_strip(rects[0], 2, colorkey=-1)
        return images

    def select_image(self):
        image = self.images[int(self.time*0.5) % 2]
        return image

    def action(self):
        # Kill at screen exit
        if self.rect.x < 0:
            self.health = 0
        elif self.rect.right > self.game.dim[0]:
            self.health = 0

        if self.rect.y < 0:
            self.health = 0
        elif self.rect.bottom > self.game.dim[1]:
            self.health = 0

        self.speed_y = self.speed_y * 1.03

class RocketEnemy(Rocket):
    def init(self):
        self.speed_y = 10.0

    @classmethod    
    def load_images(cls):
        ss = spritesheet('enemy.png')
        rects = [
            (423, 260, 26, 50),
        ]
        images = ss.load_strip(rects[0], 2, colorkey=-1)
        return images

    def select_image(self):
        image = self.images[int(self.time*0.5) % 2 ]
        return image


class Explosion(Entity):
    @classmethod    
    def load_images(cls):
        ss = spritesheet('explosion1.png')
        spritesize = 96
        images = ss.load_grid(
            (0, 0, spritesize, spritesize),
            (5,4),
            colorkey=-1)
        return images

    def select_image(self):
        index = int(self.time*0.5) % len(self.images)
        if index == len(self.images) - 1:
            self.health = 0
        return self.images[index]

class Star(Entity):
    images = None
    
    def init(self):
        self.time = random.randint(1, 20)
        self.default_speed_y = random.randint(3, 10)
        self.rect.center = (
            random.randint(0, self.game.dim[0]),
            random.randint(0, self.game.dim[1]))

    @classmethod
    def load_images(cls):
        ss = spritesheet('stars.png')
        rects = [
            (0, 10 * random.randint(0, 3), 10, 10),        
        ]
        images = ss.load_strip(rects[0], 10, colorkey=-1)
        return images

    def select_image(self):
        index = int(self.time*0.5) % len(self.images)
        return self.images[index]

    def action(self):
        # wrap screen
        if self.rect.left < 0:
            self.rect.right = self.game.dim[0]
        elif self.rect.right > self.game.dim[0]:
            self.rect.left = 0 

        if self.rect.top < 0:
            self.rect.bottom = self.game.dim[1]
        elif self.rect.bottom > self.game.dim[1]:
            self.rect.top = 0
        
        # accel counter to ship
        self.speed_x = -self.game.ship.speed_x
        self.speed_y = self.default_speed_y - self.game.ship.speed_y

class Enemy1(Entity):
    def init(self):
        self.shoot_cooldown = random.randint(2, 40)

    @classmethod
    def load_images(cls):
        ss = spritesheet('enemy.png')
        rects = [
            (527, 500, 55, 50), # normal
            (528, 557, 55, 50), # shoot
        ]
        images = ss.images_at(rects, colorkey=-1)
        return images

    def select_image(self):
        if self.shoot_delay > 1:
            return self.images[1]
        
        return self.images[0]

    def shoot(self):
        if self.shoot_delay == 1:
            self.shoot_cooldown = 40
            r = RocketEnemy(self.game, self.rect.midbottom)
            r.speed_y = 10.0
            self.game.enemies.append(r)

        if self.shoot_delay <= 0 and self.shoot_cooldown <= 0:
            self.shoot_delay = 2

    def action(self):
        self.shoot()

        if self.rect.left < 0:
            self.rect.right = self.game.dim[0]
        elif self.rect.right > self.game.dim[0]:
            self.rect.left = 0 

        if self.rect.top < 0:
            self.rect.bottom = self.game.dim[1]
        elif self.rect.bottom > self.game.dim[1]:
            self.rect.top = 0

class Enemy2(Entity):
    def init(self):
        self.shoot_cooldown = random.randint(2, 30)

    @classmethod
    def load_images(cls):
        ss = spritesheet('enemy.png')
        rects = [
            (144, 526, 65, 55), # normal
            (175, 592, 65, 55), # normal
            (212, 526, 65, 55), # shoot
        ]
        images = ss.images_at(rects, colorkey=-1)
        return images

    def select_image(self):
        if self.shoot_delay > 1:
            return self.images[2]

        return self.images[int(self.time*0.5) % 2]

    def shoot(self):
        if self.shoot_delay == 1:
            self.shoot_cooldown = 30
            r = RocketEnemy(self.game, self.rect.midbottom)
            r.speed_y = 10.0
            self.game.enemies.append(r)

        if self.shoot_delay <= 0 and self.shoot_cooldown <= 0:
            self.shoot_delay = 3


    def action(self):
        self.shoot()

        if self.rect.left < 0:
            self.rect.right = self.game.dim[0]
        elif self.rect.right > self.game.dim[0]:
            self.rect.left = 0 

        if self.rect.top < 0:
            self.rect.bottom = self.game.dim[1]
        elif self.rect.bottom > self.game.dim[1]:
            self.rect.top = 0

class Enemy3(Entity):
    def init(self):
        self.health = 10
        self.firechance = 15
        self.spread = 3

    @classmethod        
    def load_images(cls):
        ss = spritesheet('enemy.png')
        rects = [
            (530, 345, 180, 150),
        ]
        images = ss.images_at(rects, colorkey=-1)
        return images

    def select_image(self):
        return self.images[0]

    def shoot(self):
        if self.shoot_delay == 1:
            self.shoot_cooldown = 2
            for i in range(4):
                if random.randint(0, 99) > self.firechance:
                    continue
                pos = self.rect.midbottom
                pos = (pos[0] - 40 - 5 * i, pos[1] - 30)
                r = RocketEnemy(self.game, pos)
                r.speed_x = random.randint(-self.spread, self.spread)
                self.game.enemies.append(r)

            for i in range(4):
                if random.randint(0, 99) > self.firechance:
                    continue
                pos = self.rect.midbottom
                pos = (pos[0] + 50 + 5 * i, pos[1] - 30)
                r = RocketEnemy(self.game, pos)
                r.speed_x = random.randint(-self.spread, self.spread)
                self.game.enemies.append(r)

        if self.shoot_delay <= 0 and self.shoot_cooldown <= 0:
            self.shoot_delay = 3
            
    def action(self):
        self.shoot()

        # wrap screen
        if self.rect.left < 0:
            self.rect.right = self.game.dim[0]
        elif self.rect.right > self.game.dim[0]:
            self.rect.left = 0 

        if self.rect.top < 0:
            self.rect.bottom = self.game.dim[1]
        elif self.rect.bottom > self.game.dim[1]:
            self.rect.top = 0

        # change direction
        if random.randint(0,999) >= 950:
            self.speed_x = random.randint(-10.0, 10.0)
        self.speed_x = self.speed_x * 0.95

